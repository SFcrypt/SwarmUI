import subprocess
import os
from IPython.display import clear_output

def run_update():

    os.makedirs("/home/studio-lab-user/SwarmUI/dlbackend", exist_ok=True)
    os.makedirs("/home/studio-lab-user/SwarmUI/Models/diffusion_models", exist_ok=True)

    subprocess.run([
        "git", "clone",
        "https://github.com/SFcrypt/ComfyUI",
        "/home/studio-lab-user/SwarmUI/dlbackend/ComfyUI"
    ])

    subprocess.run([
        "git", "clone",
        "https://github.com/SFcrypt/SwarmUI",
        "/home/studio-lab-user/SwarmUI/SwarmUI_tmp"
    ])

    subprocess.run(
        "cp -r /home/studio-lab-user/SwarmUI/SwarmUI_tmp/* /home/studio-lab-user/SwarmUI/",
        shell=True
    )

    subprocess.run(
        "rm -rf /home/studio-lab-user/SwarmUI/SwarmUI_tmp",
        shell=True
    )

    clear_output()
    print("SwarmUI Actualizado.")