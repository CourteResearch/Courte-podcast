import subprocess
import json
from pathlib import Path
from app.core.config import settings
from pydub import AudioSegment
import os

# Placeholder for diarization
def get_diarization_segments(audio_path: str):
    """
    Placeholder function for speaker diarization.
    In a real application, this would use a proper diarization library
    to identify speaker segments.
    For now, it simulates alternating speakers.
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        duration_ms = len(audio)
        duration_s = duration_ms / 1000

        segments = []
        # Simulate 10-second segments, alternating speakers
        current_time = 0
        speaker_toggle = True # True for male, False for female
        while current_time < duration_s:
            speaker = "male" if speaker_toggle else "female"
            end_time = min(current_time + 10, duration_s) # 10-second segments
            segments.append({"start": current_time, "end": end_time, "speaker": speaker})
            current_time = end_time
            speaker_toggle = not speaker_toggle
        return segments
    except Exception as e:
        print(f"Error during placeholder diarization: {e}")
        # Return a default segment if audio processing fails
        return [{"start": 0, "end": 10, "speaker": "male"}]


def create_3d_video_from_audio(audio_path_str: str, output_video_path_str: str, speaker_mapping: dict):
    # 1. Diarization
    segments = get_diarization_segments(audio_path_str)
    print(f"Diarization segments: {segments}")

    # 2. Prepare data for Blender script
    blender_input_data = {
        "audio_path": audio_path_str,
        "speaker_mapping": speaker_mapping,
        "diarization_segments": segments, # Pass segments to Blender
        "studio_model": str(Path(settings.MODEL_ASSETS_DIR) / "studio_environment.fbx"), # Changed to FBX
        "male_model": str(Path(settings.MODEL_ASSETS_DIR) / "male_avatar.glb"),
        "female_model": str(Path(settings.MODEL_ASSETS_DIR) / "female_avatar.glb"),
        "output_render_path": str(Path(output_video_path_str).with_suffix('.blend_render.mp4')) # Blender will render to this temp path
    }

    # 3. Save input data to a temporary JSON file
    temp_json_path = Path("blender_scene_data.json")
    with open(temp_json_path, 'w') as f:
        json.dump(blender_input_data, f)
    print(f"Blender input data saved to {temp_json_path}")

    # 4. Invoke Blender
    blender_command = [
        "blender",
        "--background",
        "--python", str(Path(settings.BLENDER_SCRIPT_PATH)),
        "--", str(temp_json_path)
    ]
    print(f"Invoking Blender with command: {' '.join(blender_command)}")

    try:
        subprocess.run(blender_command, check=True, capture_output=True, text=True)
        print("Blender command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Blender rendering failed: {e.stderr}")
        raise

    # 5. Assemble video (combine Blender output with original audio)
    # This step assumes Blender renders a video without audio.
    # If Blender renders with audio, this step might be simplified or skipped.
    blender_rendered_video = Path(blender_input_data["output_render_path"])
    if not blender_rendered_video.exists():
        print(f"Warning: Blender did not produce expected output at {blender_rendered_video}. Skipping final assembly.")
        # If Blender doesn't produce output, we can't assemble.
        # For now, just copy the audio as a placeholder for the final video.
        # In a real scenario, this would be an error or a more robust fallback.
        # shutil.copy(audio_path_str, output_video_path_str)
        # print(f"Copied audio to {output_video_path_str} as placeholder.")
        raise FileNotFoundError(f"Blender output video not found at {blender_rendered_video}")


    print(f"Assembling final video: {output_video_path_str}")
    ffmpeg_command = [
        "ffmpeg",
        "-i", str(blender_rendered_video),
        "-i", audio_path_str,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        "-y", # Overwrite output file if it exists
        output_video_path_str
    ]
    try:
        subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
        print(f"Final video assembled and saved to {output_video_path_str}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg video assembly failed: {e.stderr}")
        raise

    # Clean up temporary files
    if temp_json_path.exists():
        os.remove(temp_json_path)
    if blender_rendered_video.exists():
        os.remove(blender_rendered_video)

    print(f"3D Video saved to {output_video_path_str}")
