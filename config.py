from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN", "6751484391:AAG4M0ab4BjhUPEyebwdFsz0hMjj0f_nESY")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6280048819 6691393517 6050277919").split()))
