from ai.gpt import gpt_call
import json
from fpdf import FPDF
import base64
import tempfile
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Security Incident Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_report_content(incident_details):
    prompt = f"""
    Generate a comprehensive security incident report based on the following details:
    {incident_details}
    
    The report should include:
    1. Title: "Security Incident Report"
    2. Incident Overview
    3. Detailed Description
    4. Date and Time
    5. Location
    6. Individuals Involved
    7. Potential Impact
    8. Recommended Actions
    9. Conclusion
    
    Format the report professionally with clear sections and bullet points where appropriate.
    """
    
    messages = [{"role": "user", "content": prompt}]
    response = gpt_call(messages, model="gpt-4", temperature=0.5)
    return response.choices[0].message.content

def create_pdf(report_content):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Split content into lines and add to PDF
    for line in report_content.split('\n'):
        if line.strip() == '':
            pdf.ln(5)
        elif line.strip().endswith(':'):  # Likely a section header
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, line, 0, 1)
            pdf.set_font('Arial', size=11)
        else:
            pdf.multi_cell(0, 5, line)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name
    pdf.output(pdf_path)
    return pdf_path

def report_agent(chat_history):
    # Extract incident details from chat history
    incident_details = "\n".join([msg["content"] for msg in chat_history if msg["role"] == "user"])
    
    # Generate report content
    report_content = generate_report_content(incident_details)
    
    # Create PDF
    pdf_path = create_pdf(report_content)
    
    # Create HTML version
    html_content = f"""
    <html>
        <head>
            <title>Security Incident Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; margin-top: 20px; }}
                .section {{ margin-bottom: 15px; }}
            </style>
        </head>
        <body>
            <h1>Security Incident Report</h1>
            <div>{report_content.replace('\n', '<br>')}</div>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
    </html>
    """
    
    return {
        "report_content": report_content,
        "pdf_path": pdf_path,
        "html_content": html_content
    }