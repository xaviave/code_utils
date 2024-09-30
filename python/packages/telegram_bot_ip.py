import subprocess
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parse and send the ip address of the computer via a telegram bot"""
    resp = subprocess.check_output(['ifconfig']).decode('ascii').replace("\r","")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"I'm the rasp, this is the iconfig {resp}")

if __name__ == '__main__':
    token: str = ""  # add your telegram token
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
