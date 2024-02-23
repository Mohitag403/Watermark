from os import getenv

API_ID = int(getenv("API_ID", "18618422"))
API_HASH = getenv("API_HASH", "f165b1caec3cfa4df943fe1cbe82d22a")
BOT_TOKEN = getenv("BOT_TOKEN", "6532280623:AAHOtJg0sZf1s_zRGrbQtSsT3qOTbbyKgms")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6050277919 2112898623 5753557653 6429744141 5890592765 6321150151 6807247768").split()))
OWNER_ID = int(getenv("OWNER_ID", "6050277919"))
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://mohit18324:TxsMAm4VjmS0nQ74@cluster0.ynzyhrh.mongodb.net/?retryWrites=true&w=majority")
