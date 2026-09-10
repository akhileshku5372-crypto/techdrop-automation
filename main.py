import urllib.request
import urllib.parse
import json
import random

BOT_TOKEN = "8955674704:AAGfa0olCPtJP4y1UXUw6TsZH7jLm-2TacQ"
MY_CHAT_ID = "7007988430"
CHANNEL_ID = "@techdrop24_daily"
GROQ_API_KEY = "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"

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

def generate_post_groq(tool_name, tool_desc, tool_link):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    prompt = (
        f"Create a short, engaging 3-line Telegram post about this tech tool:\n"
        f"Name: {tool_name}\n"
        f"Description: {tool_desc}\n"
        f"Link: {tool_link}\n\n"
        "Format strictly:\n"
        "🔥 [Tool Name]\n\n"
        "💡 What it does: (1 line summary)\n\n"
        "🎯 Why use it: (1 clear benefit for developers/students)\n\n"
        f"🔗 Link: {tool_link}"
    )
    
    body = {
        "model": "llama-3.1-8b-instant",",
        "messages": [
            {"role": "system", "content": "You write crisp, high-value tech updates for Telegram channels. No intro fluff, no closing remarks."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq API Error: {e}")
        return None

tools = [
    {"name": "FastAPI", "desc": "High performance, easy to learn web framework for APIs in Python.", "link": "https://fastapi.tiangolo.com/"},
    {"name": "v0 by Vercel", "desc": "Generative UI system that builds modern frontend components from plain English prompts.", "link": "https://v0.dev/"},
    {"name": "Open-WebUI", "desc": "Extensible, self-hosted web interface that runs local AI models offline.", "link": "https://openwebui.com/"},
    {"name": "Ollama", "desc": "Tool to run large language models locally on your computer with a single command.", "link": "https://ollama.com/"},
    {"name": "Supabase", "desc": "Open source Firebase alternative providing PostgreSQL database and instant APIs.", "link": "https://supabase.com/"}
]

item = random.choice(tools)
ai_post = generate_post_groq(item["name"], item["desc"], item["link"])

if not ai_post:
    ai_post = f"🔥 {item['name']}\n\n💡 What it does: {item['desc']}\n\n🔗 Link: {item['link']}"

final_post = f"{ai_post}\n\n📌 Follow: @techdrop24_daily"

print("Sending post to channel...")
send_telegram(CHANNEL_ID, final_post)
print("Sending alert to personal chat...")
send_telegram(MY_CHAT_ID, f"✅ Groq AI Post Delivered: {item['name']}")
