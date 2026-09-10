import os
import random
import requests
from datetime import datetime, timedelta
from groq import Groq
from fpdf import FPDF
from fpdf.enums import XPos, YPos

client = Groq(api_key="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")

# Curated High-Velocity Trending Topics
TOPICS = [
    "ai agent framework autonomous",
    "llm local inference api",
    "developer workflow automation cli",
    "fastapi backend system prompts",
    "docker kubernetes optimization"
]

def fetch_breakout_trends():
    topic = random.choice(TOPICS)
    # Sirf pichhle 14 din ke breakout repos
    two_weeks_ago = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    print(f"Scraping fresh breakout tools: {topic} (Since: {two_weeks_ago})")
    
    url = f"https://api.github.com/search/repositories?q={topic}+created:>{two_weeks_ago}&sort=stars&order=desc&per_page=4"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "TechDrop-Bot"}
    
    repo_summary = []
    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code == 200:
            items = res.json().get("items", [])
            for item in items:
                name = item.get("name", "Unknown")
                desc = item.get("description") or "Production tooling and framework."
                stars = item.get("stargazers_count", 0)
                link = item.get("html_url", "")
                repo_summary.append(f"TOOL: {name} (Stars: {stars})\nURL: {link}\nSUMMARY: {desc}\n")
    except Exception as e:
        print("GitHub fetch fallback:", e)

    if not repo_summary:
        repo_summary.append(
            "TOOL: vLLM-Inference-Engine\nURL: https://github.com/vllm-project/vllm\nSUMMARY: High-throughput and memory-efficient LLM serving engine with PagedAttention.\n"
        )
        repo_summary.append(
            "TOOL: Open-Devin-Agent\nURL: https://github.com/OpenDevin/OpenDevin\nSUMMARY: Autonomous AI software engineer capable of executing complex code tasks.\n"
        )
            
    return topic, "\n---\n".join(repo_summary)

def generate_pro_analysis(topic, live_data):
    prompt = f"""
    You are a Lead Principal Engineer authoring an internal VIP developer intel briefing.
    Live Scraped Data:
    {live_data}
    
    Write a high-value technical cheatsheet titled '24TECHDROP PRO INTEL: {topic.upper()}'.
    
    Strictly format into 3 sections:
    
    [SECTION 1] ARCHITECTURE BREAKDOWN
    For each tool, give a 2-sentence breakdown of its internal mechanics and why it outperforms traditional methods.
    
    [SECTION 2] PRODUCTION SNIPPETS & WORKFLOWS
    Provide 3 concrete, high-density code snippets, Docker commands, or shell automation pipelines related to these technologies. Do NOT just give 'git clone' or 'cd'. Provide real production configurations.
    
    [SECTION 3] SENIOR ENGINEER ACTION PLAN
    3 hard-hitting recommendations on optimizing memory, caching, or execution speed using these stacks.
    
    RULES:
    - Never output raw markdown markers (* or # or backticks `).
    - Use clean indentation and dashes (-) for bullets.
    - Write dense, professional, authoritative content.
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2200
    )
    return completion.choices[0].message.content

def sanitize(text):
    replacements = {
        '“': '"', '”': '"', '‘': "'", '’': "'",
        '•': '-', '—': '-', '–': '-', '`': '', '*': ''
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

class ProTechPDF(FPDF):
    def header(self):
        # Top Accent Navy Bar
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 16, 'F')
        
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(56, 189, 248) # Cyan Accent
        self.set_xy(15, 4)
        self.cell(0, 8, "24TECHDROP // VIP DEVELOPER INTELLIGENCE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", size=8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Confidential Engineering Vault  |  Page {self.page_no()}", align="C")

def build_pdf(content, topic):
    pdf = ProTechPDF()
    pdf.set_margins(16, 16, 16)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=16)
    pw = pdf.epw
    
    # Document Hero Header
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(pw, 9, f"Production Stack: {topic.title()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    date_str = datetime.now().strftime("%d %B %Y")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(pw, 5, f"Live Verified Intelligence Briefing  *  Generated on {date_str}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Divider Line
    pdf.set_draw_color(226, 232, 240)
    pdf.set_line_width(0.4)
    pdf.line(16, pdf.get_y() + 3, 210 - 16, pdf.get_y() + 3)
    pdf.ln(7)
    
    clean_text = sanitize(content)
    
    for line in clean_text.split("\n"):
        clean_line = line.strip()
        if not clean_line:
            pdf.ln(2)
            continue
            
        # Section Banners
        if "[SECTION" in clean_line or clean_line.startswith(("1.", "2.", "3.")) and len(clean_line) < 45:
            pdf.ln(4)
            pdf.set_fill_color(241, 245, 249) # Light Slate Fill
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(14, 116, 144) # Deep Cyan
            pdf.cell(pw, 7, f"  {clean_line}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
            continue
            
        # Code or Command Block
        if any(clean_line.startswith(prefix) for prefix in ["docker ", "curl ", "pip ", "python ", "kubectl ", "export "]):
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(203, 213, 225)
            pdf.set_font("Courier", "B", 8.5)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(pw, 5, f" $ {clean_line}", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            continue
            
        # Regular Explanatory Bullets
        if clean_line.startswith("-"):
            pdf.set_font("Helvetica", size=9)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(pw, 5, f"  *  {clean_line[1:].strip()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        else:
            pdf.set_font("Helvetica", size=9)
            pdf.set_text_color(71, 85, 105)
            pdf.multi_cell(pw, 5, clean_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
    pdf.output("digital_product.pdf")
    print("PDF Successfully Built with Enterprise Styling!")

if __name__ == "__main__":
    topic, live_data = fetch_breakout_trends()
    raw_content = generate_pro_analysis(topic, live_data)
    build_pdf(raw_content, topic)
