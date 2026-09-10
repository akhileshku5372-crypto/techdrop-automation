import urllib.request
import urllib.parse
import json
import random

BOT_TOKEN = "8955674704:AAGfa0olCPtJP4y1UXUw6TsZH7jLm-2TacQ"
MY_CHAT_ID = "7007988430"
CHANNEL_ID = "@techdrop24_daily"
GROQ_API_KEY = "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"
SHRINKEARN_API_TOKEN = "c60682bb4d8cc7c9f2fc1657a0d2ec020243c1c7"

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
        print(f"Unexpected Telegram error: {e}")
        return False

def shorten_link(original_url):
    try:
        encoded_url = urllib.parse.quote(original_url)
        api_url = f"https://shrinkearn.com/api?api={SHRINKEARN_API_TOKEN}&url={encoded_url}"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") == "success" and data.get("shortenedUrl"):
                print("Link shortened successfully.")
                return data.get("shortenedUrl")
    except Exception as e:
        print(f"Shortener error (using original): {e}")
    return original_url

def generate_post_groq(tool_name, tool_desc, tool_link):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    prompt = (
        f"Create a short, engaging Telegram post about this tool:\n"
        f"Name: {tool_name}\n"
        f"Description: {tool_desc}\n\n"
        "Format strictly:\n"
        f"🔥 {tool_name}\n\n"
        "💡 What it does: (1 line summary)\n\n"
        "🎯 Best for: (developers, creators, or students)\n\n"
        f"🔗 Get Tool Link: {tool_link}\n\n"
        "📌 Follow: @techdrop24_daily"
    )
    
    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a professional tech curator. Output only the requested formatted Telegram post."},
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
    {"name": "FastAPI", "desc": "High performance web framework for building APIs with Python.", "link": "https://fastapi.tiangolo.com/"},
    {"name": "v0 by Vercel", "desc": "AI system to build modern web interfaces from prompts.", "link": "https://v0.dev/"},
    {"name": "Open-WebUI", "desc": "Offline self-hosted UI for running open source LLMs locally.", "link": "https://openwebui.com/"},
    {"name": "Ollama", "desc": "Run open source AI models locally with single command setup.", "link": "https://ollama.com/"},
    {"name": "Supabase", "desc": "Open source Firebase alternative with Postgres database.", "link": "https://supabase.com/"},
    {"name": "Cursor Editor", "desc": "AI-first code editor designed to write code 10x faster.", "link": "https://www.cursor.com/"},
    {"name": "Hugging Face Spaces", "desc": "Host ML models and frontend demos for free.", "link": "https://huggingface.co/spaces"}
]

item = random.choice(tools)

# Step 1: Auto-monetize link via ShrinkEarn
monetized_url = shorten_link(item["link"])

# Step 2: Generate clean post with Groq AI
post_content = generate_post_groq(item["name"], item["desc"], monetized_url)

if not post_content:
    post_content = (
        f"🔥 {item['name']}\n\n"
        f"💡 What it does: {item['desc']}\n\n"
        f"🔗 Get Tool Link: {monetized_url}\n\n"
        f"📌 Follow: @techdrop24_daily"
    )

print("Sending post to channel...")
send_telegram(CHANNEL_ID, post_content)

print("Sending alert to personal chat...")
send_telegram(MY_CHAT_ID, f"✅ Monetized Post Live: {item['name']}")
