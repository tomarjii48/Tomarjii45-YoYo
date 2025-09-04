import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from flask import Flask, request, jsonify, render_template
import requests
from gtts import gTTS
from fpdf import FPDF
import wikipedia

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

app = Flask(__name__)

# ---------------- Telegram Handlers ----------------

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply("Hello! AI Bot is ready. Ask me anything or use commands.")

@dp.message_handler(commands=['notes'])
async def notes_cmd(message: types.Message):
    with open("data/notes.json","r") as f:
        notes=json.load(f)
    reply="\n".join([f"{k}: {v}" for k,v in notes.items()]) or "No notes yet."
    await message.reply(reply)

@dp.message_handler()
async def echo_all(message: types.Message):
    text=message.text
    # Wikipedia example
    try:
        summary = wikipedia.summary(text, sentences=2)
        await message.reply(f"Wikipedia: {summary}")
    except:
        await message.reply(f"AI: Sorry, couldn't find info. You said: {text}")

# ---------------- Flask Web ----------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webchat', methods=['POST'])
def webchat():
    data=request.get_json()
    text=data.get('text')
    # Simple echo for demo
    return jsonify({"reply": f"AI: You said '{text}'"})

@app.route('/upload', methods=['POST'])
def upload_file():
    file=request.files['file']
    if not os.path.exists('data/uploads'):
        os.makedirs('data/uploads')
    filepath=os.path.join('data/uploads', file.filename)
    file.save(filepath)
    return jsonify({"filename": file.filename})

if __name__=="__main__":
    port = int(os.environ.get("PORT", 8080))
    from threading import Thread
    # Run Flask in background
    Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
    # Run Telegram bot
    executor.start_polling(dp, skip_updates=True)
