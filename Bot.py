import os
import time
import signal
import subprocess
import traceback
import threading
from threading import Lock

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================
BOT_TOKEN = "8424462856:AAFONSWQLCi7XjqxqWIcoGvA7nyQyH3Ypl4"
BASE_DIR = "bots"
os.makedirs(BASE_DIR, exist_ok=True)

bots = {}  # bots[user_id][bot_id] = info
bots_lock = Lock()

# ================= KEYBOARD =================
MAIN_KB = ReplyKeyboardMarkup(
    [
        ["➕ Add Bot", "📋 My Bots"],
        ["📊 Status", "📜 Logs"],
        ["⛔ Kill Bot"]
    ],
    resize_keyboard=True,
    is_persistent=True
)

# ================= UTILS =================
def kill_process_tree(pid: int):
    try:
        os.killpg(os.getpgid(pid), signal.SIGKILL)
    except:
        pass

async def send_error(msg):
    tb = traceback.format_exc()
    await msg.reply_text(
        "❌ *ERROR*\n\n```" + tb[:3500] + "```",
        parse_mode="Markdown",
        reply_markup=MAIN_KB
    )

# ================= AUTO-RESTART MONITOR =================
def monitor_loop():
    while True:
        try:
            with bots_lock:
                for uid, user_bots in bots.items():
                    for bid, info in user_bots.items():
                        p = info["process"]
                        if p.poll() is not None:  # crashed
                            try:
                                new_p = subprocess.Popen(
                                    ["python", info["path"]],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,  # 🔥 FIX
                                    start_new_session=True
                                )
                                info["process"] = new_p
                                info["start"] = time.time()
                                info["restarts"] += 1
                                info["last_error"] = "Auto-restarted after crash"
                            except Exception as e:
                                info["last_error"] = f"Restart failed: {e}"
        except Exception as e:
            print("Monitor loop error:", e)

        time.sleep(5)

threading.Thread(target=monitor_loop, daemon=True).start()

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Bot Host Manager*\n\n"
        "• Sirf `bot.py` upload supported\n"
        "• Multiple bots allowed\n"
        "• Auto-restart enabled",
        parse_mode="Markdown",
        reply_markup=MAIN_KB
    )

# ================= TEXT HANDLER =================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id

    try:
        if text == "➕ Add Bot":
            context.user_data.clear()
            context.user_data["step"] = "name"
            await update.message.reply_text(
                "📝 Bot ka *NAME* bhejo",
                parse_mode="Markdown",
                reply_markup=MAIN_KB
            )

        elif text == "📋 My Bots":
            with bots_lock:
                user_bots = bots.get(uid, {})

            if not user_bots:
                await update.message.reply_text("❌ Koi bot nahi", reply_markup=MAIN_KB)
                return

            msg = "🤖 *My Bots*\n\n"
            for bid, info in user_bots.items():
                uptime = int(time.time() - info["start"])
                msg += (
                    f"• *{info['name']}*\n"
                    f"  ID: `{bid}`\n"
                    f"  ⏱ {uptime}s | 🔁 {info['restarts']}\n\n"
                )

            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=MAIN_KB)

        elif text == "📊 Status":
            with bots_lock:
                count = sum(len(v) for v in bots.values())

            await update.message.reply_text(
                f"📊 *Status*\n\n"
                f"Running bots: `{count}`\n"
                f"Auto-restart: ✅ ON",
                parse_mode="Markdown",
                reply_markup=MAIN_KB
            )

        elif text == "📜 Logs":
            with bots_lock:
                user_bots = bots.get(uid, {})

            if not user_bots:
                await update.message.reply_text("❌ No logs", reply_markup=MAIN_KB)
                return

            msg = "📜 *Logs*\n\n"
            for info in user_bots.values():
                msg += f"• *{info['name']}*: {info['last_error']}\n"

            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=MAIN_KB)

        elif text == "⛔ Kill Bot":
            context.user_data["step"] = "kill"
            await update.message.reply_text(
                "🆔 Bot *ID* bhejo",
                parse_mode="Markdown",
                reply_markup=MAIN_KB
            )

        elif context.user_data.get("step") == "name":
            context.user_data["bot_name"] = text
            context.user_data["step"] = "upload"
            await update.message.reply_text(
                "📂 Ab *bot.py* file upload karo",
                parse_mode="Markdown",
                reply_markup=MAIN_KB
            )

        elif context.user_data.get("step") == "kill":
            bid = text.strip()

            with bots_lock:
                info = bots.get(uid, {}).get(bid)

            if not info:
                await update.message.reply_text("❌ Invalid bot ID", reply_markup=MAIN_KB)
                return

            kill_process_tree(info["process"].pid)

            with bots_lock:
                bots[uid].pop(bid)

            context.user_data.clear()
            await update.message.reply_text(
                f"⛔ Bot *{info['name']}* stopped",
                parse_mode="Markdown",
                reply_markup=MAIN_KB
            )

        else:
            await update.message.reply_text("⬇️ Keyboard se option chuno", reply_markup=MAIN_KB)

    except Exception:
        await send_error(update.message)

# ================= FILE HANDLER =================
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if context.user_data.get("step") != "upload":
            await update.message.reply_text(
                "⚠️ Pehle ➕ Add Bot use karo",
                reply_markup=MAIN_KB
            )
            return

        uid = update.effective_user.id
        bot_id = f"bot{int(time.time())}"
        folder = f"{BASE_DIR}/{uid}"
        os.makedirs(folder, exist_ok=True)

        path = f"{folder}/{bot_id}.py"
        file = await update.message.document.get_file()
        await file.download_to_drive(path)

        p = subprocess.Popen(
            ["python", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,  # 🔥 FIX
            start_new_session=True
        )

        with bots_lock:
            bots.setdefault(uid, {})[bot_id] = {
                "name": context.user_data["bot_name"],
                "process": p,
                "path": path,
                "start": time.time(),
                "restarts": 0,
                "last_error": "Started successfully"
            }

        context.user_data.clear()

        await update.message.reply_text(
            f"🚀 Bot started\n"
            f"📛 Name: {bots[uid][bot_id]['name']}\n"
            f"🆔 ID: `{bot_id}`",
            parse_mode="Markdown",
            reply_markup=MAIN_KB
        )

    except Exception:
        await send_error(update.message)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    print("🔥 BOT HOST MANAGER STARTED (STABLE MODE)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
