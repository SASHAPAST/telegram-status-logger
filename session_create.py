import asyncio
from getpass import getpass
import qrcode
from telethon import TelegramClient, errors

# === Your Data ===
API_ID = 000000  # Replace with your actual API ID
API_HASH = 'HERE_YOUR_API_HASH'  # Replace with your actual API Hash
SESSION_NAME = '+1XXXXXXXXXX'  # Replace with your phone number or desired session name

def print_qr(url: str) -> None:
    """Draws a QR code in the terminal."""
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

async def main() -> None:
    print("🚀 Initializing client...")
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()

    if await client.is_user_authorized():
        print("✅ You are already authorized! The script can be used.")
    else:
        print("🔄 Requesting QR code from Telegram servers...")
        try:
            # Create a QR login request
            qr_login = await client.qr_login()
            
            print("\n📱 INSTRUCTIONS:")
            print("1. Open Telegram on your phone.")
            print("2. Go to Settings -> Devices -> Add Device.")
            print("3. Scan this QR code from your monitor:\n")
            
            # Putting the QR code in the terminal
            print_qr(qr_login.url)
            
            # Script freezes here until the user scans the QR code and confirms the login on their phone
            await qr_login.wait(timeout=120)
            print("\n🎉 Success! The server has confirmed the login.")

        except errors.SessionPasswordNeededError:
            # If the account has 2FA enabled, we need to ask for the password
            print("\n🔒 Security: 2FA (cloud password) is enabled.")
            password = getpass("Enter your 2FA password: ")
            await client.sign_in(password=password)
            print("🎉 Password accepted! Authorization completed.")
            
        except asyncio.TimeoutError:
            print("\n❌ Time expired (2 minutes elapsed). You didn't scan the code in time.")

    # Check the session and display the user information
    me = await client.get_me()
    print(f"\n🔥 SESSION CREATED! Login completed as: {me.first_name} (@{me.username})")
    print(f"Working file saved: '{SESSION_NAME}.session'")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())