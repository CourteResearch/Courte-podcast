import os

class Settings:
    PROJECT_NAME: str = "PodVision Studio 3D MVP"
    BLENDER_SCRIPT_PATH: str = os.path.join(os.path.dirname(__file__), "../blender_scripts/animate_podcast_scene.py")
    MODEL_ASSETS_DIR: str = os.path.join(os.path.dirname(__file__), "../assets_for_processing/3d_models")

settings = Settings()
