import ollama
import ffmpeg
import os
import re



with open("transcript.txt", "r", encoding="utf-8") as file:
    transcript = file.read()


prompt = f"""
You are a viral content strategist helping extract the most gripping and shareable moments from a YouTube interview transcript to create 45-90 second Shorts.

Transcript (formatted with timestamps):

{transcript}

YOUR TASK:
- Choose 3 to 5 moments from the transcript that are each between 45 and 60 seconds long.
- Segments must be **non-overlapping** and spaced at least 1 minute apart.
- Select moments that contain **shock, suspense, emotional intensity, or unexpected revelations**.
- Prioritize segments with **visual storytelling or strong spoken emotion** (even without video/audio).
- Avoid dry technical analysis or long monologues with no clear hook.

OUTPUT FORMAT (only return this!):
HH:MM:SS - "Catchy title that teases the segment's mystery or drama"

EXAMPLES:
00:03:17 - "He Saw Something in the Sky... Then Everything Went Silent"
00:07:45 - "The Day a Farmer Froze Watching a UFO in His Field"
00:12:01 - "This UFO Encounter Was So Real, the FBI Got Involved"

DO NOT include extra commentary or explanations — just the list.
"""

# Query LLaMA 3
response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
x = (response['message']['content'])
input_data = f"""{x}"""
video_path = 'video.mp4'


output_dir = 'output_clips'
os.makedirs(output_dir, exist_ok=True)

# Get video dimensions
probe = ffmpeg.probe(video_path)
video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
width = int(video_stream['width'])
height = int(video_stream['height'])

# Calculate 9:16 crop (centered)
target_height = height
target_width = int(height * 9 / 16)
x_offset = (width - target_width) // 2

# Parse input
entries = re.findall(r'(\d{2}:\d{2}:\d{2})\s*-\s*\"([^"]+)\"', input_data)

# Sanitize file names
def safe_filename(title):
    return re.sub(r'[\\/*?:"<>|]', '', title)

# Process each clip
for i, (start_time, title) in enumerate(entries, 1):
    safe_title = safe_filename(title)
    output_path = os.path.join(output_dir, f"{i:02d} - {safe_title}.mp4")


    video = (
        ffmpeg
        .input(video_path, ss=start_time, t=90)
        .filter('crop', target_width, target_height, x_offset, 0)
    )

    audio = (
        ffmpeg
        .input(video_path, ss=start_time, t=90)
        .audio
    )

    (
        ffmpeg
        .output(video, audio, output_path, vcodec='libx264', acodec='aac', strict='experimental')
        .overwrite_output()
        .run()
    )

