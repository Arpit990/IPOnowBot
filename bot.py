import requests
import time
import os
from threading import Thread
from flask import Flask

app = Flask(__name__)

# Replace with your bot token from BotFather
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text, buttons=None):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "MarkdownV2"
    }

    if buttons:
        keyboard = [[{"text": btn}] for btn in buttons]
        payload["reply_markup"] = json.dumps({
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": False
        })

    requests.post(url, data=payload)

def get_mainboard_current_ipos():
    return (
        "📊 *Mainboard IPOs \\- Current*  \n\n"
        "1\\. *ABC Industries Ltd*  \n"
        "📅 Open: 25 Sep 2025  \n"
        "📅 Close: 28 Sep 2025  \n"
        "💰 Price Band: ₹120 \\- ₹130  \n"
        "🔗 [View Details](https://example.com/ipo/abc)\n\n"
        "2\\. *XYZ Tech Pvt Ltd*  \n"
        "📅 Open: 26 Sep 2025  \n"
        "📅 Close: 30 Sep 2025  \n"
        "💰 Price Band: ₹90 \\- ₹95  \n"
        "🔗 [View Details](https://example.com/ipo/xyz)"
    )

def get_mainboard_upcoming_ipos():
    return (
        "🗓️ *Mainboard IPOs \\- Upcoming*  \n\n"
        "1\\. *NextGen Solutions Ltd*  \n"
        "📅 Opens: 2 Oct 2025  \n"
        "💰 Expected Price: ₹150  \n"
        "🔗 [View Details](https://example.com/ipo/nextgen)"
    )

def get_mainboard_closed_ipos():
    return (
        "📁 *Mainboard IPOs \\- Recently Closed*  \n\n"
        "1\\. *MegaCorp Ltd*  \n"
        "📅 Closed: 20 Sep 2025  \n"
        "💰 Final Price: ₹105  \n"
        "📈 Listing Date: 27 Sep 2025  \n"
        "🔗 [View Details](https://example.com/ipo/megacorp)"
    )

def get_sme_current_ipos():
    return (
        "📊 *SME IPOs \\- Current*  \n\n"
        "1\\. *GreenTech Innovations*  \n"
        "📅 Open: 27 Sep 2025  \n"
        "📅 Close: 1 Oct 2025  \n"
        "💰 Price Band: ₹50 \\- ₹55  \n"
        "🔗 [View Details](https://example.com/ipo/greentech)"
    )

def get_sme_upcoming_ipos():
    return (
        "🗓️ *SME IPOs \\- Upcoming*  \n\n"
        "1\\. *AgroLife Pvt Ltd*  \n"
        "📅 Opens: 3 Oct 2025  \n"
        "💰 Expected Price: ₹65  \n"
        "🔗 [View Details](https://example.com/ipo/agrolife)"
    )

def get_sme_closed_ipos():
    return (
        "📁 *SME IPOs \\- Recently Closed*  \n\n"
        "1\\. *EduSmart Ltd*  \n"
        "📅 Closed: 22 Sep 2025  \n"
        "💰 Final Price: ₹75  \n"
        "📈 Listing Date: 29 Sep 2025  \n"
        "🔗 [View Details](https://example.com/ipo/edusmart)"
    )

@app.route('/')
def health_check():
    return "IPOnowBot is running!"

def run_bot():
    offset = None
    print("Bot is running...")
   
    while True:
        try:
            updates = get_updates(offset)
            
            if updates["ok"]:
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        message_text = update["message"].get("text", "")
                        
                        # Simple echo bot - responds with the same message
                        if message_text:
                          if message_text == "/start":
                            welcome_text = (
                                "👋 *Welcome to IPO Info Bot\\!* \n\n"
                                "Stay updated with the latest *Mainboard* and *SME* IPOs in India\\.\n"
                                "Browse IPOs by category and status using the options below:"
                            )
    
                            buttons = [
                                "Mainboard: Current IPOs",
                                "Mainboard: Upcoming IPOs",
                                "Mainboard: Closed IPOs",
                                "SME: Current IPOs",
                                "SME: Upcoming IPOs",
                                "SME: Closed IPOs"
                            ]
                            send_message(chat_id, welcome_text, buttons)
                          
                          elif message_text == "Mainboard: Current IPOs":
                              send_message(chat_id, get_mainboard_current_ipos())
    
                          elif message_text == "Mainboard: Upcoming IPOs":
                              send_message(chat_id, get_mainboard_upcoming_ipos())
    
                          elif message_text == "Mainboard: Closed IPOs":
                              send_message(chat_id, get_mainboard_closed_ipos())
    
                          elif message_text == "SME: Current IPOs":
                              send_message(chat_id, get_sme_current_ipos())
    
                          elif message_text == "SME: Upcoming IPOs":
                              send_message(chat_id, get_sme_upcoming_ipos())
    
                          elif message_text == "SME: Closed IPOs":
                              send_message(chat_id, get_sme_closed_ipos())
                          else:
                              send_message(chat_id, f"You said: {message_text}")

            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

def main():
    # Start bot in background thread
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start Flask web server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
