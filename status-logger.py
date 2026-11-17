from telethon import TelegramClient, events, utils
from telethon.tl.types import (
    UpdateUserStatus, UpdateUserTyping, UpdateChatUserTyping, UpdateChannelUserTyping,
    UserStatusOnline, UserStatusOffline, UserStatusRecently
)
from telethon.tl.functions.users import GetUsersRequest
import datetime
import asyncio
import logging
import traceback

# ==========================================
# CONFIGURATION (Edit these settings first)
# ==========================================

# Your Telegram API credentials (get them at https://my.telegram.org -> API development tools)
api_id = "PUT YOUR API ID HERE"
api_hash = "PUT YOUR API HASH HERE"

# Full path where the Telegram session file will be saved (keeps you logged in between restarts)
session_path = r"SESSION PATH\EXAMPLE\+1XXXXXXXXXX.session"

# Full path to the output text file where all status changes and typing events will be recorded
log_path = r"LOG PATH\EXAMPLE\log.txt"

# List of users to track. Supports "@username", numeric user IDs (int), or numeric IDs as strings
target_usernames = ["@username1", "@username2", 1234567890]

# How often (in seconds) to actively poll all users in a batch to catch missed status updates.
# Set to 0 or None to disable active polling and rely only on real-time push events.
polling_interval = 10

# How many seconds to wait before reconnecting if the connection drops or an error occurs
reconnect_delay = 30

# ==================== Global Variables (Do Not Edit) ====================

target_ids = {}           # user_id -> raw target identifier
last_status = {}          # user_id -> simplified state ("Online", "Offline", "None", "Other")
target_entities = {}      # user_id -> cached User entity
target_input_users = {}   # user_id -> InputUser (used for batch GetUsersRequest calls)
peer_entities = {}        # chat/channel_id -> cached Chat/Channel entity


def write_log(text):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    entry = f"[{now}] {text}\n"
    print(entry.strip())
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def write_separator():
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("-----\n")
    print("-----")


class TelethonLogHandler(logging.Handler):
    """Forwards Telethon warnings/errors to the log file while suppressing INFO noise."""
    def emit(self, record):
        try:
            if record.levelno < logging.WARNING:
                return
            msg = self.format(record)
            write_log(f"[telethon] {msg}")
        except Exception:
            pass


tele_logger = logging.getLogger("telethon")
if not any(isinstance(h, TelethonLogHandler) for h in tele_logger.handlers):
    tele_handler = TelethonLogHandler()
    tele_handler.setLevel(logging.INFO)
    tele_logger.addHandler(tele_handler)
    tele_logger.setLevel(logging.INFO)

write_log("✅ Script started")


def status_to_text(status_obj, entity=None):
    if isinstance(status_obj, UserStatusOnline):
        return "🟢 Online"
    elif isinstance(status_obj, UserStatusOffline):
        return "🔴 Offline"
    elif isinstance(status_obj, UserStatusRecently):
        return "🟡 Recently (You or User privacy settings)"
    elif entity and getattr(entity, 'deleted', False):
        return "💀 Deleted"
    elif status_obj is None:
        return "🟣 Blocked"
    else:
        return f"⚪ Unknown ({type(status_obj).__name__})"


def simplify_status(status_obj):
    # Separate NoneType (blocked/restricted) from Other (e.g., UserStatusRecently) to prevent false transitions
    if isinstance(status_obj, UserStatusOnline):
        return "Online"
    elif isinstance(status_obj, UserStatusOffline):
        return "Offline"
    elif status_obj is None:
        return "None"
    else:
        return "Other"


def get_safe_name(entity):
    if not entity:
        return "Unknown Entity"
    if getattr(entity, 'deleted', False):
        return f"👻 DELETED (ID: {entity.id})"

    first = entity.first_name or ""
    last = entity.last_name or ""
    full_name = (first + " " + last).strip()

    if not full_name:
        return f"No Name User (ID: {entity.id})"
    return full_name


async def get_cached_entity(client, cache, entity_id):
    entity = cache.get(entity_id)
    if entity is None:
        entity = await client.get_entity(entity_id)
        cache[entity_id] = entity
    return entity


async def handle_status_change(user_id, entity, status_obj, prefix=""):
    current_simple = simplify_status(status_obj)
    prev_simple = last_status.get(user_id)

    if current_simple == prev_simple:
        return

    last_status[user_id] = current_simple
    full_name = get_safe_name(entity)
    status_text = status_to_text(status_obj, entity)

    write_log(f"{full_name} - {status_text}, {status_obj} {prefix}")


def register_event_handlers(client):
    @client.on(events.Raw)
    async def raw_handler(event):
        try:
            if isinstance(event, UpdateUserStatus):
                if event.user_id not in target_ids:
                    return
                entity = await get_cached_entity(client, target_entities, event.user_id)
                # Use the payload status directly to avoid redundant get_entity RPC calls
                real_status_obj = event.status
                entity.status = real_status_obj
                await handle_status_change(event.user_id, entity, real_status_obj)

            elif isinstance(event, UpdateUserTyping):
                if event.user_id not in target_ids:
                    return
                entity = await get_cached_entity(client, target_entities, event.user_id)
                full_name = get_safe_name(entity)
                write_log(f"{full_name} - ✏️ Typing in private chat, {event.action}")

            elif isinstance(event, UpdateChatUserTyping):
                # Legacy basic groups populate user_id; some constructors expose from_id.user_id instead
                u_id = getattr(event, 'user_id', None)
                if not u_id and hasattr(event, 'from_id'):
                    u_id = getattr(event.from_id, 'user_id', None)

                if not u_id or u_id not in target_ids:
                    return

                chat = await get_cached_entity(client, peer_entities, event.chat_id)
                entity = await get_cached_entity(client, target_entities, u_id)
                full_name = get_safe_name(entity)
                write_log(f"{full_name} - ✏️ Typing in group: {chat.title}, {event.action}")

            elif isinstance(event, UpdateChannelUserTyping):
                if not hasattr(event.from_id, 'user_id'):
                    return
                if event.from_id.user_id not in target_ids:
                    return
                channel = await get_cached_entity(client, peer_entities, event.channel_id)
                entity = await get_cached_entity(client, target_entities, event.from_id.user_id)
                full_name = get_safe_name(entity)
                write_log(f"{full_name} - ✏️ Typing in channel/group: {channel.title}, {event.action}")
        except Exception as e:
            write_log(f"⚠️ Error in event handler: {type(e).__name__}: {e}")
            write_log(traceback.format_exc())


async def log_initial_statuses(client):
    target_ids.clear()
    last_status.clear()
    target_entities.clear()
    target_input_users.clear()
    peer_entities.clear()

    for entry in target_usernames:
        # Coerce digit-only strings to int so Telethon resolves them as peer IDs rather than usernames
        target = int(entry) if isinstance(entry, str) and entry.lstrip('-').isdigit() else entry

        try:
            entity = await client.get_entity(target)
        except ValueError as e:
            write_log(f"⚠️ User not found: {entry} ({type(e).__name__})")
            continue

        target_ids[entity.id] = str(entry)
        target_entities[entity.id] = entity
        target_input_users[entity.id] = utils.get_input_user(entity)
        status = getattr(entity, 'status', None)
        full_name = get_safe_name(entity)
        last_status[entity.id] = simplify_status(status)
        write_log(f"{full_name} - {status_to_text(status)} - {status}")
    write_separator()


async def polling_loop(client, stop_event: asyncio.Event):
    """Batches all tracked users into a single GetUsersRequest to catch missed push updates."""
    try:
        while not stop_event.is_set():
            if not client.is_connected():
                await asyncio.sleep(1)
                continue

            if not target_ids:
                await asyncio.sleep(1)
                continue

            try:
                all_users = list(target_input_users.values())
                if not all_users:
                    await asyncio.sleep(1)
                    continue

                result = await client(GetUsersRequest(id=all_users))

                for entity in result:
                    if stop_event.is_set():
                        break

                    target_entities[entity.id] = entity
                    status = getattr(entity, 'status', None)
                    await handle_status_change(entity.id, entity, status, prefix="; [DETAINED]")

            except Exception as e:
                write_log(f"⚠️ Error in batch polling_loop: {type(e).__name__}: {e}")
                write_log(traceback.format_exc())
                await asyncio.sleep(5)

            await asyncio.sleep(polling_interval if polling_interval else 1)

    except asyncio.CancelledError:
        return
    except Exception as e:
        write_log(f"⚠️ Unexpected error in polling_loop: {type(e).__name__}: {e}")
        write_log(traceback.format_exc())


async def run_client_forever():
    # auto_reconnect=False delegates lifecycle management to this supervisor loop for clean task teardown
    while True:
        client = TelegramClient(session_path, api_id, api_hash, auto_reconnect=False)
        stop_event = asyncio.Event()
        polling_task = None
        try:
            await client.start()
            write_log("✅ Connection established")

            register_event_handlers(client)

            try:
                await log_initial_statuses(client)
            except Exception as e:
                write_log(f"⚠️ Error in log_initial_statuses: {type(e).__name__}: {e}")
                write_log(traceback.format_exc())

            if polling_interval and polling_interval > 0:
                polling_task = asyncio.create_task(polling_loop(client, stop_event))

            await client.run_until_disconnected()

            write_log("⚠️ client.run_until_disconnected exited unexpectedly. Restarting...")
        except Exception as e:
            write_log(f"⚠️ Client error: {type(e).__name__}: {e}")
            write_log(traceback.format_exc())
            write_log(f"🔁 Reconnecting in {reconnect_delay} seconds...")
            stop_event.set()
            if polling_task:
                polling_task.cancel()
                try:
                    await polling_task
                except asyncio.CancelledError:
                    pass
            try:
                if client.is_connected():
                    await client.disconnect()
            except Exception:
                pass
            await asyncio.sleep(reconnect_delay)
        finally:
            stop_event.set()
            if polling_task:
                polling_task.cancel()
                try:
                    await polling_task
                except asyncio.CancelledError:
                    pass
            try:
                if client.is_connected():
                    await client.disconnect()
            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(run_client_forever())
