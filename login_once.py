from pyrogram import Client

api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"

app = Client("my_session", api_id=api_id, api_hash=api_hash)

app.start()
print("Logged in as:", app.get_me().first_name)
app.stop()
