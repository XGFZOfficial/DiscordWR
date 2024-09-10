#!/usr/bin/env python3

import asyncio
import sys
import logging
from PyQt5 import QtWidgets, QtCore
import discord
from discord.ext import commands
import threading
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Default values (replace with your actual defaults or leave empty)
DEFAULT_TOKEN = ""
DEFAULT_CHANNEL_ID = ""

# File to store saved settings
SETTINGS_FILE = "bot_settings.json"

class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui_window = None

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        if self.gui_window:
            self.gui_window.bot_ready_signal.emit()

    async def on_message(self, message):
        if message.channel.id == self.gui_window.channel_id and message.content:  # Use channel_id from GUI
            print(f'Message from {message.author}: {message.content}')
            if self.gui_window:
                self.gui_window.update_text(f'Message from {message.author}: {message.content}')


class BotWindow(QtWidgets.QWidget):
    bot_ready_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.load_settings()
        self.init_ui()
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = DiscordBot(command_prefix='!', intents=intents)
        self.bot.gui_window = self
        self.loop = asyncio.get_event_loop()
        self.bot_thread = None  # Track bot thread

        self.bot_ready_signal.connect(self.on_bot_ready)

    def init_ui(self):
        self.setWindowTitle('DiscordWR')
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        # Token input
        token_label = QtWidgets.QLabel("Bot Token:")
        self.token_input = QtWidgets.QLineEdit(self)
        self.token_input.setText(self.token)
        layout.addWidget(token_label)
        layout.addWidget(self.token_input)

        # Channel ID input
        channel_id_label = QtWidgets.QLabel("Channel ID:")
        self.channel_id_input = QtWidgets.QLineEdit(self)
        self.channel_id_input.setText(str(self.channel_id))
        layout.addWidget(channel_id_label)
        layout.addWidget(self.channel_id_input)

        # Remember me checkbox
        self.remember_me_checkbox = QtWidgets.QCheckBox("Remember Me", self)
        self.remember_me_checkbox.setChecked(self.remember_me)
        layout.addWidget(self.remember_me_checkbox)

        # Start/Stop button
        self.start_stop_button = QtWidgets.QPushButton("Start Bot", self)
        self.start_stop_button.clicked.connect(self.toggle_bot)
        layout.addWidget(self.start_stop_button)

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def update_text(self, message):
        logging.debug(f"Received message: {message}")
        self.text_edit.append(message)

    def toggle_bot(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        self.token = self.token_input.text()
        try:
            self.channel_id = int(self.channel_id_input.text())
        except ValueError:
            logging.error("Invalid Channel ID. Please enter a number.")
            return

        self.remember_me = self.remember_me_checkbox.isChecked()
        self.save_settings()

        self.bot_thread = threading.Thread(target=self._run_bot_in_thread, daemon=True)
        self.bot_thread.start()
        self.start_stop_button.setText("Stop Bot")

    def stop_bot(self):
        if self.bot.is_closed():
            return
        self.bot.loop.call_soon_threadsafe(self.bot.loop.stop)
        self.bot_thread.join()
        self.bot_thread = None
        self.start_stop_button.setText("Start Bot")
        self.update_text("🔴 Bot Stopped")

    def _run_bot_in_thread(self):
        self.bot_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.bot_loop)

        # Create a future to wait for the bot to be ready
        self.bot_ready_future = asyncio.Future()

        # Schedule the bot's startup coroutine
        asyncio.ensure_future(self._start_bot(), loop=self.bot_loop)

        # Run the bot's event loop until the bot is ready
        self.bot_loop.run_until_complete(self.bot_ready_future)

    async def _start_bot(self):
        try:
            logging.debug("Starting bot...")
            await self.bot.start(self.token)  # Use self.token instead of TOKEN

            # Signal that the bot is ready
            self.bot_ready_future.set_result(True)

        except discord.LoginFailure:
            logging.error("Invalid token. Please check your token and try again.")
        except discord.HTTPException as e:
            logging.error(f"An error occurred while connecting to Discord: {e}")
        except asyncio.CancelledError:
            logging.warning("Bot startup was cancelled.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def closeEvent(self, event):
        if hasattr(self, 'bot_ready_future') and not self.bot_ready_future.done():
            self.bot_ready_future.cancel()

        if hasattr(self, 'bot_loop'):
            self.bot_loop.call_soon_threadsafe(self.bot_loop.stop)
            self.bot_thread.join()
        super().closeEvent(event)

    def showEvent(self, event):
        """This method is called when the window is shown."""
        super().showEvent(event)

    def on_bot_ready(self):
        self.update_text("🟢 Bot is Ready")

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                self.token = settings.get('token', DEFAULT_TOKEN)
                self.channel_id = settings.get('channel_id', DEFAULT_CHANNEL_ID)
                self.remember_me = settings.get('remember_me', False)
        except FileNotFoundError:
            self.token = DEFAULT_TOKEN
            self.channel_id = DEFAULT_CHANNEL_ID
            self.remember_me = False

    def save_settings(self):
        if self.remember_me:
            settings = {
                'token': self.token,
                'channel_id': self.channel_id,
                'remember_me': self.remember_me
            }
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f)

def set_dark_theme(app):
    dark_theme = """
        QWidget {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QTextEdit {
            background-color: #1E1E1E;
            color: #FFFFFF;
            border: 1px solid #4A4A4A;
        }
        QPushButton {
            background-color: #3E3E3E;
            color: #FFFFFF;
            border: 1px solid #4A4A4A;
        }
        QPushButton:pressed {
            background-color: #5A5A5A;
        }
    """
    app.setStyleSheet(dark_theme)

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Apply dark theme to the application
    set_dark_theme(app)

    window = BotWindow()
    window.show()

    exit_code = app.exec()
    return exit_code

if __name__ == '__main__':
    main()
