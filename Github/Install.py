R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

import sys, subprocess
python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f'{ERR}: Python version 3.10.6 or higher required, and you are using Python {python_version}')
    sys.exit()

from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from pathlib import Path
import shutil
import shlex
import json
import os

from nenen88 import pull, say, download, clone, tempe

REPO = {
    'SwarmUI': 'https://github.com/mcmonkeyprojects/SwarmUI'
}

SyS = get_ipython().system
CD = os.chdir

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARKED = SRC / 'marking.json'
TMP = Path('/tmp')

SRC.mkdir(parents=True, exist_ok=True)
iRON = os.environ

def SM_Script(WEBUI):
    return [
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}',
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}',
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}'
    ]

def CN_Script(WEBUI):
    return f'https://github.com/gutris1/segsmaker/raw/main/script/controlnet.py {WEBUI}/asd'

def Load_CSS():
    display(HTML(f'<style>{CSS.read_text()}</style>'))

def tmp_cleaning(v):
    for i in TMP.iterdir():
        if i.is_dir() and i != v:
            shutil.rmtree(i)
        elif i.is_file() and i != v:
            i.unlink()

def check_ffmpeg():
    i = get_ipython().getoutput('conda list ffmpeg')
    if not any('ffmpeg' in l for l in i):
        c = [
            ('mamba install -y ffmpeg curl', '\ninstalling ffmpeg...'),
            ('mamba install -y cuda-runtime=12.4.1', 'installing cuda-runtime=12.4.1...'),
            ('mamba install -y cudnn=9.2.1.18', 'installing cudnn=9.2.1.18...'),
            ('conda clean -y --all', None)
        ]

        for d, m in c:
            if m is not None:
                print(m)
            subprocess.run(shlex.split(d), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def marking(p, n, i):
    t = p / n
    if not t.exists():
        t.write_text(json.dumps({
            'ui': i,
            'launch_args': '',
            'zrok_token': '',
            'ngrok_token': '',
            'tunnel': ''
        }, indent=4))
    d = json.loads(t.read_text())
    d.update({'ui': i, 'launch_args': ''})
    t.write_text(json.dumps(d, indent=4))

def install_tunnel():
    bins = {
        'zrok': {
            'bin': HOME / '.zrok/bin/zrok',
            'url': 'https://github.com/openziti/zrok/releases/download/v1.0.6/zrok_1.0.6_linux_amd64.tar.gz'
        },
        'ngrok': {
            'bin': HOME / '.ngrok/bin/ngrok',
            'url': 'https://bin.ngrok.com/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz'
        }
    }

    for n, b in bins.items():
        binPath = b['bin']
        if binPath.exists(): binPath.unlink()

        url = b['url']
        name = Path(url).name
        binDir = binPath.parent

        binDir.mkdir(parents=True, exist_ok=True)

        SyS(f'curl -sLo {binDir}/{name} {url}')
        SyS(f'tar -xzf {binDir}/{name} -C {binDir} --wildcards *{n}')
        SyS(f'rm -f {binDir}/{name}')

        if str(binDir) not in iRON.get('PATH', ''): iRON['PATH'] += ':' + str(binDir)
        binPath.chmod(0o755)

def sym_link(U, M):
    configs = {
        'SwarmUI': {
            'sym': [
                f"rm -rf {M / 'Stable-Diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'controlnet'}",
                f"rm -rf {M / 'clip'} {M / 'unet'}"
            ],
            'links': [
                (TMP, HOME / 'tmp'),
                (TMP / 'ckpt', M / 'Stable-Diffusion/tmp_ckpt'),
                (TMP / 'lora', M / 'Lora/tmp_lora'),
                (TMP / 'controlnet', M / 'controlnet'),
                (TMP / 'clip', M / 'clip'),
                (TMP / 'unet', M / 'unet')
            ]
        }
    }

    cfg = configs.get(U)
    SyS(f"rm -rf {HOME / 'tmp'} {HOME / '.cache'}/*")
    [SyS(f'{cmd}') for cmd in cfg['sym']]
    [SyS(f'ln -s {src} {tg}') for src, tg in cfg['links']]

def webui_req(U, W, M):
    vnv = TMP / 'venv'
    tmp_cleaning(vnv)
    CD(W)

    M.mkdir(parents=True, exist_ok=True)
    for sub in ['Stable-Diffusion', 'Lora', 'Embeddings', 'VAE', 'upscale_models']:
        (M / sub).mkdir(parents=True, exist_ok=True)

    download(f'https://dot.net/v1/dotnet-install.sh {W}')
    dotnet = W / 'dotnet-install.sh'
    dotnet.chmod(0o755)
    SyS('bash ./dotnet-install.sh --channel 8.0')

    sym_link(U, M)

    scripts = SM_Script(W)
    scripts.append(CN_Script(W))

    u = M / 'upscale_models'
    upscalers = [
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x-UltraSharp.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x-AnimeSharp.pth {u}'
    ]

    for item in scripts + upscalers:
        download(item)

def installing_webui(U, W):
    M = W / 'Models'
    V = M / 'VAE'

    webui_req(U, W, M)
    install_tunnel()

    extras = [
        f'https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors'
    ]

    for i in extras:
        download(i)

def webui_install(ui):
    display(Image(filename=str(IMG)))

    if ui in REPO:
        WEBUI = HOME / ui
        repo = REPO[ui]

    say(f"<b>【{{red}} Installing {ui}{{d}} 】{{red}}</b>")
    clone(repo)

    marking(SRC, MARKED, ui)
    installing_webui(ui, WEBUI)
    tempe()

    get_ipython().run_line_magic('run', str(MRK))
    get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

    say('<b>【{red} Done{d} 】{red}</b>')
    CD(HOME)

def oppai(ui):
    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    current_ui = config.get('ui')
    WEBUI = HOME / ui if ui else None

    if WEBUI and WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            CD(WEBUI)
            SyS('git pull origin master')
            for y in SM_Script(WEBUI):
                download(y)
    else:
        if current_ui and current_ui != ui:
            webui = HOME / current_ui
            if webui.exists():
                print(f'{current_ui} is installed. uninstall it before switching to {ui}.')
                return

        webui_install(ui)

def Segsmaker_Setup():
    for cmd in [
        f'curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/SM/setup.css',
        f'curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/loading.png',
        f'curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/main/script/marking.py'
    ]:
        SyS(cmd)

    Load_CSS()
    oppai('SwarmUI')

CD(HOME)
Segsmaker_Setup()
