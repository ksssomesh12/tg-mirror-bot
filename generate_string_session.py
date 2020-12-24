from pyrogram import Client

API_ID = int(input("Enter API ID: "))
API_HASH = input("Enter API HASH: ")
with Client(':memory:', api_id=API_ID, api_hash=API_HASH) as app:
    print(app.export_session_string())
