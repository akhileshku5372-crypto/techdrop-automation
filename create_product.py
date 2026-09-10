import os
import requests
from groq import Groq
from fpdf import FPDF

# Groq Client setup
client = Groq(api_key="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")

def generate_valuable_content():
    prompt = """
    Create an actionable, high-density technical cheatsheet for developers titled '24TECHDROP PRO DEVELOPER BLUEPRINT 2026'.
    
    Structure it strictly into:
    1. TOP 5 AI TOOLS FOR DEVELOPERS (Mention tools like Cursor, v0.dev, LangGraph, Ollama, etc. with 1-line use case).
    2. HIGH-IMPACT SYSTEM PROMPTS (Full copy-paste prompts for Code Review, SQL Optimization, and Architecture Audit).
    3. ESSENTIAL TERMINAL HACKS (Commands like ripgrep, fd, fzf, tmux aliases, jq pipelines).
    
    IMPORTANT: Do NOT use markdown symbols like * or #. Do NOT use fancy unicode quotes or symbols. Use simple dash (-) for bullets.
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=2000
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

class BlueprintPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, "24TECHDROP | EXCLUSIVE DEVELOPER ASSET", align="L")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"Page {self.page_no()} | Distributed via 24TechDrop", align="C")

def build_pdf(content):
    pdf = BlueprintPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Ultimate AI Tools & Developer Hacks 2026", ln=True)
    
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Curated production-ready reference pack for developers and engineers.", ln=True)
    pdf.ln(6)
    
    clean_content = sanitize_text(content)
    
    for line in clean_content.split("\n"):
        line_str = line.strip()
        if not line_str:
            pdf.ln(2)
            continue
            
        if line_str[0].isdigit() and (line_str[1] in [".", ")"] or line_str[2] in [".", ")"]):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(2, 132, 199)
            pdf.cell(0, 7, line_str, ln=True)
            pdf.set_font("Helvetica", size=9)
            pdf.set_text_color(30, 41, 59)
        else:
            pdf.set_font("Helvetica", size=9)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 5, line_str)
            
    filename = "digital_product.pdf"
    pdf.output(filename)
    print("PDF Successfully Built:", filename)
    return filename

if __name__ == "__main__":
    text = generate_valuable_content()
    build_pdf(text)
