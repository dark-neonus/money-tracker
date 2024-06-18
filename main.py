

if __name__ == "__main__":
    from modules.tracker_logic.application import Application
    app = Application()
    app.init_app()
    app.run()