import whisperx
import torch
import os
import re
from pysubs2 import SSAFile, SSAEvent, SSAStyle
import pysubs2
import glob
import subprocess

folder_path = os.path.join(os.path.dirname(__file__), "output_clips")


files = os.listdir(folder_path)


file_names = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]


def generate_word_srt(input_file, output_srt):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = whisperx.load_model("large-v3", device=device, compute_type="float32")

    result = model.transcribe(input_file)

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    aligned_result = whisperx.align(result["segments"], model_a, metadata, input_file, device=device)

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

    pattern = re.compile(r"(\d+)\n([\d:,]+) --> ([\d:,]+)\n(.*?)\n", re.DOTALL)
    entries = pattern.findall(srt)

    adjusted_entries = []

    for i in range(len(entries)):
        index, start, end, text = entries[i]

        if i < len(entries) - 1:
            next_start = entries[i + 1][1]
            end = next_start

        adjusted_entries.append(f"{index}\n{start} --> {end}\n{text}\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(adjusted_entries)

def srt_to_ass_with_adjusted_style(srt_path, ass_path):
    subs = pysubs2.load(srt_path, encoding="utf-8")

    style = SSAStyle()
    style.fontname = "Arial"
    style.fontsize = 18                     
    style.primarycolor = pysubs2.Color(255, 255, 255, 0)  
    style.outlinecolor = pysubs2.Color(0, 0, 0, 0)       
    style.backcolor = pysubs2.Color(0, 0, 0, 127)         
    style.bold = True
    style.shadow = 0
    style.outline = 1                      
    style.alignment = 2                     
    style.marginl = 10
    style.marginr = 10
    style.marginv = 70                    

    subs.styles["Default"] = style
    for line in subs:
        line.style = "Default"

    subs.save(ass_path)

def delete_all_files(folder_path):
    files = glob.glob(os.path.join(folder_path, "*"))
    for file in files:
        if os.path.isfile(file):
            os.remove(file)

repo_dir = os.path.dirname(__file__)
output_clips_dir = os.path.join(repo_dir, "output_clips")
temp_dir = os.path.join(repo_dir, "temp")
final_output_dir = os.path.join(repo_dir, "final_output_clips")

for i in file_names:
    input_clip = os.path.join(output_clips_dir, i)
    word_srt_file = os.path.join(temp_dir, "word_by_word.srt")
    adjusted_srt_file = os.path.join(temp_dir, "adjusted_word_by_word.srt")
    styled_ass_file = os.path.join(temp_dir, "styled_output.ass")
    output_video_file = os.path.join(final_output_dir, i)

    generate_word_srt(input_clip, word_srt_file)
    adjust_srt_timing(word_srt_file, adjusted_srt_file)
    srt_to_ass_with_adjusted_style(adjusted_srt_file, styled_ass_file)

    subtitle_path = styled_ass_file.replace("\\", "/").replace(":", "\\:")
    vf_filter = f"ass='{subtitle_path}'"
    command = [
        "ffmpeg",
        "-i", input_clip,
        "-vf", vf_filter,
        "-c:a", "copy",
        output_video_file
    ]
    subprocess.run(command)

    delete_all_files(temp_dir)


