from database.database import create_database
from ui.splash import SplashScreen
from app import SecureVaultApp

create_database()


def launch_main_app():
    app = SecureVaultApp()
    app.mainloop()


splash = SplashScreen(on_finish=launch_main_app)
splash.mainloop()
