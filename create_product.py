import os
from groq import Groq
from fpdf import FPDF

# Groq client init
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_content():
    prompt = """
    Create an actionable and valuable developer cheatsheet titled 'Ultimate AI Tools & Developer Hacks 2026'.
    Include:
    1. Top 5 AI Tools Every Developer Should Know in 2026
    2. 5 High-Impact System Prompts for Coding, Debugging, and System Architecture
    3. Essential Terminal Hacks and Automation Tips
    Keep it clean, concise, practical, and well-structured with bullet points. Avoid using markdown formatting symbols like asterisks (*) or hash signs (#) so it prints cleanly.
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1500
    )
    return completion.choices[0].message.content

def create_pdf(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, "TechDrop24 - Exclusive Developer Power Pack", ln=True, align="C")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Daily Automated AI & Developer Cheatsheet", ln=True, align="C")
    pdf.ln(6)
    
    # Content Body
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(40, 40, 40)
    
    # Clean non-latin characters
    safe_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    
    pdf.output("digital_product.pdf")
    print("PDF Successfully Generated: digital_product.pdf")

if __name__ == "__main__":
    print("Generating product content via Groq (openai/gpt-oss-20b)...")
    content = generate_content()
    create_pdf(content)
