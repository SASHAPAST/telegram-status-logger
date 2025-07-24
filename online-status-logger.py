from telethon import TelegramClient, events
from telethon.tl.types import (
    UpdateUserStatus, UpdateUserTyping, UpdateChatUserTyping, UpdateChannelUserTyping,
    UserStatusOnline, UserStatusOffline, UserStatusRecently
)
import datetime
import asyncio

# Configuration
api_id = "PLACE YOUR API ID HERE"
api_hash = "PLACE YOUR API HASH HERE"
phone_number = "PLACE YOUR PHONE NUMBER HERE"
target_usernames = ["@username1", "@username2"]


session_path = f"{phone_number}.session"
log_path = "log.txt" # just a name of the log file, you can change it if you want

client = TelegramClient(session_path, api_id, api_hash)
target_ids = {}
previous_statuses = {}

# Just logs when the script starts
log_entry = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] ✅ Scrypt has been started.\n"
with open(log_path, "a", encoding="utf-8") as file:
    file.write(log_entry)

# Function to convert status objects to text representation
def status_to_text(status_obj):
    if isinstance(status_obj, UserStatusOnline):
        return f"🟢 Online"
    elif isinstance(status_obj, UserStatusOffline):
        return f"🔴 Offline"
    elif isinstance(status_obj, UserStatusRecently):
        return f"🟡 Unknown, by me: {getattr(status_obj, 'by_me', 'N/A')}"
    elif status_obj is None:
        return "🟡 Unknown (NoneType)"
    else:
        return f"🟡 Unknown ({type(status_obj).__name__})"

# Function to log the status of a user
def log_status(name, real_status_text, real_status_obj, incoming_text, incoming_obj):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_entry = (
        f"[{now}] {name} - {real_status_text}, {real_status_obj}; "
        f"incoming: {incoming_text}, {incoming_obj}\n"
    )
    print(log_entry.strip())
    with open(log_path, "a", encoding="utf-8") as file:
        file.write(log_entry)

# Registering the event handler for status updates
@client.on(events.Raw)
async def status_handler(event):
    if isinstance(event, UpdateUserStatus):
        if event.user_id not in target_ids:
            return

        entity = await client.get_entity(event.user_id)
        status = event.status

        full_name = entity.first_name
        if entity.last_name:
            full_name += f" {entity.last_name}"

        # The status that came in
        incoming_text = status_to_text(status)

        # Get the current status from the live entity
        try:
            live_entity = await client.get_entity(event.user_id)
            real_status_obj = getattr(live_entity, 'status', None)
        except Exception as e:
            real_status_obj = None

        real_text = status_to_text(real_status_obj)

        # Create a unique signature for the status
        status_signature = f"{type(status).__name__}_{type(real_status_obj).__name__}"
        prev = previous_statuses.get(event.user_id)
        
        # If the status has changed or the incoming text is different, log it
        if prev != status_signature or incoming_text != real_text:
            log_status(
                full_name,
                real_text,
                real_status_obj,
                incoming_text,
                status
            )
            previous_statuses[event.user_id] = status_signature

    # Handle typing events in private chats
    elif isinstance(event, UpdateUserTyping):
        if event.user_id not in target_ids:
            return

        entity = await client.get_entity(event.user_id)
        full_name = entity.first_name
        if entity.last_name:
            full_name += f" {entity.last_name}"

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{now}] {full_name} - ✏️ Typing in private chat, {event.action}\n"
        print(log_entry.strip())
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(log_entry)

    # Handle typing events in group chats
    elif isinstance(event, UpdateChatUserTyping):
        if event.user_id not in target_ids:
            return

        chat = await client.get_entity(event.chat_id)
        entity = await client.get_entity(event.user_id)
        full_name = entity.first_name
        if entity.last_name:
            full_name += f" {entity.last_name}"

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{now}] {full_name} - ✏️ Typing in group: {chat.title}, {event.action}\n"
        print(log_entry.strip())
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(log_entry)

    # Handle typing events in supergroups or channels (wait, is there any meaning in typing in channels? i don't think if it's possible to see it)
    elif isinstance(event, UpdateChannelUserTyping):
        if not hasattr(event.from_id, 'user_id'):
            return

        if event.from_id.user_id not in target_ids:
            return

        channel = await client.get_entity(event.channel_id)
        entity = await client.get_entity(event.from_id.user_id)
        full_name = entity.first_name
        if entity.last_name:
            full_name += f" {entity.last_name}"

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{now}] {full_name} - ✏️ Typing in channel/group: {channel.title}, {event.action}\n"
        print(log_entry.strip())
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(log_entry)

async def log_initial_statuses():
    for username in target_usernames:
        entity = await client.get_entity(username)
        target_ids[entity.id] = username

        status = entity.status
        full_name = entity.first_name
        if entity.last_name:
            full_name += f" {entity.last_name}"

        current_status = status_to_text(status)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{now}] {full_name} - {current_status} - {status}\n"
        print(log_entry.strip())
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(log_entry)

    print("-----")

async def main():
    await client.start()
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] ✅ Скрипт запущено")
    await log_initial_statuses()
    await client.run_until_disconnected()

asyncio.run(main())

# just for you to know, it was mostly created with ChatGPT (thank you brother) and i'm not sure if it's written correctly, don't blame me, it works. i'm noob tho