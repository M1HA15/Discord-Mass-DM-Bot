# 🚀 Discord Mass DM Bot

Welcome to the **Discord Mass DM Bot**! 🎉 This is a specialized bot designed to send direct messages (DMs) to all members of a Discord server efficiently, while ensuring compliance with Discord's rate limits. This bot is perfect for server administrators who need to communicate with all members in a streamlined manner.

## 🌟 Key Features

- **⚡️ High Efficiency:** The bot is optimized to work within Discord's rate limits, ensuring smooth operation even on large servers.
- **📶 Ping Command:** Quickly check the bot's latency with a fun, randomized response.
- **🔔 Mass DM:** Send personalized messages to every member of your server with a single command (requires administrator permissions).
- **📊 Real-time DM Status:** Track the progress of your DM campaign, with detailed stats on sent, failed, and pending messages.
- **🛠 Comprehensive Help Command:** Access a full list of available commands and their descriptions.

## 💡 How It Works

This bot is designed to be used in **one server at a time**. It sends DMs to each member at a controlled pace to avoid triggering Discord's rate limits, while providing real-time updates on the operation's status.

### Commands Overview

- **`;ping`**: Get the bot's current latency with a fun response.
- **`;dm_all [message]`**: Send a DM to all members of the server with the specified message. This command requires administrator permissions and has a cooldown to prevent abuse.
- **`;dm_status`**: View the current status of the ongoing DM operation, including the number of sent, failed, and pending messages.
- **`;help`**: Display the help menu with all available commands and their usage.

## 🛠 Setup Instructions

### Prerequisites

To get started, you'll need:

- **Python 3.6+**
- Required **Python libraries**: `discord.py==1.7.3`, `asyncio`, `pytz`, `json`

You can install the dependencies using:

```bash
pip install -r requirements.txt
```

### Running the Bot

- Clone this repository.
- Open the `settings.json` file and insert your Discord bot token and desired command prefix.
- Run the bot with:
```bash
python bot.py
```

### Permissions

The bot requires **Administrator permissions** to function correctly, as it needs to send direct messages to all members of the server. Ensure that the bot has these permissions to avoid any issues with sending messages.

## 🎨 Customization

You can customize the bot's prefix and status message directly in the `settings.json` file:
```json
{
    "token": "your-bot-token-here",
    "prefix": ";",
    "status": "your-custom-status-here"
}
```

## ⚠️ Important Disclaimer

This **bot** is **intended** for **administrative use only**. It is meant to **facilitate communication within your server**. **I am not responsible for any misuse or malicious activities conducted using this bot**. Please ensure you **comply** with **[Discord's](https://discord.com/) [Terms of Service](https://discord.com/terms)** and **[Community Guidelines](https://discord.com/guidelines)**.

**Use this tool responsibly, and ensure all members are treated with respect and dignity**.

## 📞 Support

**If you encounter** any **issues** or have any **questions**, **feel free to reach out** to me on **Discord**: `mihaivere`

## 🙏 Acknowledgments:

**Thank you for using the Discord Mass DM Bot**! Make sure to **star the repository** if you found it **useful**!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/M1HA15/Discord-Mass-DM-Bot/blob/main/LICENSE) file for more details.
