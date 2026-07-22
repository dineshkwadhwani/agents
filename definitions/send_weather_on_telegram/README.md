# 🌤️ Daily Weather Telegram Agent

## 🎯 Objective

This n8n agent sends you a **personalised weather report on Telegram every morning at 8 AM** — automatically, without you doing anything.

> **The big idea:** Instead of opening a weather app every morning, your phone receives a clean weather briefing directly in Telegram — sent by your own bot that you built!

This agent teaches students how to:
- Use a **public API** (OpenWeatherMap) to fetch real-world data
- **Format and transform** API data using a Code node
- Send messages to **Telegram** using a Bot
- Use the **Schedule Trigger** to run automatically every day

---

## 🏗️ How It Works

```
[ Schedule Trigger ]
    Fires every day at 8:00 AM
        ↓
[ HTTP Request → OpenWeatherMap API ]
    Fetches current weather for your city
    Returns: temperature, humidity, wind, conditions
        ↓
[ Code Node (JavaScript) ]
    Formats the weather data into a nice readable message
    Adds weather emojis based on conditions ☀️🌧️⛈️❄️
        ↓
[ HTTP Request → Telegram Bot API ]
    Sends the formatted message to your Telegram chat
```

**Total nodes:** 4  
**Trigger:** Scheduled — every day at 8 AM (`0 8 * * *`)  
**APIs used:** OpenWeatherMap + Telegram Bot API  
**No OAuth needed!** 🎉 Just two API keys/tokens.

---

## 📱 Sample Telegram Message

This is what you will receive every morning:

```
🌤 Morning Weather Report
📅 Wednesday, 22 July 2026
📍 Pune, IN

🌡 Temperature: 28°C (Feels like 31°C)
🔼 High: 33°C  🔽 Low: 24°C
💧 Humidity: 72%
💨 Wind: 3.2 m/s
🌤 Condition: Broken clouds

Have a great day! 🙌
```

---

## 📋 What You Need Before Starting

| What | Where to get it | Time needed |
|------|----------------|-------------|
| Docker Desktop | https://docker.com/products/docker-desktop | 5 min |
| n8n running locally | See Step 1 below | 2 min |
| Telegram app | Your phone's app store | 2 min |
| Telegram Bot Token | @BotFather on Telegram | 2 min |
| Telegram Chat ID | @userinfobot on Telegram | 1 min |
| OpenWeatherMap API Key | https://openweathermap.org/api | 3 min |

> ✅ **No Google Cloud setup needed for this agent!** Much simpler than Gmail agents.

---

## 🚀 Step-by-Step Setup

---

### STEP 1 — Install Docker and Run n8n

If you already have n8n running from a previous session, skip to Step 2.

**Install Docker Desktop:**
1. Go to: **https://www.docker.com/products/docker-desktop**
2. Download for your OS (Mac or Windows)
3. Install and open it — wait for **"Engine running"** status

**Run n8n:**

Open Terminal (Mac) or Command Prompt (Windows) and paste:

```bash
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

Wait 30 seconds then go to: **http://localhost:5678**

Create your local account when prompted (name, email, password — all stays local).

> ✅ n8n is ready when you see the Overview dashboard

---

### STEP 2 — Get Your OpenWeatherMap API Key

OpenWeatherMap is a free weather API. We use it to get real-time weather data.

1. Go to: **https://home.openweathermap.org/users/sign_up**
2. Sign up for a free account
3. Check your email and verify your account
4. Go to: **https://home.openweathermap.org/api_keys**
5. You will see a **Default** API key already created — copy it

> ⚠️ New API keys take up to **10 minutes** to activate. If you get an error, wait a few minutes and try again.

> ✅ You now have your OpenWeatherMap API key

---

### STEP 3 — Create Your Telegram Bot

This is the most exciting step! You will create your own Telegram bot in under 2 minutes.

1. Open **Telegram** on your phone or computer
2. In the search bar, search for: **@BotFather**
3. Open the BotFather chat and click **Start**
4. Send this message: `/newbot`
5. BotFather asks for a **name** — type anything, e.g.: `My Weather Bot`
6. BotFather asks for a **username** — must end in "bot", e.g.: `myweather_yourname_bot`
7. BotFather sends you a message with your **Bot Token** — it looks like:
   ```
   123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
8. **Copy this token** — you will need it in n8n

> ✅ Your Telegram bot is created!

---

### STEP 4 — Get Your Telegram Chat ID

The Chat ID tells Telegram which person to send the message to (you!).

#### Method 1 — Try @userinfobot first (sometimes works)
1. In Telegram, search for: **@userinfobot**
2. Open the chat and click **Start** (or send any message)
3. It replies with your information including your ID number
4. Copy the number next to **"Id:"**

#### Method 2 — getUpdates URL (always works, use this if Method 1 fails)

1. First, **send any message to your bot** on Telegram (search for it and click Start)
2. Open your browser and paste this URL (replace with your actual Bot Token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN_HERE/getUpdates
   ```
   Example:
   ```
   https://api.telegram.org/bot123456789:AAFxxxxxxxxx/getUpdates
   ```
3. You will see a JSON response — look for `"chat":{"id":` and copy the number after it:
   ```json
   "chat":{"id":1784026614,"first_name":"Dinesh"...}
   ```
4. That number (`1784026614` in the example) is your **Chat ID**

> ⚠️ If the URL returns `{"ok":true,"result":[]}` (empty), it means your bot hasn't received any messages yet. Go to Telegram, find your bot, click Start, then refresh the URL.

> ✅ You now have your Chat ID

---

### STEP 5 — Start Your Bot

Before n8n can send you messages, you need to start a conversation with your bot first.

1. In Telegram, search for your bot by its username (e.g. `@myweather_yourname_bot`)
2. Open the chat and click **Start**

> ⚠️ This step is easy to forget! If you skip it, Telegram will reject messages from the bot.

---

### STEP 6 — Import the Workflow into n8n

1. In n8n (`http://localhost:5678`), click the **`+`** icon (top left)
2. Click **"New Workflow"**
3. Click the **`...`** menu (top right of canvas)
4. Click **"Import from file"**
5. Select: `daily_weather_telegram.json`
6. The workflow loads with 4 nodes connected

> ✅ You should see: Schedule Trigger → Get Weather → Format Message → Send to Telegram

---

### STEP 7 — Configure the Get Weather Node

1. Click the **"Get Weather"** node
2. Find the **Query Parameters** section
3. Fill in the values:

| Parameter | Value |
|-----------|-------|
| `q` | Your city name (e.g. `Pune,IN` or `Mumbai,IN` or `Delhi,IN`) |
| `appid` | Your OpenWeatherMap API key |
| `units` | `metric` (already set — keeps temperature in °C) |

> 💡 For best accuracy use `CityName,CountryCode` format e.g. `Pune,IN` or `London,GB`

---

### STEP 8 — Configure the Send to Telegram Node

1. Click the **"Send to Telegram"** node
2. Find the **URL** field at the top of the node
3. Replace `PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE` with your actual Bot Token

The URL should look like:
```
https://api.telegram.org/bot123456789:AAFxxxxxxxxxx/sendMessage
```

4. Scroll down to the **JSON Body** field
5. Look for `PUT_YOUR_TELEGRAM_CHAT_ID_HERE` and replace it with your Chat ID **keeping the single quotes**:

```json
{
  "chat_id": '1784026614',
  "text": "...",
  "parse_mode": "Markdown"
}
```

> ⚠️ Keep the single quotes around your Chat ID — e.g. `'1784026614'` not just `1784026614`

---

### STEP 9 — Test It!

1. Press **`Cmd+S`** (Mac) or **`Ctrl+S`** (Windows) to save
2. Click the orange **"Execute workflow"** button at the bottom
3. Watch all 4 nodes turn **green** ✅
4. **Check your Telegram** — the weather message should arrive instantly! 🎉

---

### STEP 10 — Publish to Activate Daily Schedule

1. Click the **"Publish"** button (top right of canvas)
2. The workflow is now **active**
3. Every day at 8 AM, Telegram will receive your weather report automatically!

---

## 🔑 Placeholder Reference

After importing, find and replace these placeholders:

| Node | Field | What to fill in |
|------|-------|-----------------|
| Get Weather | Query Parameters → `q` value | Your city e.g. `Pune,IN` |
| Get Weather | Query Parameters → `appid` value | Your OpenWeatherMap API key |
| Send to Telegram | URL | Replace `PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE` with your Bot Token |
| Send to Telegram | JSON Body → `chat_id` | Replace `PUT_YOUR_TELEGRAM_CHAT_ID_HERE` with your Chat ID |

---

## 🛠️ Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `401 - Invalid API key` from OpenWeatherMap | Wrong or new API key | Double check key. New keys take 10 min to activate |
| `400 - Bad Request` from OpenWeatherMap | City name not found | Try `CityName,CountryCode` format e.g. `Pune,IN` |
| `401 Unauthorized` from Telegram | Wrong Bot Token | Copy the token again from BotFather — no spaces |
| `400 - chat not found` from Telegram | Wrong Chat ID or bot not started | Make sure you sent /start to your bot. Check Chat ID from @userinfobot |
| `403 - Forbidden` from Telegram | You haven't started the bot | Open Telegram → find your bot → click Start |
| `getUpdates` returns empty `[]` | Bot has no messages yet | Send any message to your bot on Telegram first, then refresh the URL |
| Chat ID not working | Missing quotes around ID | Keep single quotes around the Chat ID in the JSON body: `'1784026614'` |
| `localhost:5678` not loading | n8n not running | Open Docker Desktop → check n8n container is green |
| Weather not running at 8AM | Workflow not published | Click Publish button — saving is not enough |

---

## ⚙️ Configuration Reference

| What to change | Where |
|---|---|
| Schedule time | "Every Day 8AM" node → cron expression |
| City | "Get Weather" node → Query Parameters → `q` value |
| Temperature unit | "Get Weather" node → `units` parameter (`metric`=°C, `imperial`=°F) |
| Message format | "Format Weather Message" Code node → edit the message template |
| Bot Token | "Send to Telegram" node → URL field |
| Chat ID | "Send to Telegram" node → JSON Body → `chat_id` |

**Current schedule:** `0 8 * * *` = 8 AM every day (including weekends)
To make it weekdays only: `0 8 * * 1-5`

---

## 💡 Ideas to Extend This Agent

Once working, here are ways to make it more interesting:

- **Add a forecast** — call the `/forecast` endpoint to get a 5-day forecast
- **Add UV Index** — call OpenUV API and add sun protection advice
- **Add air quality** — use OpenWeatherMap's Air Pollution API
- **Multiple cities** — send weather for home AND office
- **Conditional alerts** — only send if rain is expected (`if rain → send alert`)
- **Weekly summary** — every Sunday, send a 7-day forecast
- **Send to a group** — add the bot to a Telegram group and share weather with family/friends

---

## 📁 Repository Structure

```
daily-weather-telegram/
├── daily_weather_telegram.json    # n8n workflow — import this into n8n
├── .env.example                   # Keys and tokens reference
└── README.md                      # This file
```

---

## 📚 Key Concepts Learned

| Concept | Where you used it |
|---------|------------------|
| **Schedule Trigger** | Runs the workflow every morning at 8 AM |
| **REST API** | Calling OpenWeatherMap to get weather data |
| **API Key** | Authenticating with OpenWeatherMap |
| **JSON parsing** | Extracting temperature, humidity etc from the API response |
| **Code Node** | Formatting data and building the message string |
| **Bot API** | Sending messages via Telegram Bot |
| **HTTP POST** | How the Telegram API receives messages |
| **Markdown** | Formatting the Telegram message with bold and emojis |

---

## 🧩 Built With

- [n8n](https://n8n.io) — Workflow automation platform
- [OpenWeatherMap API](https://openweathermap.org/api) — Real-time weather data (free tier)
- [Telegram Bot API](https://core.telegram.org/bots/api) — Message delivery
- [Docker](https://docker.com) — Local hosting

---

*Powered by n8n + OpenWeatherMap. Weather data is approximate. Always carry an umbrella just in case! ☂️*
