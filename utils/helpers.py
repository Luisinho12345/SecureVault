import os
import shutil
from datetime import datetime

from utils.constants import BACKUP_DIR, DATABASE_NAME


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def format_datetime(dt=None):
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def create_backup():

    ensure_dir(BACKUP_DIR)

    if not os.path.exists(DATABASE_NAME):
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"securevault_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    shutil.copy2(DATABASE_NAME, backup_path)

    return backup_path


def list_backups():

    ensure_dir(BACKUP_DIR)

    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
    files.sort(reverse=True)

    return files


def restore_backup(backup_filename):

    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    if not os.path.exists(backup_path):
        return False

    shutil.copy2(backup_path, DATABASE_NAME)

    return True
