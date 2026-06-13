from dotenv import load_dotenv
load_dotenv()
from gradio_ui import build_gradio_ui
from utils import load_settings, load_css


class App:
    def __init__(self):
        load_dotenv()
        load_settings()
        self.css = load_css()
        self.coach_graph = CoachGraph()


if __name__ == '__main__':
    app = App()
    ui = build_gradio_ui()
    ui.launch(inbrowser=False, css=app.css)
