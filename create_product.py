import os
import json
import zipfile
import requests
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from groq import Groq

# Purani working API key aur tokens
client = Groq(api_key="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")
BOT_TOKEN = os.environ.get("8955674704:AAGfa0olCPtJP4y1UXUw6TsZH7jLm-2TacQ")
CHANNEL_CHAT_ID = os.environ.get("7007988430")

def fetch_live_problem():
    """Hacker News API se real-world human/tech problem dhundhta hai"""
    try:
        url = "https://hn.algolia.com/api/v1/search?query=how%20to%20automate&tags=story&hitsPerPage=3"
        res = requests.get(url, timeout=10).json()
        story = res.get("hits", [])[0]
        return story.get("title", "Automating Daily Repetitive Workflows")
    except Exception:
        return "Automating Daily Repetitive Workflows"

def generate_multi_asset_product(problem_title):
    print(f"Generating digital assets for: {problem_title}")
    prompt = f"""
    Create a complete multi-format digital utility kit that solves this real problem: "{problem_title}".
    
    Output strictly in this JSON format with 3 keys:
    1. "guide_markdown": A simple, friendly, jargon-free markdown guide explaining the solution for both non-tech and tech humans.
    2. "code_script": A fully functional, production-ready Python or shell script that actually automates the solution.
    3. "prompt_pack": 5 practical, copy-paste AI system prompts that solve related sub-problems.
    
    JSON format:
    {{
      "guide_markdown": "content here",
      "code_script": "content here",
      "prompt_pack": "content here"
    }}
    Ensure valid raw JSON only.
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

def build_pdf_summary(problem_title, guide_text):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(pdf.epw, 10, "24TECHDROP PRO BUNDLE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(pdf.epw, 6, f"Problem Solved: {problem_title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(30, 30, 30)
    safe_text = guide_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(pdf.epw, 5, safe_text[:1800], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf_filename = "quick_overview.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

def package_bundle(assets, problem_title):
    # 1. Save Markdown Guide
    with open("GUIDE.md", "w", encoding="utf-8") as f:
        f.write(f"# Solution: {problem_title}\n\n" + assets.get("guide_markdown", ""))
        
    # 2. Save Executable Script / Template
    with open("automation_tool.py", "w", encoding="utf-8") as f:
        f.write(assets.get("code_script", "# Automation code"))
        
    # 3. Save AI Prompts
    with open("PROMPT_PACK.txt", "w", encoding="utf-8") as f:
        f.write(assets.get("prompt_pack", ""))
        
    # 4. Generate PDF
    pdf_file = build_pdf_summary(problem_title, assets.get("guide_markdown", ""))
    
    # 5. Make complete ZIP Bundle (The Real Digital Product)
    zip_filename = "digital_power_pack.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write("GUIDE.md")
        zipf.write("automation_tool.py")
        zipf.write("PROMPT_PACK.txt")
        zipf.write(pdf_file)
        
    print(f"Digital Product Bundle created: {zip_filename}")
    return zip_filename

def notify_channel(problem_title):
    if not BOT_TOKEN or not CHANNEL_CHAT_ID:
        return
    caption = f"""🔥 **NEW DIGITAL UTILITY DROP!**

📦 **Product Bundle:** `{problem_title}`
Includes:
- 🛠 Ready-to-Run Automation Script (`.py`)
- 🤖 5x High-Impact AI Prompt Templates
- 📖 Beginner-to-Pro Action Guide (`.md`)
- 📄 Quick Visual Overview (`.pdf`)

💰 **Unlock Full Power Pack for ₹29**
👉 Direct instant bundle access for developers and builders."""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CHANNEL_CHAT_ID,
            "text": caption,
            "parse_mode": "Markdown"
        }, timeout=10)
        print("Telegram alert sent!")
    except Exception as e:
        print("Telegram notification failed:", e)

if __name__ == "__main__":
    problem = fetch_live_problem()
    product_assets = generate_multi_asset_product(problem)
    bundle_zip = package_bundle(product_assets, problem)
    notify_channel(problem)
