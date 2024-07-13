from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN", "7457499767:AAEw4LiCtTzYRjToo6Wo8IE5ZQZ3i_I3n5s")
OWNER_ID = list(map(int, getenv("OWNER_ID", "7091230649 6107581019").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://mohit18324:TxsMAm4VjmS0nQ74@cluster0.ynzyhrh.mongodb.net/?retryWrites=true&w=majority")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002050385725"))
