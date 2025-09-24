# Automated YouTube Shorts Generator

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green)](https://ffmpeg.org/)
[![Ollama](https://img.shields.io/badge/Ollama-LLaMA3-orange)](https://ollama.ai/)

## Project Description
**Automated YouTube Shorts Generator** is an **AI-powered system** that transforms long YouTube videos into **viral-ready Shorts**.  
The pipeline downloads a video, transcribes it with Whisper, extracts the most engaging moments using LLaMA 3, clips them into a vertical 9:16 format with FFmpeg, and embeds styled subtitles using WhisperX + pysubs2.  

The system can:
- **Download any YouTube video** using yt-dlp  
- **Generate transcriptions** and word-level subtitles  
- **Select engaging segments** automatically with LLaMA 3  
- **Produce ready-to-publish Shorts** with captions and formatting  

---

## Features

| Feature | Description |
|----------|-------------|
| Video Download | Fetches any YouTube video using **yt-dlp** |
| Transcription | Converts speech into text using **Whisper** |
| Smart Segment Selection | Identifies viral-worthy clips with **LLaMA 3 (Ollama)** |
| Clipping & Formatting | Crops and edits into **9:16 Shorts** using **FFmpeg** |
| Subtitles | Generates word-level subtitles with **WhisperX + pysubs2** |
| Automated Pipeline | End-to-end automation from **URL → Shorts folder** |

---

## Screenshots

**Pipeline Overview**  
![Pipeline Overview](docs/pipeline.png)  

**Sample Short**  
![Before](docs/Before.PNG)

![After(Sample Short)](docs/sample.gif)  

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone <repository_url>
cd automated-shorts-generator
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Install required tools

### 4. Run the pipeline
```bash
Automated-Short-Video-Content-Creation/Code/main.py
```
### 5. Check output
Generated Shorts will be stored in:
```bash
Automated-Short-Video-Content-Creation/final_output_clips
```
## Future Scope

- **Multi-language subtitle support**
- **AI-generated thumbnails**
- **Direct upload to YouTube via API**
- **Automatic background music & effects**
