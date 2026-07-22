# 📈 Stock News Morning Report Agent

## 🎯 Objective

This n8n agent automates your daily stock market research. Every weekday morning at 8 AM, it:

1. Reads your personal stock watchlist from a Google Drive Excel file
2. Calls Google Gemini AI to fetch the latest 48-hour news for each stock
3. Builds a clean HTML report with headlines, price-moving events, and sentiment
4. Delivers it straight to your Gmail inbox — before you even open your laptop

> **The big idea:** Instead of manually checking news for 10-20 stocks every morning, this agent does it all automatically while you sleep.

This agent teaches students how to:
- Run n8n locally using Docker
- Read files from Google Drive
- Loop through a list and call an AI API for each item
- Build and send an HTML email report
- Schedule automation to run on a timer

---

## 🏗️ How It Works

```
[ Schedule Trigger ]
    Fires every weekday at 8:00 AM
        ↓
[ Google Drive Node ]
    Downloads your stock watchlist Excel file
        ↓
[ Extract from File Node ]
    Reads each row from the Excel sheet
        ↓
[ Normalize Stock Rows — Code Node ]
    Cleans up the data, extracts stock names
        ↓
[ Wait Node ]
    Waits 5 seconds between each stock (avoids Gemini rate limits)
        ↓
[ HTTP Request → Gemini AI ]
    For each stock: "What is the latest news about [Stock]?"
        ↓
[ Extract News Summary — Code Node ]
    Pulls just the text response from Gemini's JSON
        ↓
[ Build HTML Report — Code Node ]
    Combines all stocks into one clean HTML email table
        ↓
[ Gmail Node ]
    Sends the report to your inbox
```

**Total nodes:** 9  
**Trigger:** Scheduled — every weekday at 8 AM (`0 8 * * 1-5`)  
**AI Model:** Google Gemini 2.5 Flash  

---

## 📋 What You Need Before Starting

| What | Where to get it | Time needed |
|------|----------------|-------------|
| Docker Desktop | https://docker.com/products/docker-desktop | 5 min |
| Google Account (Gmail + Drive) | Already have one | — |
| Gemini API Key | https://aistudio.google.com/apikey | 2 min |
| Google OAuth Credentials | https://console.cloud.google.com | 10 min |
| Stock list Excel file (.xlsx) | Create it yourself | 2 min |

---

## 🚀 Step-by-Step Setup

---

### STEP 1 — Install Docker Desktop

Docker is a tool that runs applications in isolated containers. We use it to run n8n without complex installation.

1. Go to: **https://www.docker.com/products/docker-desktop**
2. Download for your OS (Mac or Windows)
3. Install it like any normal app
4. Open **Docker Desktop**
5. Wait until you see **"Engine running"** in green at the bottom left

> ✅ Docker is ready when you see "Engine running"

---

### STEP 2 — Run n8n Using Docker

**Open Terminal (Mac)** or **Command Prompt (Windows)** and paste this command:

```bash
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

> **What each part means:**
> - `-d` — runs in the background so you can close Terminal
> - `--name n8n` — gives the container a memorable name
> - `--restart unless-stopped` — auto-restarts after every Mac/PC reboot
> - `-p 5678:5678` — makes n8n accessible on port 5678
> - `-v n8n_data` — saves your workflows so they survive restarts

**Wait about 30 seconds**, then open your browser and go to:

```
http://localhost:5678
```

You will be prompted to create a local account. Fill in any name, email and password — **this is 100% local, nothing goes to the internet.**

> ✅ n8n is ready when you see the "Overview" dashboard

---

### STEP 3 — Create Your Stock List Excel File

This is the file n8n will read every morning.

1. Open **Microsoft Excel** or **Google Sheets**
2. In cell A1, type exactly: `StockName`
3. From A2 onwards, add your stocks — one per row:

| StockName |
|-----------|
| Bajaj Finance |
| Tata Motors |
| Reliance Industries |
| HDFC Bank |
| TCS |
| Infosys |

4. Save the file as `.xlsx` format (Excel format)
5. Upload it to **Google Drive**:
   - Go to https://drive.google.com
   - Click **"+ New"** → **"File upload"**
   - Select your `.xlsx` file

> ⚠️ The column header must be exactly `StockName` — capital S, capital N, no spaces
>
> ⚠️ Start with 5-6 stocks if you are using the Gemini free tier (to avoid rate limits)

---

### STEP 4 — Get Your Gemini API Key

Gemini is Google's AI. We use it to fetch and summarise news for each stock.

1. Go to: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API key"**
4. Select **"Create API key in new project"**
5. Copy the key — it looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXX`

> ⚠️ Keep this key safe — treat it like a password. Never share it publicly or check it into GitHub.

> ✅ You now have your Gemini API key

---

### STEP 5 — Set Up Google OAuth (for Drive + Gmail)

OAuth lets n8n securely access your Google Drive and Gmail. You set it up once.

#### Part A — Create a Google Cloud Project

1. Go to: **https://console.cloud.google.com**
2. Sign in with your Google account
3. Click the project dropdown (top left, next to "Google Cloud") → **"New Project"**
4. Name it: `n8n-stock-agent` (or anything)
5. Click **Create** and wait for it to be selected (you'll see it in the top bar)

#### Part B — Enable Google Drive API

1. In the search bar at the top, type: `Google Drive API`
2. Click **"Google Drive API"** in the results
3. Click the blue **"Enable"** button
4. Wait for it to enable

#### Part C — Enable Gmail API

1. In the search bar, type: `Gmail API`
2. Click **"Gmail API"**
3. Click **"Enable"**

#### Part D — Configure OAuth Consent Screen

1. In the left sidebar, go to **"APIs & Services"** → **"OAuth consent screen"**

   > If redirected to Google Auth Platform, look for **"Get started"** or **"Branding"** in the sidebar

2. Fill in:
   - **App name:** `n8n stock agent` (any name)
   - **User support email:** your Gmail address
3. Click **Next** / **Save and continue** through all steps
4. On the **Audience** page, make sure **"External"** is selected
5. After setup is complete, click **"Audience"** in the left sidebar
6. Scroll down to **"Test users"** → click **"+ Add users"**
7. Type your Gmail address → click **Add** → click **Save**

> ✅ Your Gmail is now an approved test user

#### Part E — Create OAuth Client ID

1. In the left sidebar, click **"Clients"** (or go to **"APIs & Services" → "Credentials"**)
2. Click **"+ Create client"** or **"+ Create Credentials" → "OAuth Client ID"**
3. Fill in:
   - **Application type:** `Web application`
   - **Name:** `n8n local`
   - **Authorised redirect URIs:** click **"+ Add URI"** and paste:
     ```
     http://localhost:5678/rest/oauth2-credential/callback
     ```
4. Click **Create**
5. A popup shows your **Client ID** and **Client Secret** — copy and save both

> ✅ You now have your Client ID and Client Secret

---

### STEP 6 — Import the Workflow into n8n

1. In n8n (`http://localhost:5678`), click the **`+`** icon (top left sidebar)
2. Click **"New Workflow"**
3. Click the **`...`** menu at the top right of the canvas
4. Click **"Import from file"**
5. Select: `stock_news_morning_report.json`
6. The workflow loads with all 9 nodes connected

> ✅ You should see the full pipeline from Schedule Trigger to Gmail

---

### STEP 7 — Connect Google Drive

1. Click the **"Download Stock List (Google Drive)"** node
2. Click the **✏️ edit icon** next to "Credential" → "Google Drive account"
3. In the popup:
   - Paste your **Client ID**
   - Paste your **Client Secret**
4. Click **"Sign in with Google"**
5. A Google popup appears — select your account → click **Allow**
6. You should see **"Account connected"** ✅
7. Back in the node, find the **File** field:
   - Click the dropdown that says "By ID"
   - Switch to **"From List"**
   - Your Excel file should appear — select it

---

### STEP 8 — Connect Gmail

1. Click the **"Send Morning Report Email"** node
2. Click **"Set up credential"**
3. In the popup:
   - Paste the **same Client ID** as before
   - Paste the **same Client Secret** as before
4. Click **"Sign in with Google"** and approve
5. You should see **"Account connected"** ✅
6. Fill in the node fields:
   - **To:** your Gmail address (e.g. `you@gmail.com`)
   - **Subject:** is already set to auto-include today's date
   - **Message:** is already set to `{{ $json.html }}`

---

### STEP 9 — Add Your Gemini API Key

1. Click the **"Ask Gemini for News"** node
2. Scroll down to the **"Query Parameters"** section
3. You will see:
   - **Name:** `key`
   - **Value:** a placeholder text
4. Click on the **Value** field and replace it with your actual Gemini API key

---

### STEP 10 — Save and Publish

1. Press **`Cmd+S`** (Mac) or **`Ctrl+S`** (Windows) to save
2. Click the **"Publish"** button (top right of canvas)
3. The workflow is now **active** and will run every weekday at 8 AM automatically!

> 💡 To test immediately without waiting for 8 AM, click the orange **"Execute workflow"** button at the bottom of the canvas

---

## 📊 Excel File Format

| StockName |
|-----------|
| Bajaj Finance |
| Tata Motors |
| Reliance Industries |
| HDFC Bank |
| TCS |

> ⚠️ Column header must be exactly `StockName` (case-sensitive)  
> ⚠️ One stock name per row, starting from row 2  
> ⚠️ No blank rows in the middle of the list  

---

## 📧 Sample Report Email

The email you receive will look like this:

```
📈 Morning Stock News Report
Wednesday, 22 July 2026

Stock                  | News Summary
-----------------------|-----------------------------------------------
Bajaj Finance          | No major company-specific news in the last 48
                       | hours. Analysts maintain Buy ratings. Sentiment:
                       | Neutral to cautiously positive.

Reliance Industries    | RIL announces new partnership in green energy
                       | space. Share price up 1.2% on strong volumes.
                       | Sentiment: Positive.

HDFC Bank              | Q1 results beat expectations. NIM stable at
                       | 4.1%. FIIs buying on dips. Sentiment: Positive.
```

---

## ⚙️ Configuration Reference

Once it's working, here's how to customise it:

| What to change | Where to change it |
|---|---|
| Schedule time | "Every Weekday 8AM" node → cron expression field |
| Recipient email | "Send Morning Report Email" node → **To** field |
| Gemini API key | "Ask Gemini for News" node → Query Parameters → **Value** |
| Stock Excel file | "Download Stock List" node → **File** dropdown |
| Delay between stocks | "Wait" node → **Wait Amount** field |
| Gemini model | "Ask Gemini for News" node → **URL** (change model name) |

**Current Gemini model:** `gemini-2.5-flash`  
**Current schedule:** `0 8 * * 1-5` = 8 AM, Monday to Friday

---

## ⚠️ Gemini Free Tier Limits

The free Gemini API has limits:

| Limit | Value |
|-------|-------|
| Requests per minute | 15 |
| Daily limit | ~500 requests (varies) |

**How to stay within limits:**
- Start with **5-6 stocks** when testing
- The **Wait node (5 seconds)** spaces out requests automatically
- Once confirmed working, you can increase to 15-20 stocks
- For larger watchlists, enable billing on Google Cloud (~₹0.50/month)

---

## 🔄 Keep n8n Running After Reboot

The Docker command includes `--restart unless-stopped` which means n8n will restart automatically every time your computer reboots.

Also make sure Docker Desktop itself starts on login:
- Open Docker Desktop → **Settings → General**
- ✅ Check **"Start Docker Desktop when you sign in"**

---

## 🛠️ Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `localhost:5678` not loading | n8n container not running | Open Docker Desktop → check if n8n container is running → if not, run the docker command again |
| `Access blocked` during Google sign-in | Not added as test user | Go to Google Cloud Console → OAuth Consent Screen → Audience → add your Gmail as test user |
| `File not found` in Drive node | File ID mismatch | In the Drive node, switch File field from "By ID" to "From List" and reselect your file |
| `Quota exceeded` from Gemini | Too many requests too fast | Wait 2 minutes and retry. Reduce stock list to 5 stocks for testing |
| `API key not valid` | Wrong key or extra spaces | Copy the key fresh from aistudio.google.com, no spaces |
| `Forbidden - project denied` | API not enabled in that project | Enable Gemini API at console.cloud.google.com for your project |
| Email not received | Gmail node not configured | Check To, Subject and Message fields are filled in the Gmail node |
| Workflow not running at 8AM | Not published | Click the "Publish" button — saving alone is not enough |

---

## 🔑 Placeholder Reference

After importing, find and fill these placeholders:

| Node | Field | What to fill in |
|------|-------|-----------------|
| Download Stock List (Google Drive) | Credential | Connect via OAuth (Client ID + Client Secret) |
| Download Stock List (Google Drive) | File | Select your Excel file from the dropdown |
| Ask Gemini for News | Query Parameters → Value | Your Gemini API key |
| Send Morning Report Email | Credential | Connect via OAuth (same Client ID + Secret) |
| Send Morning Report Email | To | Your email address |

---

## 💡 Ideas to Extend This Agent

Once working, here are ways to make it more powerful:

- **Add more data** — include stock price, P/E ratio by calling a stock data API
- **Filter by sentiment** — only email if any stock has negative news
- **WhatsApp delivery** — send the report via WhatsApp instead of email
- **Weekly summary** — add a second workflow that summarises the week every Friday
- **Sector grouping** — group stocks by sector (Banking, IT, Auto) in the report
- **Multiple watchlists** — read from different Excel sheets for different portfolios

---

## 📁 Repository Structure

```
stock-news-morning-report/
├── stock_news_morning_report.json   # n8n workflow — import this into n8n
├── .env.example                     # Keys and credentials reference
└── README.md                        # This file
```

---

## 📚 Key Concepts Learned

| Concept | Where you used it |
|---------|------------------|
| **Container** | Running n8n inside Docker |
| **Schedule Trigger** | Cron expression to run at 8 AM weekdays |
| **API** | Calling Gemini to fetch news |
| **API Key** | Authenticating with Gemini |
| **OAuth** | Securely connecting Google Drive and Gmail |
| **Loop** | Processing each stock one by one |
| **Rate limiting** | Wait node to avoid overwhelming the API |
| **HTML email** | Building a formatted report in code |
| **Expression** | Using `{{ $json.field }}` to pass data between nodes |

---

## 🧩 Built With

- [n8n](https://n8n.io) — Workflow automation platform
- [Google Gemini 2.5 Flash](https://ai.google.dev) — AI news summarisation
- [Google Drive API](https://developers.google.com/drive) — Stock list storage
- [Gmail API](https://developers.google.com/gmail) — Report delivery
- [Docker](https://docker.com) — Local hosting

---

*Generated automatically via n8n + Gemini. Not investment advice.*
