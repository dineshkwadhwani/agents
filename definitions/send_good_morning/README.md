# 🌅 Good Morning Telegram Agent

## 🎯 Objective

This is the **simplest possible n8n agent** — just 2 nodes.

Every morning at 8 AM, it automatically sends a "Good Morning" message with today's date to your Telegram chat.

> **The big idea:** You wake up, and Telegram already has a message waiting for you — sent automatically by a bot you built yourself!

This agent is the **perfect starting point** for anyone new to n8n. It teaches:
- How to use the **Schedule Trigger** to run something automatically
- How to call an **external API** (Telegram) using HTTP Request
- How to send a **JSON body** in an API call
- The core concept of **Trigger → Action**

---

## 🏗️ How It Works

```
[ Schedule Trigger ]
    Fires every day at 8:00 AM
        ↓
[ HTTP Request → Telegram Bot API ]
    Sends "Good Morning!" message to your Telegram chat
```

**Total nodes:** 2  
**Trigger:** Scheduled — every day at 8 AM (`0 8 * * *`)  
**API used:** Telegram Bot API (free, no billing needed)  
**No OAuth, no Google Cloud, no API keys to pay for!** 🎉

---

## 📱 Sample Telegram Message

```
🌅 Good Morning! Have an amazing day ahead! 😊

Wednesday, 22 July 2026
```

---

## 📋 What You Need Before Starting

| What | Where to get it | Time needed |
|------|----------------|-------------|
| Docker Desktop | https://docker.com/products/docker-desktop | 5 min |
| Telegram app | Your phone's app store | 2 min |
| Telegram Bot Token | @BotFather on Telegram | 2 min |
| Telegram Chat ID | @userinfobot or getUpdates URL | 1 min |

> ✅ **This is the easiest agent to set up — no paid APIs, no Google Cloud, no OAuth!**

---

## 🚀 Step-by-Step Setup

---

### STEP 1 — Install Docker and Run n8n

If you already have n8n running from a previous session, skip to Step 2.

**Install Docker Desktop:**
1. Go to: **https://www.docker.com/products/docker-desktop**
2. Download for your OS (Mac or Windows)
3. Install and open it — wait for **"Engine running"** at the bottom left

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

Create your local account when prompted — stays 100% on your machine.

> ✅ n8n is ready when you see the Overview dashboard

---

### STEP 2 — Create Your Telegram Bot

1. Open **Telegram** on your phone or computer
2. Search for: **@BotFather**
3. Open the chat and click **Start**
4. Send: `/newbot`
5. BotFather asks for a **name** — type anything e.g. `My Morning Bot`
6. BotFather asks for a **username** — must end in "bot" e.g. `mymorning_yourname_bot`
7. BotFather sends you a **Bot Token** that looks like:
   ```
   123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
8. **Copy this token** — you'll need it in Step 5

> ✅ Your Telegram bot is created!

---

### STEP 3 — Start a Chat With Your Bot

Before your bot can send you messages, you need to start a conversation with it first.

1. In Telegram, search for your bot by username (e.g. `@mymorning_yourname_bot`)
2. Open the chat
3. Click **Start** or send any message like "Hi"

> ⚠️ Don't skip this step! If you do, Telegram will block messages from your bot.

---

### STEP 4 — Get Your Telegram Chat ID

Your Chat ID tells Telegram exactly who to send the message to.

#### Method 1 — @userinfobot (try this first)
1. In Telegram, search: **@userinfobot**
2. Send any message to it
3. It replies with your ID number — copy it

#### Method 2 — getUpdates URL (use this if Method 1 doesn't work)
1. Make sure you've sent a message to your bot (Step 3)
2. Open your browser and go to (replace with your token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN_HERE/getUpdates
   ```
3. Look for `"chat":{"id":` in the response — the number after it is your Chat ID:
   ```json
   "chat":{"id":1784026614,"first_name":"Dinesh"}
   ```
4. Copy that number

> ⚠️ If you see `{"ok":true,"result":[]}` — go to Telegram, send a message to your bot, then refresh the URL

> ✅ You now have your Chat ID

---

### STEP 5 — Import the Workflow

1. In n8n (`http://localhost:5678`), click **`+`** (top left)
2. Click **"New Workflow"**
3. Click the **`...`** menu (top right of canvas)
4. Click **"Import from file"**
5. Select: `good_morning_telegram.json`

> ✅ You should see 2 nodes: Schedule Trigger → Send Good Morning

---

### STEP 6 — Configure the Send Good Morning Node

1. Click the **"Send Good Morning"** node
2. Find the **URL** field — replace `PUT_YOUR_BOT_TOKEN_HERE` with your Bot Token:
   ```
   https://api.telegram.org/bot123456789:AAFxxxxxxxxxx/sendMessage
   ```
3. Scroll down to the **JSON Body** field
4. Replace `PUT_YOUR_CHAT_ID_HERE` with your Chat ID (keep the single quotes):
   ```
   '1784026614'
   ```

---

### STEP 7 — Test It!

1. Press **`Cmd+S`** (Mac) or **`Ctrl+S`** (Windows) to save
2. Click **"Execute workflow"** at the bottom of the canvas
3. Both nodes should turn **green** ✅
4. Check your **Telegram** — the Good Morning message should arrive instantly! 🎉

---

### STEP 8 — Publish to Activate Daily Schedule

1. Click **"Publish"** (top right)
2. The workflow is now **active**
3. Every morning at 8 AM, Telegram will receive your Good Morning message automatically!

---

## 🔑 Placeholder Reference

| Node | Field | What to fill in |
|------|-------|-----------------|
| Send Good Morning | URL | Replace `PUT_YOUR_BOT_TOKEN_HERE` with your Bot Token |
| Send Good Morning | JSON Body → `chat_id` | Replace `PUT_YOUR_CHAT_ID_HERE` with your Chat ID (keep single quotes) |

---

## ⚙️ Configuration Reference

| What to change | Where |
|---|---|
| Schedule time | "Every Day 8AM" node → cron expression |
| Message text | "Send Good Morning" node → JSON Body → `text` field |
| Recipient | "Send Good Morning" node → JSON Body → `chat_id` |
| Bot | "Send Good Morning" node → URL (change the token) |

**Current schedule:** `0 8 * * *` = 8 AM every day including weekends
To make it weekdays only: `0 8 * * 1-5`

---

## 🛠️ Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `localhost:5678` not loading | n8n not running | Open Docker Desktop → check n8n container is running |
| `401 Unauthorized` from Telegram | Wrong Bot Token | Copy the token again from BotFather — no spaces |
| `400 - chat not found` | Wrong Chat ID or bot not started | Send /start to your bot on Telegram. Check Chat ID via getUpdates URL |
| `403 - Forbidden` | Haven't started the bot | Find your bot on Telegram → click Start |
| `getUpdates` returns `[]` | Bot has no messages | Send any message to your bot first, then refresh URL |
| Message not arriving at 8AM | Workflow not published | Click the Publish button — saving alone is not enough |

---

## 💡 Ideas to Extend This Agent

Once working, here are fun ways to make it more interesting:

- **Personalise the message** — add the student's name using a Code node
- **Add a quote** — call Gemini AI to generate a motivational quote each morning
- **Add weather** — combine with the Weather agent to include today's forecast
- **Change the message daily** — use a Code node to pick a different message each day of the week
- **Send to a group** — add your bot to a Telegram group and send to all friends at once
- **Add emoji variety** — randomly pick a different emoji each morning

---

## 📁 Repository Structure

```
good-morning-telegram/
├── good_morning_telegram.json    # n8n workflow — import this into n8n
├── .env.example                  # Keys and tokens reference
└── README.md                     # This file
```

---

## 📚 Key Concepts Learned

| Concept | Where you used it |
|---------|------------------|
| **Schedule Trigger** | Runs the workflow automatically every morning |
| **HTTP Request** | Calling the Telegram API to send a message |
| **POST request** | Sending data (the message) to an API endpoint |
| **JSON body** | Structuring the data sent to Telegram |
| **Bot Token** | Authenticating your bot with Telegram |
| **Chat ID** | Telling Telegram who to send the message to |
| **Publish** | Activating a workflow to run on schedule |

---

## 🧩 Built With

- [n8n](https://n8n.io) — Workflow automation platform
- [Telegram Bot API](https://core.telegram.org/bots/api) — Free messaging API
- [Docker](https://docker.com) — Local hosting

---

*The simplest agent. The biggest smile when it works. 🌅*
