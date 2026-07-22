# 😄 AI Joke Emailer — n8n Agent

## 🎯 Objective

This is a beginner-friendly n8n agent that demonstrates the core concept of AI automation:

> **Trigger → AI thinks → Action happens**

When you click a button, the agent calls Google Gemini AI to generate a funny joke, then automatically sends it to your Gmail inbox. No manual copy-paste. No coding. Just a button click — and the joke arrives in your email.

This agent is designed as a **classroom exercise** to teach students how to:
- Run n8n locally using Docker
- Connect an AI API (Gemini) to a workflow
- Authenticate with Google (Gmail)
- Chain nodes together to build an automated pipeline

---

## 🏗️ How It Works

```
[ Manual Trigger ]
    Click "Execute workflow"
        ↓
[ HTTP Request → Gemini AI ]
    Sends a prompt: "Tell me a funny joke"
    Gemini returns a joke
        ↓
[ Code Node (JavaScript) ]
    Extracts just the joke text from Gemini's response
        ↓
[ Gmail Node ]
    Sends the joke to your inbox
```

**Total nodes:** 3  
**Trigger:** Manual (click a button)  
**AI Model:** Google Gemini 2.5 Flash  

---

## 📋 What You Need Before Starting

| What | Where to get it | Time |
|------|----------------|------|
| Docker Desktop | https://docker.com/products/docker-desktop | 5 min |
| Google Account (Gmail) | Already have one | — |
| Gemini API Key | https://aistudio.google.com/apikey | 2 min |
| Google OAuth Credentials | https://console.cloud.google.com | 10 min |

---

## 🚀 Step-by-Step Setup

---

### STEP 1 — Install Docker Desktop

Docker is a tool that lets you run applications in isolated containers. We use it to run n8n on your laptop without installing anything complex.

1. Go to: **https://www.docker.com/products/docker-desktop**
2. Download the version for your operating system (Mac or Windows)
3. Install it like any normal application
4. Open Docker Desktop — you should see the Docker whale icon in your taskbar/menu bar
5. Make sure it says **"Engine running"** at the bottom left

> ✅ Docker is ready when you see the green "Engine running" status

---

### STEP 2 — Run n8n Using Docker

n8n is the automation tool we use to build our agent. We run it inside Docker.

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
> - `-d` — runs in background (you can close Terminal after)
> - `--name n8n` — gives the container a name
> - `--restart unless-stopped` — auto-restarts after reboot
> - `-p 5678:5678` — exposes n8n on port 5678
> - `-v n8n_data` — saves your workflows permanently

**Wait about 30 seconds**, then open your browser and go to:

```
http://localhost:5678
```

You will be asked to create a local account. Fill in any name, email and password — **this is 100% local, nothing is sent to the internet.**

> ✅ n8n is ready when you see the "Overview" dashboard

---

### STEP 3 — Get Your Gemini API Key

Gemini is Google's AI. We use it to generate the joke.

1. Go to: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API key"**
4. Select **"Create API key in new project"**
5. Copy the key — it looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXX`

> ⚠️ Keep this key safe — treat it like a password. Don't share it publicly.

> ✅ You now have your Gemini API key

---

### STEP 4 — Set Up Google OAuth (for Gmail)

OAuth is a secure way to give n8n permission to send emails from your Gmail. You set it up once and it works forever.

#### Part A — Create a Google Cloud Project

1. Go to: **https://console.cloud.google.com**
2. Sign in with your Google account
3. Click the project dropdown at the top left → **"New Project"**
4. Name it anything, e.g. `n8n-agent`
5. Click **Create** and wait for it to be selected

#### Part B — Enable Gmail API

1. In the search bar at the top, type: `Gmail API`
2. Click on **"Gmail API"** in the results
3. Click the blue **"Enable"** button
4. Wait for it to enable (10-15 seconds)

#### Part C — Configure OAuth Consent Screen

1. In the left sidebar, click **"APIs & Services"** → **"OAuth consent screen"**

   > If you see a new screen asking about Google Auth Platform, click through to set it up

2. Fill in:
   - **App name:** `n8n agent` (any name)
   - **User support email:** your Gmail address
3. Click **Next** through the steps
4. On the **Audience** page, select **"External"**
5. Click **Next** and complete setup
6. After setup, go to **Audience** in the left sidebar
7. Scroll to **"Test users"** → click **"+ Add users"**
8. Add your Gmail address → click **Save**

#### Part D — Create OAuth Client ID

1. In the left sidebar, click **"Clients"** or go to **"APIs & Services" → "Credentials"**
2. Click **"+ Create Credentials"** → **"OAuth Client ID"**
3. Fill in:
   - **Application type:** `Web application`
   - **Name:** `n8n local`
   - **Authorised redirect URIs:** click **"+ Add URI"** and paste:
     ```
     http://localhost:5678/rest/oauth2-credential/callback
     ```
4. Click **Create**
5. Copy your **Client ID** and **Client Secret** — you'll need these in n8n

> ✅ You now have your Client ID and Client Secret

---

### STEP 5 — Import the Workflow into n8n

1. In n8n (`http://localhost:5678`), click the **`+`** icon (top left)
2. Click **"New Workflow"**
3. Click the **`...`** menu (top right of canvas) → **"Import from file"**
4. Select the file: `ai_joke_emailer.json`
5. The workflow will open with 3 nodes connected

> ✅ You should see: Manual Trigger → HTTP Request → Code → Gmail

---

### STEP 6 — Configure the HTTP Request Node (Gemini)

1. Click on the **"HTTP Request"** node
2. Verify the URL is:
   ```
   https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent
   ```
3. Scroll to **Query Parameters** section
4. You should see:
   - **Name:** `key`
   - **Value:** *(paste your Gemini API key here)*
5. Replace the placeholder value with your actual Gemini API key

---

### STEP 7 — Connect Gmail (Set Up Credential)

1. Click on the **"Send a message"** (Gmail) node
2. Click **"Set up credential"** button
3. In the popup:
   - Paste your **Client ID**
   - Paste your **Client Secret**
4. Click **"Sign in with Google"**
5. A Google popup will appear — select your Gmail account and click **Allow**
6. You should see **"Account connected"** ✅
7. Back in the node, fill in:
   - **To:** your Gmail address (e.g. `you@gmail.com`)
   - **Subject:** `😄 Your AI Joke of the Day!`
   - **Message:** click the field → click **"Expression"** toggle → type `{{ $json.joke }}`

---

### STEP 8 — Test the Agent!

1. Press **`Cmd+S`** (Mac) or **`Ctrl+S`** (Windows) to save
2. Click the orange **"Execute workflow"** button at the bottom of the canvas
3. Watch all nodes turn **green** ✅
4. Check your Gmail inbox — the joke should arrive within seconds! 🎉

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `localhost:5678` not loading | Wait 30 seconds and refresh. Check Docker Desktop shows n8n container as "Running" |
| `Access blocked` when signing into Google | You haven't added yourself as a Test User — go to OAuth Consent Screen → Audience → Add your email |
| `Forbidden - project denied access` | Your Gemini API key doesn't match the project. Get a fresh key from aistudio.google.com |
| `Quota exceeded` from Gemini | Wait 1-2 minutes and try again. Free tier has rate limits |
| Gmail node says fields required | Fill in the To, Subject and Message fields |
| Docker container stops after reboot | Run the full `docker run` command again — next time it will auto-restart |

---

## 🔑 Placeholder Reference

When you import the workflow, look for these placeholders and replace them:

| Node | Field | What to put |
|------|-------|-------------|
| HTTP Request | Query Parameters → Value | Your Gemini API key |
| Gmail | Credential | Connect via OAuth (Client ID + Secret) |
| Gmail | To | Your email address |
| Gmail | Subject | Any subject you like |
| Gmail | Message | `{{ $json.joke }}` |

---

## 💡 Ideas to Extend This Agent

Once you get this working, here are ways to make it more interesting:

- **Change the topic** — instead of a random joke, ask for a joke about a specific topic (e.g. programming, cricket, Bollywood)
- **Schedule it** — swap the Manual Trigger for a Schedule Trigger so you get a joke every morning
- **Add a random topic** — use a Code node to pick a random topic from a list before calling Gemini
- **Send to WhatsApp** — replace Gmail with a WhatsApp node
- **Post to Slack** — send the joke to a Slack channel instead

---

## 📁 Repository Structure

```
ai-joke-emailer/
├── ai_joke_emailer.json     # n8n workflow — import this into n8n
├── .env.example             # Keys and credentials reference
└── README.md                # This file
```

---

## 🧩 Built With

- [n8n](https://n8n.io) — Workflow automation platform
- [Google Gemini 2.5 Flash](https://ai.google.dev) — AI joke generation
- [Gmail API](https://developers.google.com/gmail) — Email delivery
- [Docker](https://docker.com) — Local hosting

---

## 📚 Key Concepts Learned

| Concept | Where you used it |
|---------|------------------|
| **Container** | Running n8n inside Docker |
| **API** | Calling Gemini to generate a joke |
| **API Key** | Authenticating with Gemini |
| **OAuth** | Securely connecting Gmail |
| **Workflow** | Chaining nodes to automate a task |
| **Trigger** | The manual button that starts the workflow |
| **Expression** | Using `{{ $json.joke }}` to pass data between nodes |

---

*This agent was built as part of an n8n AI Agents classroom session.*  
*Not responsible for bad jokes. Gemini is. 😄*
