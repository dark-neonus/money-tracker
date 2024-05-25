

def run_gui():
    from modules.gui.window import GUI
    app = GUI()
    app.run()


def run_app():
    from modules.tracker_logic.application import Application
    app = Application()
    app.init_app()
    app.run()

if __name__ == "__main__":
    run_app()