import os
from groq import Groq
from fpdf import FPDF

# Groq client init
client = Groq(api_key="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")

def generate_content():
    prompt = """
    Create a highly valuable, well-structured cheat sheet titled 'Ultimate AI & Developer Power Pack 2026'.
    Include:
    1. Top 5 Free AI Tools for Coding & Automation
    2. 5 High-Impact System Prompts for Developers
    3. Essential Terminal Shortcuts & Hacks
    Keep it clean, concise, and professional with bullet points. Do not include markdown stars (**) in headings so it renders cleanly.
    """
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1500
    )
    return completion.choices[0].message.content

def create_pdf(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 15, "Ultimate AI & Developer Power Pack", ln=True, align="C")
    pdf.ln(5)
    
    # Body
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(50, 50, 50)
    
    # Clean up non-latin characters if any
    safe_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, safe_text)
    
    pdf.output("digital_product.pdf")
    print("PDF Successfully Generated: digital_product.pdf")

if __name__ == "__main__":
    print("Generating product content via Groq...")
    content = generate_content()
    create_pdf(content)
