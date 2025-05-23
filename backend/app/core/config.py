import os

class Settings:
    PROJECT_NAME: str = "PodVision Studio 3D MVP"
    BLENDER_SCRIPT_PATH: str = os.path.join(os.path.dirname(__file__), "../blender_scripts/animate_podcast_scene.py")
    MODEL_ASSETS_DIR: str = os.path.join(os.path.dirname(__file__), "../../3d_assets")

settings = Settings()
