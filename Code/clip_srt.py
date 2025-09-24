import whisperx
import torch
import os
import re
from pysubs2 import SSAFile, SSAEvent, SSAStyle
import pysubs2
import glob
import subprocess
# Specify the folder path
folder_path = r"C:\Users\shara\Desktop\Final_yt_project\output_clips"

# List all files
files = os.listdir(folder_path)

# Filter out only files (ignore subfolders)
file_names = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]


def generate_word_srt(input_file, output_srt):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Step 1: Load ASR model
    model = whisperx.load_model("large-v3", device=device, compute_type="float32")

    # Step 2: Transcribe to get segments
    result = model.transcribe(input_file)

    # Step 3: Load alignment model
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    # Step 4: Align to get word-level timestamps
    aligned_result = whisperx.align(result["segments"], model_a, metadata, input_file, device=device)

    # Step 5: Write to .srt
    with open(output_srt, "w", encoding="utf-8") as f:
        for i, word in enumerate(aligned_result["word_segments"]):
            f.write(f"{i + 1}\n")
            f.write(f"{format_timestamp(word['start'])} --> {format_timestamp(word['end'])}\n")
            f.write(f"{word['word'].strip()}\n\n")

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def parse_srt_time(srt_time):
    """Convert SRT timestamp to seconds."""
    hours, minutes, seconds = srt_time.replace(",", ":").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

def format_srt_time(seconds):
    """Convert seconds to SRT timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:06.3f}".replace(".", ",")

def adjust_srt_timing(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        srt = f.read()

    # Match SRT blocks
    pattern = re.compile(r"(\d+)\n([\d:,]+) --> ([\d:,]+)\n(.*?)\n", re.DOTALL)
    entries = pattern.findall(srt)

    adjusted_entries = []

    for i in range(len(entries)):
        index, start, end, text = entries[i]

        # Use start time of next block as current end, if not last
        if i < len(entries) - 1:
            next_start = entries[i + 1][1]
            end = next_start

        adjusted_entries.append(f"{index}\n{start} --> {end}\n{text}\n")

    # Write adjusted SRT
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(adjusted_entries)

def srt_to_ass_with_adjusted_style(srt_path, ass_path):
    # Load the SRT file
    subs = pysubs2.load(srt_path, encoding="utf-8")

    # Define an improved style
    style = SSAStyle()
    style.fontname = "Arial"
    style.fontsize = 18                     # Slightly smaller
    style.primarycolor = pysubs2.Color(255, 255, 255, 0)  # White
    style.outlinecolor = pysubs2.Color(0, 0, 0, 0)        # Black outline
    style.backcolor = pysubs2.Color(0, 0, 0, 127)         # Transparent black bg (optional)
    style.bold = True
    style.shadow = 0
    style.outline = 1                       # Soft outline for better readability
    style.alignment = 2                     # Bottom-center
    style.marginl = 10
    style.marginr = 10
    style.marginv = 70                      # ↓ Lower on screen (was 100 before)

    # Apply the style
    subs.styles["Default"] = style
    for line in subs:
        line.style = "Default"

    # Save ASS file
    subs.save(ass_path)

def delete_all_files(folder_path):
    files = glob.glob(os.path.join(folder_path, "*"))
    for file in files:
        if os.path.isfile(file):
            os.remove(file)


# Run
for i in file_names:
    generate_word_srt(f"C:\\Users\\shara\\Desktop\\Final_yt_project\\output_clips\\{i}", "C:\\Users\\shara\\Desktop\\Final_yt_project\\temp\\word_by_word.srt")
    adjust_srt_timing(r"C:\Users\shara\Desktop\Final_yt_project\temp\word_by_word.srt", r"C:\Users\shara\Desktop\Final_yt_project\temp\adjusted_word_by_word.srt")
    srt_to_ass_with_adjusted_style(r"C:\Users\shara\Desktop\Final_yt_project\temp\adjusted_word_by_word.srt", r"C:\Users\shara\Desktop\Final_yt_project\temp\styled_output.ass")

    input_video = f"C:\\Users\\shara\\Desktop\\Final_yt_project\\output_clips\\{i}"
    subtitle_file = r"C:\Users\shara\Desktop\Final_yt_project\temp\styled_output.ass"
    output_video = f"C:\\Users\\shara\\Desktop\\Final_yt_project\\final_output_clips\\{i}"

    # Convert to FFmpeg-safe Windows path: escape colon
    subtitle_path = subtitle_file.replace("\\", "/").replace(":", "\\:")

    # Use shlex.quote to properly quote for subprocess
    vf_filter = f"ass='{subtitle_path}'"

    command = [
        "ffmpeg",
        "-i", input_video,
        "-vf", vf_filter,
        "-c:a", "copy",
        output_video
    ]
    subprocess.run(command)
    delete_all_files(r"C:\Users\shara\Desktop\Final_yt_project\temp")

