import subprocess
import os
from IPython.display import clear_output

def run_update():
    base = os.path.expanduser("~/SwarmUI")

    os.makedirs(f"{base}/dlbackend", exist_ok=True)
    os.makedirs(f"{base}/Models/diffusion_models", exist_ok=True)

    subprocess.run([
        "git", "clone",
        "https://github.com/SFcrypt/ComfyUI",
        f"{base}/dlbackend/ComfyUI"
    ])

    subprocess.run([
        "git", "clone",
        "https://github.com/SFcrypt/SwarmUI",
        f"{base}/SwarmUI_tmp"
    ])

    subprocess.run(
        f"cp -r {base}/SwarmUI_tmp/* {base}/",
        shell=True
    )

    subprocess.run(
        f"rm -rf {base}/SwarmUI_tmp",
        shell=True
    )

    clear_output()
    print("SwarmUI Actualizado.")

if __name__ == "__main__":
    run_update()
