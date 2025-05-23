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

    # Find male and female avatars within the imported scene
    # IMPORTANT: You will need to replace "MaleCharacterName" and "FemaleCharacterName"
    # with the actual names of the male and female character objects in your FBX file.
    male_avatar = bpy.data.objects.get("MaleCharacterName")
    female_avatar = bpy.data.objects.get("FemaleCharacterName")

    if not male_avatar:
        print("Warning: Male avatar object 'MaleCharacterName' not found in the imported FBX. Please update the script with the correct object name.")
    if not female_avatar:
        print("Warning: Female avatar object 'FemaleCharacterName' not found in the imported FBX. Please update the script with the correct object name.")

    # Add a camera if none exists
    if not bpy.context.scene.camera:
        bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(1.2, 0, 0))
        bpy.context.scene.camera = bpy.context.object
        print("Added default camera.")

    # Add a light if none exists
    if not any(obj.type == 'LIGHT' for obj in bpy.data.objects):
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
        print("Added default light.")

    return male_avatar, female_avatar

def animate_scene(data, male_avatar, female_avatar):
    """Animates the scene based on diarization segments."""
    diarization_segments = data.get("diarization_segments", [])
    audio_path = data["audio_path"]

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

    # Ensure avatars exist before trying to animate
    if not male_avatar and not female_avatar:
        print("No avatars found to animate.")
        return

    # Simple animation: make active speaker slightly visible/active
    # This is a placeholder for actual lip-sync or body animation
    for segment in diarization_segments:
        start_frame = int(segment["start"] * bpy.context.scene.render.fps)
        end_frame = int(segment["end"] * bpy.context.scene.render.fps)
        speaker = segment["speaker"]

        # Ensure objects are not None before accessing properties
        if male_avatar:
            male_avatar.hide_render = True
            male_avatar.hide_viewport = True
            male_avatar.keyframe_insert(data_path="hide_render", frame=start_frame - 1)
            male_avatar.keyframe_insert(data_path="hide_viewport", frame=start_frame - 1)
        if female_avatar:
            female_avatar.hide_render = True
            female_avatar.hide_viewport = True
            female_avatar.keyframe_insert(data_path="hide_render", frame=start_frame - 1)
            female_avatar.keyframe_insert(data_path="hide_viewport", frame=start_frame - 1)

        if speaker == "male" and male_avatar:
            male_avatar.hide_render = False
            male_avatar.hide_viewport = False
            male_avatar.keyframe_insert(data_path="hide_render", frame=start_frame)
            male_avatar.keyframe_insert(data_path="hide_viewport", frame=start_frame)
            male_avatar.hide_render = True
            male_avatar.hide_viewport = True
            male_avatar.keyframe_insert(data_path="hide_render", frame=end_frame)
            male_avatar.keyframe_insert(data_path="hide_viewport", frame=end_frame)
        elif speaker == "female" and female_avatar:
            female_avatar.hide_render = False
            female_avatar.hide_viewport = False
            female_avatar.keyframe_insert(data_path="hide_render", frame=start_frame)
            female_avatar.keyframe_insert(data_path="hide_viewport", frame=start_frame)
            female_avatar.hide_render = True
            female_avatar.hide_viewport = True
            female_avatar.keyframe_insert(data_path="hide_render", frame=end_frame)
            female_avatar.keyframe_insert(data_path="hide_viewport", frame=end_frame)

    # Set all avatars to hidden after the last segment
    last_frame = bpy.context.scene.frame_end
    if male_avatar:
        male_avatar.hide_render = True
        male_avatar.hide_viewport = True
        male_avatar.keyframe_insert(data_path="hide_render", frame=last_frame)
        male_avatar.keyframe_insert(data_path="hide_viewport", frame=last_frame)
    if female_avatar:
        female_avatar.hide_render = True
        female_avatar.hide_viewport = True
        female_avatar.keyframe_insert(data_path="hide_render", frame=last_frame)
        female_avatar.keyframe_insert(data_path="hide_viewport", frame=last_frame)


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
    print(f"Render output path set to: {output_path}")

def main():
    print("Blender script started.")
    if "--" not in sys.argv:
        print("Error: No arguments passed to Blender script.")
        sys.exit(1)

    idx = sys.argv.index("--")
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

    male_avatar, female_avatar = setup_scene(data)
    animate_scene(data, male_avatar, female_avatar)
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
