import subprocess
import os
from backend.config import settings

def render_plantuml_to_png(puml_code: str, output_path: str) -> bytes:
    """
    Saves PlantUML code to a .puml file and renders it into a PNG using the PlantUML JAR.
    Returns PNG image bytes.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        puml_file = output_path.replace(".png", ".puml")

        # Write the PlantUML code to file
        with open(puml_file, "w", encoding="utf-8") as f:
            f.write(puml_code)

        # Run PlantUML JAR to generate PNG
        subprocess.run(
            ["java", "-jar", settings.PLANTUML_JAR_PATH, puml_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # ✅ Read and return the PNG bytes
        with open(output_path, "rb") as img_file:
            return img_file.read()

    except Exception as e:
        print(f"❌ PlantUML rendering failed: {e}")
        raise RuntimeError("Rendering failed")
