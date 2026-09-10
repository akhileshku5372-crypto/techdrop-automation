import os
import requests
from datetime import datetime
from groq import Groq
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Groq Client Setup
client = Groq(api_key="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")

def fetch_live_github_trends():
    """Internet / GitHub se live top 5 trending tech & AI repos nikalta hai"""
    print("Fetching live trending repositories from GitHub API...")
    url = "https://api.github.com/search/repositories?q=stars:>100+pushed:>2026-01-01&sort=stars&order=desc&per_page=5"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "TechDrop-Bot"}
    
    repo_summary = []
    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code == 200:
            items = res.json().get("items", [])
            for item in items:
                name = item.get("name", "Unknown")
                desc = item.get("description", "No description provided")
                stars = item.get("stargazers_count", 0)
                link = item.get("html_url", "")
                repo_summary.append(f"Repo: {name} (Stars: {stars})\nURL: {link}\nDescription: {desc}\n")
    except Exception as e:
        print("GitHub fetch fallback:", e)

    # Agar GitHub rate-limit ho, toh live Hacker News API se tech items lo
    if not repo_summary:
        print("Fetching from live Hacker News Tech Feed...")
        hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        ids = requests.get(hn_url, timeout=10).json()[:5]
        for item_id in ids:
            item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", timeout=10).json()
            title = item.get("title", "")
            url = item.get("url", "https://news.ycombinator.com")
            repo_summary.append(f"Tech Trend: {title}\nURL: {url}\n")
            
    return "\n---\n".join(repo_summary)

def analyze_with_ai(live_scraped_data):
    """Live internet data ko actionable developer cheatsheet me convert karta hai"""
    print("Processing live internet data with Groq...")
    prompt = f"""
    Here is LIVE TRENDING data fetched directly from GitHub and Developer feeds today:
    
    {live_scraped_data}
    
    Based ONLY on this live developer data, build an elite, professional report titled 'DAILY GITHUB & AI TRENDS BLUEPRINT'.
    
    Structure:
    1. TOP LIVE TRENDING TOOLS (Break down each repository/tool, its core architecture, and why developers are starring it today).
    2. HOW TO USE & AUTOMATE (Provide concrete code commands or terminal setup for these trending tools).
    3. KEY TAKEAWAYS FOR DEVELOPERS (Actionable advice to leverage these technologies).
    
    STRICT RULES:
    - Do NOT use markdown symbols like * or # or backticks.
    - Keep bullet points as simple dashes (-).
    - Give rich, practical explanation with no fluff.
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2200
    )
    return completion.choices[0].message.content

def sanitize_text(text):
    replacements = {
        '“': '"', '”': '"', '‘': "'", '’': "'",
        '•': '-', '—': '-', '–': '-', '…': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

class LiveBlueprintPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, "24TECHDROP | LIVE INTERNET & GITHUB PULSE", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"Page {self.page_no()} | Realtime Verified Tech Drop", align="C")

def build_pdf(content):
    pdf = LiveBlueprintPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pw = pdf.epw
    date_str = datetime.now().strftime("%d %B %Y")
    
    # Title Section
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(pw, 9, "Daily GitHub & AI Trends Blueprint", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(pw, 5, f"Live Scraped from GitHub API & Developer Feeds ({date_str})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)
    
    clean_content = sanitize_text(content)
    
    for line in clean_content.split("\n"):
        line_str = line.strip()
        if not line_str:
            pdf.ln(2)
            continue
            
        # Headers highlight
        if line_str[0].isdigit() and len(line_str) > 1 and (line_str[1] in [".", ")"] or (len(line_str) > 2 and line_str[2] in [".", ")"])):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(2, 132, 199)
            pdf.cell(pw, 7, line_str, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        else:
            pdf.set_font("Helvetica", size=9)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(pw, 5, line_str, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
    filename = "digital_product.pdf"
    pdf.output(filename)
    print("PDF Successfully Built with LIVE Data:", filename)
    return filename

if __name__ == "__main__":
    live_data = fetch_live_github_trends()
    ai_content = analyze_with_ai(live_data)
    build_pdf(ai_content)
    
