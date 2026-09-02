"""
Assemble the complete Shadow Cut Hackathon Demo Video (1080p, 30fps, AAC Audio).
Duration: ~2 minutes 56 seconds (exact fit for Devpost 3-minute hard ceiling).
"""
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(".").resolve()
AUDIO_DIR = BASE_DIR / "demo_production" / "audio"
GRAPHICS_DIR = BASE_DIR / "demo_production" / "graphics"
CLIPS_DIR = BASE_DIR / "demo_production" / "clips"
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

FINAL_OUTPUT = BASE_DIR / "demo_production" / "shadow_cut_official_demo.mp4"

BOB_RECORDING = Path(r"C:\Users\zache\Videos\Screen Recordings\Screen Recording 2026-09-04 115233.mp4")
NOTLD_VIDEO = BASE_DIR / "test_data" / "notld" / "farmhouse_scene.mp4"

# Find recorded UI webm
ui_recordings = list((BASE_DIR / "demo_captures" / "ui_raw").glob("*.webm"))
if not ui_recordings:
    raise FileNotFoundError("No UI recording found in demo_captures/ui_raw")
UI_RECORDING = ui_recordings[0]

def run_ffmpeg(cmd, desc=""):
    print(f"\n--- [FFMPEG] {desc} ---")
    print(" ".join(str(x) for x in cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"FFmpeg Error in {desc}:")
        print(result.stderr[-1000:])
        raise RuntimeError(f"FFmpeg command failed: {desc}")
    print(f"  [OK] Completed {desc}")

def build_still_clip(img_path, duration, output_path):
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(img_path),
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-s", "1920x1080",
        str(output_path)
    ]
    run_ffmpeg(cmd, f"Still clip: {output_path.name}")

def build_act1():
    print("\n=== Building Act 1: The Hook ===")
    p1 = CLIPS_DIR / "act1_p1_intro.mp4"
    p2 = CLIPS_DIR / "act1_p2_movie.mp4"
    p3 = CLIPS_DIR / "act1_p3_problem.mp4"
    act1_video = CLIPS_DIR / "act1_video_only.mp4"
    act1_final = CLIPS_DIR / "act1_final.mp4"

    # P1: Intro title (6.0s)
    build_still_clip(GRAPHICS_DIR / "intro_title.png", 6.0, p1)

    # P2: Movie clip (14.0s) from farmhouse_scene.mp4 (ss 5.0, t 14.0) with dark pillarbox and badge
    cmd_p2 = [
        "ffmpeg", "-y",
        "-ss", "5.0",
        "-i", str(NOTLD_VIDEO),
        "-t", "14.0",
        "-vf", "scale=1440:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(p2)
    ]
    run_ffmpeg(cmd_p2, "Act 1 Part 2 Movie Clip")

    # P3: Problem card (12.232s)
    build_still_clip(GRAPHICS_DIR / "problem_card.png", 12.232, p3)

    # Concat P1 + P2 + P3
    concat_list = CLIPS_DIR / "act1_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{p1.name}'\n")
        f.write(f"file '{p2.name}'\n")
        f.write(f"file '{p3.name}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(act1_video)
    ]
    run_ffmpeg(cmd_concat, "Act 1 Video Concat")

    # Merge audio act1_hook.mp3
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", str(act1_video),
        "-i", str(AUDIO_DIR / "act1_hook.mp3"),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(act1_final)
    ]
    run_ffmpeg(cmd_merge, "Act 1 Final Merge")
    return act1_final

def build_act2():
    print("\n=== Building Act 2: Architecture & IBM Bob ===")
    p1 = CLIPS_DIR / "act2_p1_arch.mp4"
    p2 = CLIPS_DIR / "act2_p2_bob.mp4"
    act2_video = CLIPS_DIR / "act2_video_only.mp4"
    act2_final = CLIPS_DIR / "act2_final.mp4"

    # P1: Architecture card (14.0s)
    build_still_clip(GRAPHICS_DIR / "architecture_card.png", 14.0, p1)

    # P2: Bob Screen Recording overlay on bob_layout_bg.png (32.224s)
    # Bob video is 678x954 -> scale to fit 980x980 inside the 1050x1080 left region
    cmd_bob = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(GRAPHICS_DIR / "bob_layout_bg.png"),
        "-ss", "10.0",
        "-i", str(BOB_RECORDING),
        "-t", "32.224",
        "-filter_complex",
        "[1:v]scale=980:980:force_original_aspect_ratio=decrease[bob];[0:v][bob]overlay=40:(1080-overlay_h)/2[v]",
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(p2)
    ]
    run_ffmpeg(cmd_bob, "Act 2 Part 2 Bob Overlay")

    # Concat P1 + P2
    concat_list = CLIPS_DIR / "act2_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{p1.name}'\n")
        f.write(f"file '{p2.name}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(act2_video)
    ]
    run_ffmpeg(cmd_concat, "Act 2 Video Concat")

    # Merge audio act2_architecture_bob.mp3
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", str(act2_video),
        "-i", str(AUDIO_DIR / "act2_architecture_bob.mp3"),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(act2_final)
    ]
    run_ffmpeg(cmd_merge, "Act 2 Final Merge")
    return act2_final

def build_act3():
    print("\n=== Building Act 3: Hero Cinema Audit ===")
    p1 = CLIPS_DIR / "act3_p1_title.mp4"
    p2 = CLIPS_DIR / "act3_p2_barricade.mp4"
    p3 = CLIPS_DIR / "act3_p3_lighter.mp4"
    p4 = CLIPS_DIR / "act3_p4_rifle.mp4"
    p5 = CLIPS_DIR / "act3_p5_table.mp4"
    act3_video = CLIPS_DIR / "act3_video_only.mp4"
    act3_final = CLIPS_DIR / "act3_final.mp4"

    # 5 parts: 10s title, 12s barricade, 11s lighter, 10s rifle, 11.384s table = 54.384s total
    build_still_clip(GRAPHICS_DIR / "audit_title.png", 10.0, p1)
    build_still_clip(GRAPHICS_DIR / "evidence_1_barricade.png", 12.0, p2)
    build_still_clip(GRAPHICS_DIR / "evidence_2_lighter_fluid.png", 11.0, p3)
    build_still_clip(GRAPHICS_DIR / "evidence_3_rifle.png", 10.0, p4)
    build_still_clip(GRAPHICS_DIR / "evidence_4_table_deviation.png", 11.384, p5)

    concat_list = CLIPS_DIR / "act3_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{p1.name}'\n")
        f.write(f"file '{p2.name}'\n")
        f.write(f"file '{p3.name}'\n")
        f.write(f"file '{p4.name}'\n")
        f.write(f"file '{p5.name}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(act3_video)
    ]
    run_ffmpeg(cmd_concat, "Act 3 Video Concat")

    cmd_merge = [
        "ffmpeg", "-y",
        "-i", str(act3_video),
        "-i", str(AUDIO_DIR / "act3_hero_audit.mp3"),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(act3_final)
    ]
    run_ffmpeg(cmd_merge, "Act 3 Final Merge")
    return act3_final

def build_act4():
    print("\n=== Building Act 4: Command Center & Outro ===")
    p1 = CLIPS_DIR / "act4_p1_ui.mp4"
    p2 = CLIPS_DIR / "act4_p2_outro.mp4"
    act4_video = CLIPS_DIR / "act4_video_only.mp4"
    act4_final = CLIPS_DIR / "act4_final.mp4"

    # P1: UI recording (32.0s)
    # Convert webm to 1080p 30fps h264
    cmd_ui = [
        "ffmpeg", "-y",
        "-i", str(UI_RECORDING),
        "-t", "32.0",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(p1)
    ]
    run_ffmpeg(cmd_ui, "Act 4 Part 1 UI Transcode")

    # P2: Outro card (11.344s)
    build_still_clip(GRAPHICS_DIR / "outro_card.png", 11.344, p2)

    concat_list = CLIPS_DIR / "act4_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        f.write(f"file '{p1.name}'\n")
        f.write(f"file '{p2.name}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(act4_video)
    ]
    run_ffmpeg(cmd_concat, "Act 4 Video Concat")

    cmd_merge = [
        "ffmpeg", "-y",
        "-i", str(act4_video),
        "-i", str(AUDIO_DIR / "act4_command_center.mp3"),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(act4_final)
    ]
    run_ffmpeg(cmd_merge, "Act 4 Final Merge")
    return act4_final

def assemble_master(act1, act2, act3, act4):
    print("\n=== Assembling Master Demo Video ===")
    master_concat = CLIPS_DIR / "master_concat.txt"
    with open(master_concat, "w", encoding="utf-8") as f:
        f.write(f"file '{act1.name}'\n")
        f.write(f"file '{act2.name}'\n")
        f.write(f"file '{act3.name}'\n")
        f.write(f"file '{act4.name}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(master_concat),
        "-c", "copy",
        str(FINAL_OUTPUT)
    ]
    run_ffmpeg(cmd, "Master Video Concatenation")
    print(f"\n=======================================================")
    print(f"SUCCESS! Master Demo Video created at: {FINAL_OUTPUT}")
    print(f"File size: {FINAL_OUTPUT.stat().st_size / (1024*1024):.2f} MB")
    print(f"=======================================================")

if __name__ == "__main__":
    a1 = build_act1()
    a2 = build_act2()
    a3 = build_act3()
    a4 = build_act4()
    assemble_master(a1, a2, a3, a4)
