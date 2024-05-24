

def run_gui():
    from modules.gui.window import GUIApplication
    app = GUIApplication()
    app.run()

def run_app():
    from modules.tracker_logic.application import Application
    app = Application()

if __name__ == "__main__":
    run_gui()