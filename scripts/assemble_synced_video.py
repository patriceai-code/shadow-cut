"""
Assemble perfectly synchronized demo video beat-by-beat.
Every visual transition triggers on the exact word spoken by the narrator.
Total duration: ~2 minutes 50 seconds.
"""
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(".").resolve()
AUDIO_DIR = BASE_DIR / "demo_production" / "audio_synced"
GRAPHICS_DIR = BASE_DIR / "demo_production" / "graphics"
CLIPS_DIR = BASE_DIR / "demo_production" / "synced_clips"
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

FINAL_OUTPUT = BASE_DIR / "demo_production" / "shadow_cut_official_demo.mp4"
VIDEOS_FOLDER_OUTPUT = Path(r"C:\Users\zache\Videos\shadow_cut_official_demo.mp4")

BOB_RECORDING = Path(r"C:\Users\zache\Videos\Screen Recordings\Screen Recording 2026-09-04 115233.mp4")
NOTLD_VIDEO = BASE_DIR / "test_data" / "notld" / "farmhouse_scene.mp4"

ui_recordings = sorted(
    (BASE_DIR / "demo_captures" / "ui_raw").glob("*.webm"),
    key=lambda f: f.stat().st_mtime,
    reverse=True
)
if not ui_recordings:
    raise FileNotFoundError("No UI recording found in demo_captures/ui_raw")
UI_RECORDING = ui_recordings[0]

def run_ffmpeg(cmd, desc=""):
    print(f"\n--- [FFMPEG] {desc} ---")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"FFmpeg Error in {desc}:")
        print(result.stderr[-800:])
        raise RuntimeError(f"FFmpeg command failed: {desc}")
    print(f"  [OK] Completed {desc}")

def assemble_all():
    manifest_path = BASE_DIR / "demo_production" / "beat_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        beats = json.load(f)

    concat_files = []

    for i, b in enumerate(beats, 1):
        beat_id = b["id"]
        dur = b["duration"]
        audio_file = Path(b["audio_file"])
        video_clip = CLIPS_DIR / f"{beat_id}_v.mp4"
        final_clip = CLIPS_DIR / f"{beat_id}_final.mp4"

        v_type = b["visual_type"]
        print(f"\n[{i}/{len(beats)}] Rendering Beat: {beat_id} ({dur}s, {v_type})")

        # Step 1: Render video stream
        if v_type == "still":
            img = GRAPHICS_DIR / b["visual_file"]
            cmd_v = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(img),
                "-t", str(dur),
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                "-s", "1920x1080",
                str(video_clip)
            ]
            run_ffmpeg(cmd_v, f"Still {beat_id}")

        elif v_type == "movie_clip":
            cmd_v = [
                "ffmpeg", "-y",
                "-ss", "5.0",
                "-i", str(NOTLD_VIDEO),
                "-t", str(dur),
                "-vf", "scale=1440:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                str(video_clip)
            ]
            run_ffmpeg(cmd_v, f"Movie Clip {beat_id}")

        elif v_type == "bob_recording":
            ss = b.get("ss", 10.0)
            cmd_v = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(GRAPHICS_DIR / "bob_layout_bg.png"),
                "-ss", str(ss),
                "-i", str(BOB_RECORDING),
                "-t", str(dur),
                "-filter_complex",
                "[1:v]scale=980:980:force_original_aspect_ratio=decrease[bob];[0:v][bob]overlay=40:(1080-overlay_h)/2[v]",
                "-map", "[v]",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                str(video_clip)
            ]
            run_ffmpeg(cmd_v, f"Bob Recording {beat_id}")

        elif v_type == "ui_segment":
            ss = b.get("ss", 0.0)
            cmd_v = [
                "ffmpeg", "-y",
                "-ss", str(ss),
                "-i", str(UI_RECORDING),
                "-t", str(dur),
                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                str(video_clip)
            ]
            run_ffmpeg(cmd_v, f"UI Segment {beat_id}")

        # Step 2: Merge audio with video for this beat (pad audio to exact duration if needed)
        cmd_merge = [
            "ffmpeg", "-y",
            "-i", str(video_clip),
            "-i", str(audio_file),
            "-filter_complex", f"[1:a]apad=whole_dur={dur}[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-ar", "48000",
            "-b:a", "192k",
            "-t", str(dur),
            str(final_clip)
        ]
        run_ffmpeg(cmd_merge, f"Merge Beat {beat_id}")
        concat_files.append(final_clip)

    # Step 3: Concat all beats into master video
    concat_list = CLIPS_DIR / "synced_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in concat_files:
            f.write(f"file '{cf.name}'\n")

    cmd_master = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(FINAL_OUTPUT)
    ]
    run_ffmpeg(cmd_master, "Master Concatenation")

    # Step 4: Copy to user's Videos folder
    import shutil
    shutil.copyfile(FINAL_OUTPUT, VIDEOS_FOLDER_OUTPUT)
    print(f"\n=======================================================")
    print(f"SUCCESS! Synchronized Demo Video created at:")
    print(f"  -> {FINAL_OUTPUT}")
    print(f"  -> {VIDEOS_FOLDER_OUTPUT}")
    print(f"File size: {FINAL_OUTPUT.stat().st_size / (1024*1024):.2f} MB")
    print(f"=======================================================")

if __name__ == "__main__":
    assemble_all()
