import subprocess
import shutil
import sys

video_url = sys.argv[1]
output_filename = "video"

yt_dlp_path = shutil.which("yt-dlp")
if yt_dlp_path is None:
    raise Exception("yt-dlp not found. Make sure it's installed.")

command = [
    yt_dlp_path,
    "--write-auto-sub",
    "--sub-lang", "en",
    "--convert-subs", "srt",
    "--write-sub",
    "--extractor-args", "youtube:player_client=android",
    "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
    "-o", f"{output_filename}.%(ext)s",
    video_url
]

subprocess.run(command)