# 🎂 Birthday Reminder Telegram Bot

## 🎯 Objective

Never forget a birthday again! This n8n agent checks your birthday list every morning and sends you a Telegram message if someone's birthday is today.

> **The big idea:** You maintain a simple Excel file with names and birthdays in Google Drive. Every morning at 8 AM the agent reads the list, checks today's date, and only alerts you if there's a match. No birthday = no message. Someone's birthday = instant Telegram alert!

This agent teaches students how to:
- Read data from a **Google Drive Excel file**
- Use a **Code node** to compare dates
- Use an **IF node** to make decisions (only send if birthday matches)
- Send alerts to **Telegram**
- Chain multiple nodes into a real-world useful tool

---

## 🏗️ How It Works

```
[ Schedule Trigger ]
    Fires every day at 8:00 AM
        ↓
[ Google Drive Node ]
    Downloads your birthday Excel file
        ↓
[ Extract from File Node ]
    Reads each row (name + date of birth)
        ↓
[ Code Node ]
    Checks if today's date matches any birthday
    Builds the alert message
        ↓
[ IF Node ]
    YES — someone has a birthday today → continue
    NO — no birthdays today → stop, do nothing
        ↓
[ HTTP Request → Telegram ]
    Sends birthday alert to your Telegram chat
```

**Total nodes:** 6  
**Trigger:** Scheduled — every day at 8 AM (`0 8 * * *`)  
**Smart behaviour:** Only sends a message when there is actually a birthday — no daily spam!

---

## 📱 Sample Telegram Messages

**Single birthday:**
```
🎂 Birthday Reminder!
📅 Wednesday, 22 July 2026

🎉 Today is Rahul Sharma's birthday!

Don't forget to wish them! 🥳
```

**Multiple birthdays on same day:**
```
🎂 Birthday Reminder!
📅 Wednesday, 22 July 2026

🎉 Multiple birthdays today!

• Rahul Sharma
• Priya Patel

Don't forget to wish them all! 🥳
```

**No birthdays today:** *(No message sent — silence is the signal!)*

---

## 📋 What You Need Before Starting

| What | Where to get it | Time needed |
|------|----------------|-------------|
| Docker Desktop | https://docker.com/products/docker-desktop | 5 min |
| Google Account (Drive) | Already have one | — |
| Google OAuth Credentials | https://console.cloud.google.com | 10 min |
| Birthday Excel file (.xlsx) | Create it yourself | 5 min |
| Telegram app | Your phone's app store | 2 min |
| Telegram Bot Token | @BotFather on Telegram | 2 min |
| Telegram Chat ID | @userinfobot or getUpdates URL | 1 min |

---

## 🚀 Step-by-Step Setup

---

### STEP 1 — Install Docker and Run n8n

If you already have n8n running, skip to Step 2.

**Install Docker Desktop:**
1. Go to: **https://www.docker.com/products/docker-desktop**
2. Download for your OS (Mac or Windows)
3. Install and open — wait for **"Engine running"** at the bottom left

**Run n8n in Terminal (Mac) or Command Prompt (Windows):**

```bash
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

Wait 30 seconds then open: **http://localhost:5678**

Create a local account when prompted — stays 100% on your machine.

> ✅ n8n is ready when you see the Overview dashboard

---

### STEP 2 — Create Your Birthday Excel File

1. Open **Microsoft Excel** or **Google Sheets**
2. Create two columns with these exact headers in Row 1:

| Full Name | Date of Birth |
|-----------|--------------|
| Rahul Sharma | 22/07/1990 |
| Priya Patel | 15/08/1995 |
| Dinesh Wadhwani | 03/01/1985 |
| Anita Desai | 22/07/2000 |

> ⚠️ Column headers must be exactly `Full Name` and `Date of Birth`

> 💡 Date format can be DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD — the agent handles all formats

> 💡 To test immediately — add today's date for one person so you get an alert right away!

3. Save as `.xlsx` (Excel format)
4. Upload to **Google Drive**:
   - Go to https://drive.google.com
   - Click **"+ New"** → **"File upload"**
   - Select your `.xlsx` file

> ✅ Your birthday file is on Google Drive

---

### STEP 3 — Set Up Google OAuth (for Google Drive)

#### Part A — Create a Google Cloud Project
1. Go to: **https://console.cloud.google.com**
2. Click the project dropdown (top left) → **"New Project"**
3. Name it: `n8n-birthday-bot`
4. Click **Create**

#### Part B — Enable Google Drive API
1. In the search bar, type: `Google Drive API`
2. Click **"Google Drive API"** → click **"Enable"**

#### Part C — Configure OAuth Consent Screen
1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Fill in App name and support email
3. Click through all steps
4. On **Audience**, make sure **External** is selected
5. Go to **Audience** in left sidebar → **"+ Add users"** → add your Gmail → **Save**

#### Part D — Create OAuth Client ID
1. Go to **"Clients"** or **"Credentials"** → **"+ Create Credentials"** → **"OAuth Client ID"**
2. Application type: **Web application**
3. Name: `n8n local`
4. Authorised redirect URI:
   ```
   http://localhost:5678/rest/oauth2-credential/callback
   ```
5. Click **Create** → copy your **Client ID** and **Client Secret**

> ✅ You have your Google OAuth credentials

---

### STEP 4 — Create Your Telegram Bot

1. Open **Telegram** → search **@BotFather**
2. Click **Start** → send `/newbot`
3. Name: e.g. `My Birthday Bot`
4. Username: e.g. `mybirthday_yourname_bot` (must end in "bot")
5. Copy the **Bot Token** BotFather sends you
6. Find your bot by username → click **Start** (important!)

> ✅ Telegram bot is ready

---

### STEP 5 — Get Your Telegram Chat ID

#### Method 1 — @userinfobot
1. Search **@userinfobot** on Telegram → send any message
2. Copy the **Id** number it replies with

#### Method 2 — getUpdates URL (if Method 1 fails)
1. Make sure you sent a message to your bot (Step 4)
2. Open in browser (replace with your token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Find `"chat":{"id":` — copy the number after it

> ⚠️ If result is empty `[]` — send a message to your bot first, then refresh

> ✅ You have your Chat ID

---

### STEP 6 — Import the Workflow

1. In n8n (`http://localhost:5678`), click **`+`** → **"New Workflow"**
2. Click **`...`** (top right) → **"Import from file"**
3. Select: `birthday_reminder_telegram.json`

> ✅ You should see 6 nodes connected in a pipeline

---

### STEP 7 — Connect Google Drive

1. Click the **"Download Birthdays (Google Drive)"** node
2. Click the **✏️ edit icon** next to Credential
3. Paste your **Client ID** and **Client Secret**
4. Click **"Sign in with Google"** → approve
5. You should see **"Account connected"** ✅
6. In the **File** field:
   - Switch from "By ID" to **"From List"**
   - Select your birthday `.xlsx` file from the dropdown

---

### STEP 8 — Configure the Telegram Node

1. Click the **"Send Birthday Alert"** node
2. In the **URL** field — replace `PUT_YOUR_BOT_TOKEN_HERE` with your Bot Token:
   ```
   https://api.telegram.org/bot123456789:AAFxxxxxxxxxx/sendMessage
   ```
3. In the **JSON Body** field — replace `PUT_YOUR_CHAT_ID_HERE` with your Chat ID (keep single quotes):
   ```
   '1784026614'
   ```

---

### STEP 9 — Test It!

> 💡 **Testing tip:** Add today's date as a birthday for a test person in your Excel file before running!

1. Press **`Cmd+S`** to save
2. Click **"Execute workflow"** at the bottom
3. If there's a birthday today → all nodes turn green → Telegram message arrives 🎉
4. If no birthday today → the IF node stops the flow (this is correct behaviour!)

---

### STEP 10 — Publish

1. Click **"Publish"** (top right)
2. The agent now runs every morning at 8 AM automatically!

---

## 📊 Excel File Format

| Full Name | Date of Birth |
|-----------|--------------|
| Rahul Sharma | 22/07/1990 |
| Priya Patel | 15/08/1995 |
| Anita Desai | 03/01/2000 |

> ⚠️ Headers must be exactly: `Full Name` and `Date of Birth`  
> ✅ Supported date formats: `22/07/1990`, `07/22/1990`, `1990-07-22`  
> ✅ Year doesn't matter — only day and month are compared  
> ✅ Multiple people on the same day are all included in one message  

---

## 🔑 Placeholder Reference

| Node | Field | What to fill in |
|------|-------|-----------------|
| Download Birthdays (Google Drive) | Credential | Connect via OAuth (Client ID + Client Secret) |
| Download Birthdays (Google Drive) | File | Select your `.xlsx` file from the dropdown |
| Send Birthday Alert | URL | Replace `PUT_YOUR_BOT_TOKEN_HERE` with your Bot Token |
| Send Birthday Alert | JSON Body → `chat_id` | Replace `PUT_YOUR_CHAT_ID_HERE` with your Chat ID (keep single quotes) |

---

## ⚙️ Configuration Reference

| What to change | Where |
|---|---|
| Schedule time | "Every Day 8AM" node → cron expression |
| Birthday file | "Download Birthdays" node → File dropdown |
| Message text | "Check Today's Birthdays" Code node → edit the `message` variable |
| Bot Token | "Send Birthday Alert" node → URL |
| Chat ID | "Send Birthday Alert" node → JSON Body → `chat_id` |

---

## 🛠️ Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `localhost:5678` not loading | n8n not running | Open Docker Desktop → check n8n container is running |
| `Access blocked` on Google sign-in | Not added as test user | OAuth Consent Screen → Audience → add your Gmail as test user |
| `File not found` in Drive node | File not selected | Switch to "From List" and pick your file from the dropdown |
| No Telegram message received | No birthday today | Add today's date for a test person in your Excel file |
| IF node stops the flow | No birthdays today | This is correct! The agent only sends when there's a match |
| `401 Unauthorized` from Telegram | Wrong Bot Token | Copy the token again from BotFather — no spaces |
| `400 - chat not found` | Wrong Chat ID | Use getUpdates URL method to get the correct Chat ID |
| Date not matching | Wrong date format | Try YYYY-MM-DD format (e.g. 1990-07-22) in your Excel file |

---

## 💡 Ideas to Extend This Agent

- **Send to a group** — add the bot to a WhatsApp-style Telegram group so everyone gets notified
- **Add a gift suggestion** — ask Gemini to suggest a gift idea for the birthday person
- **Send the day before** — change the code to alert you one day in advance
- **Add anniversary reminders** — add a third column for anniversaries
- **Send a personalised message** — include a fun fact about the birthday person

---

## 📁 Repository Structure

```
birthday-reminder-telegram/
├── birthday_reminder_telegram.json   # n8n workflow — import this
├── .env.example                      # Keys and credentials reference
└── README.md                         # This file
```

---

## 📚 Key Concepts Learned

| Concept | Where you used it |
|---------|------------------|
| **Google Drive integration** | Downloading the Excel file |
| **File parsing** | Extracting rows from Excel |
| **Date comparison** | Checking if today matches a birthday |
| **IF node** | Only sending when a birthday is found |
| **Code node** | JavaScript logic to find matches |
| **Telegram Bot API** | Sending the alert message |
| **Conditional automation** | Agent that only acts when needed |

---

## 🧩 Built With

- [n8n](https://n8n.io) — Workflow automation platform
- [Google Drive API](https://developers.google.com/drive) — Birthday list storage
- [Telegram Bot API](https://core.telegram.org/bots/api) — Alert delivery
- [Docker](https://docker.com) — Local hosting

---

*Because forgetting a birthday is unforgivable. Let the bot remember for you. 🎂*
