# main.py

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from IPython import get_ipython
import updater

def launch_interface():

    process_out = widgets.Output()

    css_url = "https://raw.githubusercontent.com/gutris1/segsmaker/refs/heads/main/script/SM/setup.css"
    display(HTML(f'<link rel="stylesheet" type="text/css" href="{css_url}">'))

    instalar_img = "https://raw.githubusercontent.com/SFcrypt/ColabUI/main/Notebook/00008-0603.png"
    actualizar_img = "https://raw.githubusercontent.com/SFcrypt/ColabUI/main/Notebook/00005-4209.png"
    desinstalar_img = "https://raw.githubusercontent.com/SFcrypt/ColabUI/main/Notebook/00002-1225.png"

    display(HTML(f"""
    <style>
    .setup-box {{
        padding: 10px;
        border-radius: 16px;
        background: #000000;
    }}

    .custom-btn {{
        width: 100%;
        height: 100%;
        border: 2px solid #111 !important;
        border-radius: 14px;
        background-size: cover;
        background-position: center;
        color: white !important;
        font-size: 14px;
        font-weight: 700;
        text-transform: lowercase;
        text-shadow: 0 2px 6px rgba(0,0,0,.95);
        padding-top: 8px;
        align-items: flex-start;
        justify-content: center;
        box-shadow: inset 0 0 0 1px #222;
        transition: all .15s ease-in-out;
    }}

    .custom-btn:hover {{
        border-color: #00aaff !important;
        box-shadow: 0 0 0 2px #00aaff;
        transform: translateY(-2px);
    }}

    .instalar {{
        background-image: url('{instalar_img}');
    }}

    .actualizar {{
        background-image: url('{actualizar_img}');
    }}

    .desinstalar {{
        background-image: url('{desinstalar_img}');
    }}

    .widget-button {{
        min-width: 0 !important;
    }}
    </style>
    """))

    def run_instalar(_):
        panel.layout.display = "none"
        with process_out:
            clear_output()
            ip = get_ipython()
            if ip:
                ip.run_line_magic("run", "~/.conda/setup.py")

    def run_actualizar(_):
        panel.layout.display = "none"
        with process_out:
            clear_output()
            updater.run_update()

    def run_desinstalar(_):
        panel.layout.display = "none"
        with process_out:
            clear_output()
            ip = get_ipython()
            if ip:
                ip.run_line_magic("uninstall_webui", "")

    btn_instalar = widgets.Button(description="instalar")
    btn_actualizar = widgets.Button(description="actualizar")
    btn_desinstalar = widgets.Button(description="desinstalar")

    for btn, clase in [
        (btn_instalar, "instalar"),
        (btn_actualizar, "actualizar"),
        (btn_desinstalar, "desinstalar")
    ]:
        btn.add_class("custom-btn")
        btn.add_class(clase)

    btn_instalar.on_click(run_instalar)
    btn_actualizar.on_click(run_actualizar)
    btn_desinstalar.on_click(run_desinstalar)

    row = widgets.HBox(
        [btn_instalar, btn_actualizar, btn_desinstalar],
        layout=widgets.Layout(
            width="100%",
            height="255px",
            gap="10px"
        )
    )

    global panel
    panel = widgets.VBox(
        [row],
        layout=widgets.Layout(width="100%")
    )

    panel.add_class("setup-box")

    display(panel, process_out)

launch_interface()