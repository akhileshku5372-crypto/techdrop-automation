import urllib.request
import urllib.parse
import json
import random

BOT_TOKEN = "8955674704:AAFEP21NawmtKsbT4G3sZD0Pr1vzfZk7S96g"
MY_CHAT_ID = "7007988430"
CHANNEL_ID = "@techdrop24_daily"
GEMINI_API_KEY = "AQ.Ab8RN6K7GWGM-1iRIOjea0a8-iHnWd2-hqbWk4m9JU6WaKRoJA"

def send_telegram(chat_target, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_target, "text": message}
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode("utf-8"))
            print(f"Delivered to {chat_target}: {res.get('ok')}")
            return True
    except urllib.error.HTTPError as e:
        error_content = e.read().decode("utf-8")
        print(f"Telegram Delivery Failed to {chat_target}: Status {e.code} -> {error_content}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def generate_post(topic_data):
    for model_name in ["gemini-1.5-flash", "gemini-2.0-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            prompt = (
                f"Write a crisp 3-line Telegram post about this tool: {topic_data}.\n"
                "Line 1: Tool name with an emoji.\n"
                "Line 2: What it solves.\n"
                "Line 3: Official Link.\n"
                "Keep it short, clean, no boilerplate intros."
            )
            body = {"contents": [{"parts": [{"text": prompt}]}]}
            req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as err:
            print(f"Gemini API attempt failed: {err}")
            continue
    return None

tools = [
    {"name": "FastAPI", "desc": "Ultra-fast modern Python framework for building production APIs.", "link": "https://fastapi.tiangolo.com/"},
    {"name": "v0 by Vercel", "desc": "AI system to generate modern frontend web components.", "link": "https://v0.dev/"},
    {"name": "Open-WebUI", "desc": "Offline self-hosted UI for running local AI models.", "link": "https://openwebui.com/"},
    {"name": "Ollama", "desc": "Run open source LLMs locally with simple commands.", "link": "https://ollama.com/"}
]

item = random.choice(tools)
raw_info = f"Name: {item['name']}, Info: {item['desc']}, URL: {item['link']}"

content = generate_post(raw_info)
if not content:
    content = f"🔥 {item['name']}\n💡 {item['desc']}\n🔗 Link: {item['link']}"

final_post = f"{content}\n\n📌 Follow: @techdrop24_daily"

print("Sending post to channel...")
send_telegram(CHANNEL_ID, final_post)
print("Sending alert to personal chat...")
send_telegram(MY_CHAT_ID, f"Test alert: Attempted to post {item['name']}")
