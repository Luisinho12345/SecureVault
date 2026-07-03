from app import SecureVaultApp
from database.database import create_database

create_database()

app = SecureVaultApp()
app.mainloop()