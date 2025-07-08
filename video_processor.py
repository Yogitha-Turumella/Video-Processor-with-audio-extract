import os
import ffmpeg

# File paths
INPUT_PATH = "input_videos/input.mp4"
OUTPUT_DIR = "processed_outputs"

def ensure_output_folder():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_audio():
    """Extracts audio and saves it as audio.wav"""
    ensure_output_folder()
    audio_out = os.path.join(OUTPUT_DIR, "audio.wav")
    ffmpeg.input(INPUT_PATH).output(audio_out, **{'q:a': 0, 'map': 'a'}).run()
    print(f"[✔] Audio extracted → {audio_out}")

def resize_video():
    """Resizes video to vertical 1080x1920 with padding"""
    ensure_output_folder()
    output_path = os.path.join(OUTPUT_DIR, "output.mp4")
    vf = "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
    ffmpeg.input(INPUT_PATH).output(output_path, vf=vf).run()
    print(f"[✔] Video resized to vertical → {output_path}")

def get_video_duration():
    """Returns video duration in seconds"""
    probe = ffmpeg.probe(INPUT_PATH)
    return float(probe['format']['duration'])

def chunk_if_long(threshold_minutes=10):
    """Splits video into 5-min chunks if longer than threshold"""
    duration_sec = get_video_duration()
    if duration_sec > threshold_minutes * 60:
        output_pattern = os.path.join(OUTPUT_DIR, "chunk_%03d.mp4")
        ffmpeg.input(INPUT_PATH).output(
            output_pattern, c='copy', map='0', f='segment', segment_time=300
        ).run()
        print(f"[✔] Video split into 5-min chunks")
    else:
        print(f"[ℹ️] Skipping chunking — duration is {duration_sec / 60:.1f} minutes")

# Run everything
if __name__ == "__main__":
    print(f"📁 Processing: {INPUT_PATH}")
    extract_audio()
    resize_video()
    chunk_if_long()
    print("✅ All tasks completed!")
