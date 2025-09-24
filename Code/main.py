import subprocess
import sys

def run_script(script_name, *args):
    try:
        command = [sys.executable, script_name] + list(args)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")
        sys.exit(1)

def main():
    # Step 1: Get YouTube video URL from user
    video_url = input("Enter the YouTube video URL: ").strip()

    print("\nRunning: download_yt_video.py...")
    run_script("download_yt_video.py", video_url)

    print("\nRunning: transcript_creation.py...")
    run_script("transcript_creation.py")

    print("\nRunning: short_discovery_and_clipping.py...")
    run_script("short_discovery_and_clipping.py")

    print("\nRunning: clip_srt.py...")
    run_script("clip_srt.py")

    print("\n Task Completed 🎇")

if __name__ == "__main__":
    main()
