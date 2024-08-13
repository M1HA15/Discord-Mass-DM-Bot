# 🚀 Discord Mass DM Bot

Welcome to the **Discord Mass DM Bot**! 🎉 This is a specialized tool designed to send direct messages (DMs) to all members of a single Discord server. Built with efficiency in mind, this bot helps you avoid Discord's rate limits while delivering your message to your community.

## 🌟 Key Features

- **⚡️ High Efficiency:** Optimized to work within Discord's rate limits, ensuring smooth operations even in large servers.
- **📶 Ping Command:** Check the bot's latency with a fun, randomized response.
- **🔔 Mass DM:** Send personalized messages to every member in your server with administrator permissions.
- **📊 Real-time DM Status:** Track the progress of your DM campaign with detailed stats on sent, failed, and pending messages.
- **🛠 Comprehensive Help Command:** Access a complete list of available commands and their usage.

## 💡 How It Works

This bot is designed to be used in **one server at a time**. It ensures that each member receives your message without triggering Discord's rate limits, by carefully pacing the sending process.

### Commands Overview

- **`;ping`**: Get the bot's current latency.
- **`;dm_all [message]`**: Send a DM to all members of the server with the specified message. Requires administrator permissions.
- **`;dm_status`**: View the current status of the ongoing DM operation.
- **`;help`**: Display the help menu with all available commands.

## 🛠 Setup Instructions

### Prerequisites

To get started, you'll need:

- **Python 3.6+**
- Required Python libraries: `discord.py`, `asyncio`, `pytz`

You can install the dependencies using:

```bash
pip install -r requirements.txt
```
