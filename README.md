# ***⚠️ Disclaimer:***
#### - This script was created for experimental and educational purposes only.
#### - It is shared so others can use it for personal use on their own Telegram account or to learn about Telethon and Telegram API behavior.
#### - The author does not take responsibility for any misuse of this code.
#### - Use responsibly and comply with your local laws.

---

## 🚀 What This Script Does
##### ✅ Tracks online/offline/recently status of selected Telegram users.
##### ✅ Logs when these users start typing in private chats, groups, or supergroups.
##### ✅ Saves detailed logs with timestamps to log.txt for personal reference or experiments.

## ⚙️ Requirements
##### ✅ Python (3.10 or higher recommended (better the newest one))
##### ✅ Pip (usually comes with Python)

---

# **🛠️ Installation (Step-by-Step)**

## 1. Install Python:
##### Download and install Python from python.org.

##### *✅ Check “Add Python to PATH” during installation.*


## 2. Install Pip:
##### Open command prompt (cmd), and paste:
`python -m ensurepip --upgrade`


## 3. Install the required libraries:
##### In the same cmd paste:
`pip install telethon qrcode`

###### You can close cmd now

---

# **⚙️ Configuration**

## 1. Open this python code in any text editor (even usual Notepad).
`online-status-logger.py`

## 2. Replace the placeholders:
```python
api_id = "here"
api_hash = "here"
session_path = "my_session.session"
log_path = "log.txt"
target_usernames = ["@username1", "@username2", 123456789]
polling_interval = 10
reconnect_delay = 30
```
> **api_id and api_hash:** The API ID and Hash of your Telegram Account.
> **session_path:** Path or filename for your `.session` file (e.g., `"+1234567890.session"`).
> **log_path:** Path or filename where logs will be saved.
> **target_usernames:** Telegram `@usernames` or numeric user IDs of people you want to log.
> **polling_interval:** How often (in seconds) to actively check all users in a batch (`0` or `None` to disable).
> **reconnect_delay:** Seconds to wait before reconnecting if the connection drops.

### **❓ How to get api_id and api_hash?**
##### ***To run this script, you need your Telegram api_id and api_hash, which are easy to get:***
> **1. Go to https://my.telegram.org in your browser.**

> **2. Log in with your Telegram phone number.**
> **Telegram will send you a login code in your Telegram app for verification. (don't worry, it's an official Telegram Webside where you can actually delete your account but i'm hoping you don't need that, and be careful and don't delete it by mistake.)**

> **3. Click on “API Development Tools.”**

> **4. Fill out:**
> *App title: Any name (example: OnlineTracker)*
> *Short name: Any short name (example: trackerbot)*
> *You can leave everything else empty*

> **5. Click “Create application.”**

> **Now you will see your:**
`api_id`
`api_hash`
**Copy and paste them into the script**

---

# **🚀 Running the Script**

## **Standard Method**
##### It's better to run it in cmd, just:
##### - Right click `online-status-logger.py`
##### - Open with > Python

##### *✅ On first launch, it will request a verification code sent to your Telegram, and (if enabled) your 2FA password.*
##### *✅ It will create a `.session` file for future automatic logins.*

---

## **⚠️ Alternative Login Method (via QR Code)**
##### If the standard login method doesn't work (for example, Telegram doesn't send the login code), you can authorize your account via QR code using `session_create.py`:

### **1. Configure `session_create.py`:**
##### Open `session_create.py` in any text editor and fill in your credentials:
```python
API_ID = 000000  # Replace with your actual API ID (numbers only)
API_HASH = 'HERE_YOUR_API_HASH'  # Replace with your actual API Hash
SESSION_NAME = '+1XXXXXXXXXX'  # Replace with your phone number or desired session name
```
*(Make sure `qrcode` is installed — if not, run `pip install qrcode` in cmd.)*

### **2. Run `session_create.py` and scan the QR code:**
##### - Run `session_create.py` in cmd (`python session_create.py`). A QR code will appear in the terminal.
##### - Open Telegram on your phone -> **Settings -> Devices -> Add Device** (or **Link Desktop Device**).
##### - Scan the QR code from your screen within 2 minutes.
##### - If you have 2FA (cloud password) enabled, enter it in the terminal when prompted.

### **3. Connect the created `.session` file to the main script:**
##### - After successful login, a new file named `<SESSION_NAME>.session` (for example, `+1XXXXXXXXXX.session`) will appear in the **same folder**.
##### - Open `online-status-logger.py` and set `session_path` to that exact `.session` file name (or its full path), e.g.:
```python
session_path = "+1XXXXXXXXXX.session"
```
##### - Now you can run `online-status-logger.py` — it will log in automatically without asking for a code.

---

# **💾 Output**

## All logs are saved to log.txt in the same folder, including:
##### Status changes (Online, Offline, Recently, Deleted, Blocked)
##### Typing events in private and group chats
##### Timestamps and usernames

---

# **❓ Notes**
## ✅ Why Command Prompt and not VSCode?
##### > VSCode requires plugin setup and may require enabling execution in the correct working directory, making it more complex for beginners. Command Prompt is simpler and ensures the session file and log files are saved consistently.

##### > *And VSCode eats much more RAM*

## ✅ What if I close the script?
##### > The script will stop tracking immediately. You can rerun it anytime.

## ✅ Is it legal?
### Should be, if:
##### > *You are using your own account to view public information.*
##### > *You respect privacy, use responsibly, and do not share logs with anyone without consent.*
##### > *The code itself is not illegal, but misuse may be.*

---

# ❤️ About
##### This script was built with ChatGPT's and Gemini's assistance for fun and learning.

##### “It might not be perfect, but it works. Don't blame me, I'm just a noob.” – Author
