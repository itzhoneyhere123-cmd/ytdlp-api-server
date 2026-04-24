import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# Plugin folder (agar future mein koi custom site add karni ho to)
os.environ['YTDLP_PLUGIN_DIRS'] = './plugins'

@app.route('/extract')
def extract():
    url = request.args.get('url', '')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400
    ydl_opts = {
        'quiet': True,
        'format': 'best[height<=720]',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'url': info.get('url'),
                'title': info.get('title'),
                'ext': info.get('ext'),
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
