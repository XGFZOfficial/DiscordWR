# DiscordWR: Discord Webhook Reader

**Made By XGFZOfficial** | [Find me on GitHub](https://github.com/XGFZOfficial)

## Table of Contents

- [Overview](#overview)
- [Files](#files)
- [How to Set Up Your Discord Bot](#how-to-set-up-your-discord-bot)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

DiscordWR allows you to easily monitor and read incoming webhook messages from a designated Discord channel.

## Files

1. `Bot_gui.py`: The core code of the application (not the main executable file).
2. `Bot_settings.json`: Stores settings, like the "Remember Me" option.
3. `DiscordWR.bat`: The main executable file; run this to launch the app.
4. `README.txt`: (This file) Provides instructions and information about the project.

## How to Set Up Your Discord Bot

1. Go to the Discord Developer Portal: [https://discord.com/developers/applications](https://discord.com/developers/applications) and log in to your Discord account.

2. In the top right, click **New Application** and give your new application a name (this will also be your bot's username).

3. On the left sidebar, click the menu icon (three stacked lines) and then click **Bot**.

4. Enable the following intents:
    * Presence Intent
    * Server Members Intent
    * Message Content Intent

5. Go back to the sidebar and click **OAuth2**.
    * Under **OAuth2 URL Generator**:
        * For **Scopes**, select **bot**.
        * For **Bot Permissions**, select **Administrator**.
    * Scroll down and copy the generated URL. Visit this URL in your browser to add the bot to your server.

6. Go back to the sidebar and click **Bot**.
    * You can change the username if desired.
    * Under **Token**, click **Reset Token** and then copy your token (keep it safe and never share it).

7. **Get the Channel ID:**
    * Open Discord, right-click on the channel you want to receive messages from, and click **Copy Channel ID**. (The channel must be in the same server where you added the bot.)

## Installation

1. Download or clone this repository to your local machine.
2. Make sure you have Python installed.
3. Install any required dependencies (if applicable): `pip install -r requirements.txt` 

## Usage

1. **Launch DiscordWR:**
    * Double-click on `DiscordWR.bat`.
    * Enter your token and channel ID into the app.
    * Click **Start**.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the [UNLicense](LICENSE). 

## Enjoy!

If you have any questions or run into issues, feel free to reach out or open an issue on GitHub.

**XGFZTeam**
