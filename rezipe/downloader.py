import json
import yt_dlp

URL = 'https://www.facebook.com/reel/1637777207153125'

# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    print(json.dumps(ydl.sanitize_info(info)))


# --cookies-from-browser BROWSER[+KEYRING][:PROFILE][::CONTAINER]