import sys
import bpy
import json
from pathlib import Path

def clear_scene():
    """Clears all objects, meshes, materials, and textures from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Clear all collections
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

    # Clear all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

    # Clear all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    # Clear all textures
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

    # Clear all images
    for image in bpy.data.images:
        bpy.data.images.remove(image)

def import_fbx(filepath):
    """Imports an FBX file and returns the imported objects."""
    bpy.ops.import_scene.fbx(filepath=filepath)
    # Return the newly imported objects (assuming they are selected after import)
    return bpy.context.selected_objects

def setup_scene(data):
    """Sets up the 3D scene based on input data."""
    clear_scene()

    # Import studio environment (FBX)
    studio_path = Path(data["studio_model"])
    if studio_path.exists():
        print(f"Importing studio environment: {studio_path}")
        import_fbx(str(studio_path)) # Use import_fbx
    else:
        print(f"Error: Studio model not found at {studio_path}. Please ensure 'studio_environment.fbx' is in '3d_assets/'.")
        sys.exit(1) # Exit if critical model is missing

    # Add a camera if none exists
    if not bpy.context.scene.camera:
        bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(1.2, 0, 0))
        bpy.context.scene.camera = bpy.context.object
        print("Added default camera.")

    # Add a light if none exists
    if not any(obj.type == 'LIGHT' for obj in bpy.data.objects):
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
        print("Added default light.")

    # No need to return avatars as we are animating camera instead of avatars directly
    return None, None

def animate_scene(data):
    """Animates the scene based on diarization segments, focusing on camera movement."""
    diarization_segments = data.get("diarization_segments", [])
    audio_path = data["audio_path"]
    camera = bpy.context.scene.camera

    if not camera:
        print("Error: No camera found in scene for animation.")
        return

    # Set scene frame rate
    bpy.context.scene.render.fps = 24 # Standard frame rate

    # Load audio to get its duration
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(audio_path)
        audio_duration_s = len(audio) / 1000
        bpy.context.scene.frame_end = int(audio_duration_s * bpy.context.scene.render.fps)
        print(f"Audio duration: {audio_duration_s}s. Setting frame_end to {bpy.context.scene.frame_end}")
    except Exception as e:
        print(f"Could not load audio for duration: {e}. Using default frame_end.")
        bpy.context.scene.frame_end = 250 # Default to 10 seconds at 24fps

    # Define camera positions for male and female sides
    # These are example coordinates and rotations. You might need to adjust them
    # based on your specific FBX scene layout.
    camera_male_pos = (-2.5, -3.5, 1.5)
    camera_male_rot = (1.3, 0, -0.7) # (pitch, yaw, roll) in radians

    camera_female_pos = (2.5, -3.5, 1.5)
    camera_female_rot = (1.3, 0, 0.7) # (pitch, yaw, roll) in radians

    # Set interpolation to linear for smoother transitions
    for fcurve in camera.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'

    # Animate camera based on speaker segments
    current_frame = 1
    for segment in diarization_segments:
        start_frame = int(segment["start"] * bpy.context.scene.render.fps)
        end_frame = int(segment["end"] * bpy.context.scene.render.fps)
        speaker = segment["speaker"]

        # Ensure camera is at the correct position/rotation at the start of the segment
        if speaker == "male":
            camera.location = camera_male_pos
            camera.rotation_euler = camera_male_rot
        elif speaker == "female":
            camera.location = camera_female_pos
            camera.rotation_euler = camera_female_rot

        camera.keyframe_insert(data_path="location", frame=start_frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=start_frame)

        # If this is not the last segment, set keyframe for next segment's start
        if segment != diarization_segments[-1]:
            next_segment_start_frame = int(diarization_segments[diarization_segments.index(segment) + 1]["start"] * bpy.context.scene.render.fps)
            # Ensure camera holds position until just before next segment starts
            camera.keyframe_insert(data_path="location", frame=next_segment_start_frame - 1)
            camera.keyframe_insert(data_path="rotation_euler", frame=next_segment_start_frame - 1)
        else:
            # For the last segment, hold position until the end of the animation
            camera.keyframe_insert(data_path="location", frame=bpy.context.scene.frame_end)
            camera.keyframe_insert(data_path="rotation_euler", frame=bpy.context.scene.frame_end)


def configure_render(output_path):
    """Configures Blender's rendering settings."""
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
    bpy.context.scene.render.ffmpeg.gopsize = 18
    bpy.context.scene.render.ffmpeg.max_b_frames = 2
    bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'
    bpy.context.scene.render.filepath = output_path

    # Set resolution to 16:9 (e.g., 1920x1080)
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100 # Render at 100% of set resolution

    print(f"Render output path set to: {output_path}")
    print(f"Render resolution set to {bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}")

def main():
    print("Blender script started.")
    if "--" not in sys.argv:
        print("Error: No arguments passed to Blender script.")
        sys.exit(1)

    idx = sys.argv[2:].index("--") + 2 # Adjust index for --background --python
    args = sys.argv[idx+1:]
    if not args:
        print("Error: No data file path provided.")
        sys.exit(1)

    data_file_path = Path(args[0])
    if not data_file_path.exists():
        print(f"Error: Data file not found at {data_file_path}")
        sys.exit(1)

    with open(data_file_path, 'r') as f:
        data = json.load(f)
    print(f"Loaded data from {data_file_path}")

    setup_scene(data)
    animate_scene(data) # Pass only data, as avatars are not separate
    configure_render(data["output_render_path"])

    print("Starting Blender render...")
    try:
        bpy.ops.render.render(animation=True)
        print("Blender render completed successfully.")
    except Exception as e:
        print(f"Blender rendering failed during bpy.ops.render.render: {e}")
        sys.exit(1)

    # Clean up temporary data file
    if data_file_path.exists():
        data_file_path.unlink()
        print(f"Cleaned up temporary data file: {data_file_path}")

    print("Blender script finished.")

if __name__ == "__main__":
    main()
