from os import getenv


API_ID = int(getenv("API_ID", "18618422"))
API_HASH = getenv("API_HASH", "f165b1caec3cfa4df943fe1cbe82d22a")
BOT_TOKEN = getenv("BOT_TOKEN", "6968442211:AAHaOay5WJH_wsycGKYYewvbtrr83HdUOBw")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6050277919 5890592765 5809339058 2112898623").split()))
