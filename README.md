# agents

This project is set up for organizing n8n agent exports and their supporting documentation.

## Project structure

- definitions/ - contains one folder per agent
- each agent folder can include:
  - <agent-name>.json - the exported workflow/agent JSON used in n8n
  - README.md - a detailed explanation of what the agent does and how to set it up

## Agents in this project

### 1. Stock News Morning Report Agent
Location:
- [definitions/stock_news_morning_report/stock_news_morning_report.json](definitions/stock_news_morning_report/stock_news_morning_report.json)
- [definitions/stock_news_morning_report/README.md](definitions/stock_news_morning_report/README.md)

What it does:
- Runs every weekday at 8:00 AM
- Downloads a stock watchlist from Google Drive
- Uses Gemini to gather recent news for each stock
- Builds an HTML report and sends it by email

### 2. AI Joke Emailer
Location:
- [definitions/send_joke_agent/README.md](definitions/send_joke_agent/README.md)

What it does:
- Runs manually when executed from n8n
- Calls Gemini to generate a funny joke
- Sends the joke to a Gmail inbox

## Notes

This layout keeps the imported JSON workflow files and the companion documentation together, making it easier to manage and reuse agent definitions.
