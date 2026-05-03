import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from IPython import get_ipython

def launch_interface():

    process_out = widgets.Output()
    css_url = "https://raw.githubusercontent.com/gutris1/segsmaker/refs/heads/main/script/SM/setup.css"
    display(HTML(f'<link rel="stylesheet" type="text/css" href="{css_url}">'))

    swarm_img = "https://raw.githubusercontent.com/SFcrypt/SwarmUI/main/Github/Cover/003219.png"
    forge_img = "https://raw.githubusercontent.com/SFcrypt/SwarmUI/main/Github/Cover/092918.png"

    display(HTML(f"""
    <style>
    .setup-box {{
        padding: 10px;
        border-radius: 16px;
        background: #000000;
        overflow: hidden;
    }}

    .custom-btn {{
        width: 100%;
        height: 100%;
        border: 2px solid #111 !important;
        border-radius: 14px;
        background-size: cover;
        background-position: center;
        color: white !important;
        font-size: 18px;
        font-weight: 700;
        text-transform: lowercase;
        text-shadow: 0 2px 6px rgba(0,0,0,.95);
        padding-top: 10px;
        align-items: flex-start;
        justify-content: center;
        box-shadow: inset 0 0 0 1px #222;
        transition: all .15s ease-in-out;
        overflow: hidden;
    }}

    .custom-btn:hover {{
        border-color: #00aaff !important;
        box-shadow: 0 0 0 2px #00aaff;
        transform: translateY(-2px);
    }}

    .swarm {{
        background-image: url('{swarm_img}');
    }}

    .forge {{
        background-image: url('{forge_img}');
    }}

    .widget-button {{
        min-width: 0 !important;
    }}

    .widget-box, .output_wrapper, .output {{
        overflow: hidden !important;
        max-height: none !important;
    }}
    </style>
    """))

    def run_swarm(_):
        panel.layout.display = "none"
        with process_out:
            clear_output()
            ip = get_ipython()
            if ip:
                ip.run_line_magic("run", "~/.swarmui/Updater.py")

    def run_forge(_):
        panel.layout.display = "none"
        with process_out:
            clear_output()
            ip = get_ipython()
            if ip:
                ip.run_line_magic("run", "~/.swarmui/Forge.py")

    btn_swarm = widgets.Button(description="swarmui")
    btn_forge = widgets.Button(description="forge")

    for btn, clase in [
        (btn_swarm, "swarm"),
        (btn_forge, "forge")]:
        btn.add_class("custom-btn")
        btn.add_class(clase)

    btn_swarm.on_click(run_swarm)
    btn_forge.on_click(run_forge)

    row = widgets.HBox(
        [btn_swarm, btn_forge],
        layout=widgets.Layout(
            width="100%",
            height="240px",
            gap="10px"))

    global panel
    panel = widgets.VBox(
        [row],
        layout=widgets.Layout(width="100%"))

    panel.add_class("setup-box")

    display(panel, process_out)


if __name__ == "__main__":
    launch_interface()
