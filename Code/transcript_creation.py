import whisper

def format_timestamp(seconds: float):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def group_segments_by_duration(segments, max_duration=15):
    grouped = []
    current_group = []
    group_start = segments[0]['start']
    group_text = ""

    for segment in segments:
        if not current_group:
            group_start = segment['start']
        current_group.append(segment)
        group_text += segment["text"].strip() + " "
        if segment['end'] - group_start >= max_duration:
            grouped.append((group_start, group_text.strip()))
            current_group = []
            group_text = ""

    if current_group:
        grouped.append((group_start, group_text.strip()))

    return grouped

def save_as_custom_format(segments, filepath="transcript.txt"):
    grouped = group_segments_by_duration(segments, max_duration=15)

    with open(filepath, "w", encoding="utf-8") as f:
        for start_time, text in grouped:
            timestamp = format_timestamp(start_time)
            f.write(f"[{timestamp}] - {text}\n")


model = whisper.load_model("base")
result = model.transcribe("video.mp4")

save_as_custom_format(result["segments"], "transcript.txt")
