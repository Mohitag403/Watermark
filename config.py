from os import getenv


API_ID = int(getenv("API_ID", "18618422"))
API_HASH = getenv("API_HASH", "f165b1caec3cfa4df943fe1cbe82d22a")
BOT_TOKEN = getenv("BOT_TOKEN", "7072928279:AAE4qqJezs3sZVWmB1htMTI7QGBI1cbLgYI")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6050277919 2112898623 5753557653 6429744141 5890592765 6321150151 6807247768").split()))
OWNER_ID = "6050277919"
MONGO_DB_URI = "mongodb+srv://mohitag24082006:yox8Q1a9P5aLcAzK@cluster0.yafxbo4.mongodb.net/?retryWrites=true&w=majority"
