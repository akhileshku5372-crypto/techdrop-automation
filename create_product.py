from fpdf import FPDF

CONTENT = """
ULTIMATE AI & DEVELOPER POWER PACK 2026

1. TOP 5 FREE AI TOOLS FOR DEVELOPERS
- Cursor / Windsurf: AI-native code editors for full-stack workflows.
- Groq Cloud: Ultra low-latency inference for local and cloud bots.
- v0.dev: Generate production-ready frontend components from prompts.
- n8n (Self-hosted): Enterprise-grade workflow automation without limits.
- Hugging Face Spaces: Free cloud hosting for small AI prototypes.

2. HIGH-IMPACT DEVELOPER PROMPTS
- Architecture Design: "Analyze this system architecture for high-concurrency bottlenecks and propose 3 caching strategies."
- Code Optimization: "Refactor this Python code to reduce memory footprint and improve execution speed with complexity O(n)."
- Regex Generator: "Generate an optimized regex to validate international phone numbers and match standard formats."

3. ESSENTIAL TERMINAL SHORTCUTS & HACKS
- Ctrl + R: Reverse-search your entire shell command history.
- lsof -i :<port>: Find and terminate the process hogging your local port.
- curl -I <url>: Instantly fetch and inspect HTTP response headers.
- tail -f <log_file>: Stream application logs in real-time.
"""

def create_pdf(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 15, "TechDrop24 - Exclusive Developer Pack", ln=True, align="C")
    pdf.ln(5)
    
    # Content
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(40, 40, 40)
    safe_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    
    pdf.output("digital_product.pdf")
    print("PDF Successfully Generated: digital_product.pdf")

if __name__ == "__main__":
    create_pdf(CONTENT)
