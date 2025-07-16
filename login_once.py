from pyrogram import Client

api_id = 28607488
api_hash = "bc94e7a874a66b95e28cfbabf8c29948"

app = Client("my_session", api_id=api_id, api_hash=api_hash)

app.start()
print("Logged in as:", app.get_me().first_name)
app.stop()
