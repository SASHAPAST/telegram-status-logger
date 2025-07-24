# ***⚠️ Disclaimer:***
#### > This script was created for experimental and educational purposes only.
#### > It is shared so others can use it for personal use on their own Telegram account or to learn about Telethon and Telegram API behavior.
#### > The author does not take responsibility for any misuse of this code.
#### > Use responsibly and comply with your local laws.

---

## 🚀 What This Script Does
##### ✅ Tracks online/offline/recently status of selected Telegram users.
##### ✅ Logs when these users start typing in private chats, groups, or supergroups.
##### ✅ Saves detailed logs with timestamps to log.txt for personal reference or experiments.

## ⚙️ Requirements
##### ✅ Python (3.40 or higher recommended (better the newest one))
##### ✅ Pip (usually comes with Python)

---

# **🛠️ Installation (Step-by-Step)**

## 1. Install Python:
##### Download and install Python from python.org.

##### *✅ Check “Add Python to PATH” during installation.*


## 2. Install Pip:
##### Open command prompt (cmd), and paste:
`python -m ensurepip --upgrade`


## 3. Install the required library:
##### In the same cmd paste
`pip install telethon`

###### You can close cmd now

---

# **⚙️ Configuration**

## 1. Open this python code in any text editor (even usual Notepad).
`online-status-logger.py`

## 2. Replace the placeholders:
```
api_id = "here"
api_hash = "here"
phone_number = "+1"
target_usernames = ["@username1", "@username2"]
```
> **api_id and api_hash:** The API ID and Hash of your Telegram Account.
> **phone_number:** Your phone number in international format (+1...). Must be on the same account at where you've got your API Hash and ID.
> **target_usernames:** Telegram usernames of people you want to log.

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

## **Now, you almost made it, congrats!**
##### It's better to run it in cmd, just:
##### - Right click `online-status-logger.py`
##### - Open with > Python

##### *✅ On first launch, it will request a verification code sent to your Telegram, and (if enabled) your 2FA password.*
##### *✅ It will create a session file for future automatic logins.*

---

# **💾 Output**

## All logs are saved to log.txt in the same folder, including:
##### Status changes (Online, Offline, Recently)
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
##### This script was built with ChatGPT's assistance for fun and learning.

##### “It might not be perfect, but it works. Don't blame me, I'm just a noob.” – Author
