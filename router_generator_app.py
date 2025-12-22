"""
MAC Router Generator - AI-Powered Manufacturing Router Creation
Ultra-clean ChatGPT-style interface with MAC Products branding
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime
import base64
import io
import os
import re

# ==========================================
# HTML Cleaning Utility
# ==========================================
def clean_html_from_csv(csv_text):
    """
    Aggressively remove ALL HTML tags and artifacts from CSV text.
    This fixes the issue where Gemini outputs HTML formatting in CSV data.
    """
    if not csv_text:
        return csv_text

    # Remove all HTML tags (including malformed ones with spaces)
    # Pattern matches: <tag>, < tag>, <tag >, < /tag>, </tag >, etc.
    csv_text = re.sub(r'<\s*/?\s*\w+[^>]*\s*/?>', '', csv_text)

    # Remove any remaining angle bracket patterns that look like HTML
    csv_text = re.sub(r'<\s*/?\s*(strong|td|tr|th|table|div|span|br|p|b|i|em)[^>]*>', '', csv_text, flags=re.IGNORECASE)

    # Remove HTML entities
    csv_text = re.sub(r'&[a-zA-Z]+;', '', csv_text)
    csv_text = re.sub(r'&#\d+;', '', csv_text)

    # Remove class attributes that might have leaked
    csv_text = re.sub(r'\s*class\s*=\s*["\'][^"\']*["\']', '', csv_text)

    # Clean up any double/triple commas that might result from removed content
    # But preserve intentional empty cells (single commas)
    csv_text = re.sub(r',{3,}', ',,', csv_text)

    # Clean up extra whitespace within cells but preserve structure
    lines = csv_text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Split by comma, clean each cell, rejoin
        cells = line.split(',')
        cleaned_cells = [cell.strip() for cell in cells]
        cleaned_lines.append(','.join(cleaned_cells))

    return '\n'.join(cleaned_lines)

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="MAC Router Generator",
    page_icon="mac_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MAC Blue & White Theme (Ultra Clean)
# ==========================================
PRIMARY_COLOR = "#1E3A8A"  # MAC Blue
SECONDARY_COLOR = "#EEF2FF"  # Light blue
BACKGROUND_COLOR = "#F7F7F8"  # Light gray
TEXT_COLOR = "#0F172A"  # Dark text
BUTTON_COLOR = "#1E40AF"  # Button blue

st.markdown(f"""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main background */
    .main {{
        background-color: {BACKGROUND_COLOR};
        padding: 0;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: white;
        padding-top: 0;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 0;
    }}
    
    /* MAC Logo in sidebar */
    .sidebar-logo {{
        padding: 1.5rem;
        border-bottom: 1px solid #E5E7EB;
        background-color: white;
        margin-bottom: 1rem;
    }}
    
    .sidebar-logo img {{
        width: 120px;
        height: auto;
    }}
    
    /* Main content container - PROPERLY CENTERED */
    .main-content {{
        max-width: 900px;
        margin: 0 auto;
        padding-top: 6rem;
        padding-left: 2rem;
        padding-right: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    /* When chat exists, move input to bottom */
    .main-content.with-chat {{
        justify-content: flex-end;
        min-height: auto;
        padding-bottom: 2rem;
    }}
    
    /* Welcome heading */
    .welcome-heading {{
        font-size: 2.5rem;
        font-weight: 600;
        color: {TEXT_COLOR};
        text-align: center;
        margin-bottom: 3rem;
    }}

    /* Input container - horizontal layout */
    .input-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }}

    .file-upload-wrapper {{
        flex: 1;
        max-width: 500px;
    }}
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {{
        width: 100%;
    }}
    
    [data-testid="stFileUploader"] > div {{
        padding: 0;
        border: none;
        background: transparent;
    }}
    
    [data-testid="stFileUploader"] label {{
        display: none;
    }}
    
    /* Quantity input - inline with file uploader */
    .stNumberInput {{
        width: 100% !important;
    }}

    .stNumberInput > div {{
        width: 100% !important;
    }}

    .stNumberInput > div > div {{
        width: 100% !important;
    }}

    .stNumberInput>div>div>input {{
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        background: white !important;
        text-align: center !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }}

    .stNumberInput>div>div>input:focus {{
        border-color: {PRIMARY_COLOR} !important;
        box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.1) !important;
        outline: none !important;
    }}

    .stNumberInput>div>div>input::placeholder {{
        color: #9CA3AF !important;
        font-size: 0.875rem !important;
    }}

    /* Hide number input buttons */
    .stNumberInput>div>div>input::-webkit-inner-spin-button,
    .stNumberInput>div>div>input::-webkit-outer-spin-button {{
        -webkit-appearance: none;
        margin: 0;
    }}

    .stNumberInput>div>div>input[type=number] {{
        -moz-appearance: textfield;
    }}
    
    /* Chat message bubbles */
    .chat-message {{
        width: 100%;
        max-width: 800px;
        padding: 1.5rem;
        margin: 1.5rem auto;
        border-radius: 12px;
        animation: fadeIn 0.3s ease-in;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .user-message {{
        background: {SECONDARY_COLOR};
        border: 1px solid #D1D5DB;
    }}
    
    .assistant-message {{
        background: white;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}
    
    .message-role {{
        font-weight: 600;
        color: {PRIMARY_COLOR};
        margin-bottom: 0.75rem;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .message-content {{
        color: {TEXT_COLOR};
        line-height: 1.6;
        font-size: 1rem;
    }}
    
    /* Router output styling - M2M Format */
    .router-output {{
        background: white;
        border: 2px solid #000;
        padding: 1.5rem;
        border-radius: 4px;
        font-family: Arial, sans-serif;
        margin: 1rem auto;
        overflow-x: auto;
        overflow-y: visible;
        box-sizing: border-box;
        max-width: 1050px;
        width: 1050px;
    }}

    .router-header {{
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: start;
        border-bottom: 2px solid black;
        padding-bottom: 15px;
        margin-bottom: 20px;
        gap: 2rem;
    }}

    .router-logo {{
        font-size: 48px;
        font-weight: 900;
        letter-spacing: -2px;
        font-family: Arial Black, sans-serif;
    }}

    .router-title {{
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        align-self: center;
    }}

    .router-info {{
        text-align: right;
        font-size: 11px;
        line-height: 1.4;
        white-space: nowrap;
    }}

    .router-output table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 10px;
    }}

    .router-output th, .router-output td {{
        border: 1px solid black;
        padding: 4px 6px;
        text-align: left;
        font-size: 10px;
    }}

    .router-output th {{
        background-color: #f5f5f5;
        font-weight: bold;
        text-align: center;
    }}

    .router-output .part-info-table {{
        margin-bottom: 5px;
    }}

    .router-output .part-info-table td {{
        text-align: left;
        font-weight: normal;
    }}

    .router-output .operations-table th,
    .router-output .operations-table td {{
        text-align: center;
    }}

    .totals-row {{
        background-color: transparent;
        color: red;
        font-weight: bold;
    }}

    .instruction-row {{
        border: none !important;
        border-top: 2px dashed #666 !important;
        border-bottom: 2px dashed #666 !important;
        padding: 6px 8px !important;
    }}

    .instruction-row td {{
        border: none !important;
        text-align: left !important;
        font-style: italic;
        font-size: 10px;
    }}

    .footer {{
        text-align: center;
        margin-top: 25px;
        padding-top: 20px;
        font-style: italic;
        font-size: 12px;
    }}

    .footer-line {{
        border-top: 2px solid black;
        margin: 15px 0;
    }}

    .footer-text {{
        margin-top: 15px;
        font-style: italic;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {BUTTON_COLOR};
        color: white;
        border-radius: 50px;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2.5rem;
        transition: all 0.2s ease;
        font-size: 1rem;
    }}
    
    .stButton>button:hover {{
        background-color: {PRIMARY_COLOR};
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
    }}
    
    /* Success/Error boxes */
    .stSuccess {{
        background-color: #D1FAE5;
        color: #065F46;
        border-left: 4px solid #059669;
        border-radius: 8px;
    }}
    
    .stError {{
        background-color: #FEE2E2;
        color: #991B1B;
        border-left: 4px solid #DC2626;
        border-radius: 8px;
    }}
    
    /* Metric cards */
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        color: {PRIMARY_COLOR};
        font-weight: 700;
    }}
    
    /* Download section */
    .download-section {{
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }}

    /* Generate button container */
    .generate-button-container {{
        display: flex;
        justify-content: center;
        margin-top: 1.5rem;
        width: 100%;
    }}

    /* Make the primary button visible and styled */
    button[kind="primary"] {{
        background-color: {BUTTON_COLOR} !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.75rem 2.5rem !important;
        transition: all 0.2s ease !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.2) !important;
    }}

    button[kind="primary"]:hover {{
        background-color: {PRIMARY_COLOR} !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3) !important;
    }}
</style>

<script>
    // Utility function to click the generate button
    function clickGenerateButton() {{
        const button = document.querySelector('button[data-testid="baseButton-primary"]') ||
                      document.querySelector('button[kind="primary"]') ||
                      Array.from(document.querySelectorAll('button')).find(btn =>
                          btn.textContent.includes('Generate Router')
                      );

        if (button) {{
            button.click();
            return true;
        }}
        return false;
    }}

    // Optional: Listen for Enter key to submit (convenience feature)
    document.addEventListener('DOMContentLoaded', function() {{
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Enter' || e.keyCode === 13) {{
                const fileUploader = document.querySelector('[data-testid="stFileUploader"]');
                const fileItems = fileUploader?.querySelectorAll('[data-testid="stFileUploaderFile"]');

                // Only submit if a file is uploaded
                if (fileItems && fileItems.length > 0) {{
                    e.preventDefault();
                    e.stopPropagation();
                    clickGenerateButton();
                }}
            }}
        }}, true);
    }});
</script>
""", unsafe_allow_html=True)

# ==========================================
# Session State Initialization
# ==========================================
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'router_generated' not in st.session_state:
    st.session_state.router_generated = False
if 'router_csv' not in st.session_state:
    st.session_state.router_csv = ""
if 'quantity' not in st.session_state:
    st.session_state.quantity = 50

# ==========================================
# Sidebar with MAC Logo
# ==========================================
with st.sidebar:
    logo_path = "mac_logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
            st.markdown(f"""
            <div class="sidebar-logo">
                <img src="data:image/png;base64,{logo_data}" alt="MAC Products">
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sidebar-logo">
            <h2 style="margin: 0; color: #1E3A8A;">MAC PRODUCTS</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Configuration")
    
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get your API key from https://aistudio.google.com/apikey",
        placeholder="Enter your API key..."
    )
    
    if api_key:
        st.success("API Key configured")
    else:
        st.warning("Please enter API key")
    
    st.markdown("---")
    
    st.markdown("### Model Settings")
    
    # Gemini model selector
    gemini_models = [
        "gemini-3-flash-preview",
        "gemini-3-pro", 
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]
    
    selected_model = st.selectbox(
        "Select Gemini Model",
        gemini_models,
        index=0,
        help="Choose the Gemini model for router generation"
    )
    
    st.info(f"**{selected_model}**\n\nFREE for 1,500 requests/day")
    
    st.markdown("---")
    
    st.markdown("### Session Statistics")
    st.metric("Routers Generated", len([m for m in st.session_state.chat_history if m['role'] == 'assistant']))
    st.metric("Total Cost", "$0.00", delta="FREE Tier")
    
    st.markdown("---")
    
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.router_generated = False
        st.session_state.router_csv = ""
        st.rerun()
    
    st.markdown("---")
    
    with st.expander("Help & Documentation"):
        st.markdown("""
        **How to Use:**
        1. Enter your Gemini API key above
        2. Upload an engineering drawing (PDF)
        3. Adjust quantity if needed (default: 50)
        4. Click Generate Router
        5. Download or copy the result
        
        **Tips:**
        - PDFs work best
        - Clear drawings produce better results
        - Review times before using in production
        """)

# ==========================================
# Knowledge Base
# ==========================================
KNOWLEDGE_BASE = """
CRITICAL MANUFACTURING RULES:

Setup Times (ALWAYS use these):
- SAW: 0.25 hrs
- WATERJT: 0.50 hrs
- BEND: 0.50-2.00 hrs
- CNC-L: 2.00 hrs (ALWAYS 2.00, never 1.00)
- CNC-M: 1.50-2.00 hrs
- WELD: 0.50-3.00 hrs
- PAINT: 0.50-1.00 hrs (ALWAYS 4.00 hrs move time)

Run Times Per Piece (DO NOT EXCEED):
- SAW: 0.5 min/piece
- WATERJET: 3-5 min/piece (simple), 10-15 min/piece (complex)
- BEND: 0.5-1 min/piece (simple), 2-3 min/piece (complex)
- CNC-L: 2-3 min/piece (simple lathe work - IF >5 min YOU'RE WRONG)
- CNC-M: 2-5 min/piece
- WELD: 5-40 min/piece

Formula: Run Hours = (min per piece × quantity) ÷ 60

Work Center Codes:
- WATERJT - "WATERJET MACHINE"
- SAW - "CUT OFF SAW AREA"
- BEND - "PRESS BRAKE"
- CNC-L - "CNC LATHE MACH."
- CNC-M - "CNC MILL MACHINE"
- WELD - "WELDING AREA"
- PAINT - "SPRAY BOOTH"
- SUB-PL - "SUB PLATING"

Instructions:
- Waterjet: "VETTED S.O. [DATE] CUT OUT PER THE DWG AND DEBURR."
- Saw: "CUT MATERIAL TO LENGTH PER THE DWG."
- CNC-L: "MACHINE PART PER THE DWG AND DEBURR."
- Bend: "BEND PART TO THE DWG."
- Weld: "VETTED S.O. [DATE] WELD PARTS PER DRAWING."
- Paint: "PAINT PARTS PER THE DWG."

EXAMPLES:
Example: Simple Lathe Part (Z110001B046) - 23 pieces
- Op 10: SAW - Setup: 0.25 hrs, Run: 0.77 hrs (2 min/piece)
- Op 20: CNC-L - Setup: 2.00 hrs, Run: 0.77 hrs (2 min/piece)

Example: Sheet Metal with Bends (Z005002A019) - 30 pieces
- Op 10: WATERJT - Setup: 0.50 hrs, Run: 1.50 hrs (3 min/piece)
- Op 20: BEND - Setup: 0.50 hrs, Run: 0.38 hrs (0.76 min/piece)
"""

# ==========================================
# Router Generation Function
# ==========================================
def generate_router_with_gemini(pdf_file, quantity, api_key, model_name="gemini-3-flash-preview"):
    """Call Gemini API to generate router"""
    try:
        genai.configure(api_key=api_key)
        pdf_bytes = pdf_file.read()
        
        prompt = f"""You are a manufacturing engineer creating a router for Made2Manage ERP.

{KNOWLEDGE_BASE}

TASK: Analyze this drawing and generate a router for {quantity} pieces.

CRITICAL RULES:
1. Keep it SIMPLE (2-4 operations max)
2. CNC-L setup = 2.00 hrs ALWAYS (not 1.00)
3. Simple lathe parts = 2-3 min/piece MAX (if >5 min YOU'RE WRONG)
4. Use examples as baseline for times
5. Match instruction templates exactly
6. DESCRIPTION FORMATTING: Always put the complete description in the Description field (e.g., "SLEEVE WIPING CAP" as one entry, not split)

OUTPUT: Generate M2M Standard Routing Summary in CSV format.

CSV STRUCTURE (output EXACTLY this format):
Line 1: MAC,,,,,Standard Routing Summary,,,,,Page : 1 of 1
Line 2: ,,,,,,,,,Date : {datetime.now().strftime('%m/%d/%Y')}
Line 3: ,,,,,,,,,Time : {datetime.now().strftime('%I:%M:%S %p')} EST
Line 4: ,,,,,,,,,
Line 5: Facility,Part Number,Rev,Description,Unit of Measure,Standard Process Qty,,,
Line 6: Default,[PART# from drawing],0,[COMPLETE DESCRIPTION - combine all description words into single field separated by spaces],EA,{quantity}.00000,,,
Line 7-8: Empty rows (just commas)
Line 9: Op,Work Center,Operation Description,Operation Qty,Setup Hours,Production Hours,Move Hours,Sub-Contract Costs,Other Costs,Standard Cost/Operation
Then for each operation (2 lines):
  Data row: [OP#],[CODE],[DESC],{quantity}.0000,[SETUP],[RUN],0.00,0.00,0.00,0.00
  Instruction row: ,[INSTRUCTION],,,,,,,,,
  Empty row: ,,,,,,,,,
After all operations:
  Totals,,,,[TOTAL SETUP],[TOTAL RUN],0.00,0.00,0.00,"$ 0.00"
  Totals per Unit,,,,[SETUP÷{quantity}],[RUN÷{quantity}],0.00,0.00,0.00,$ 0.00
  Empty rows
  ,,,,,,End of Report,,,,,
  Empty row
  ,,,,,,This report was requested by MAC ROUTER GENERATOR,,,,,

Remember:
- Read part number and description from the drawing title block
- IMPORTANT: The Description field must contain the COMPLETE description as a single entry (e.g., "SLEEVE WIPING CAP" not split across fields)
- Unit of Measure must be "EA"
- Standard Process Qty must be the quantity value {quantity}.00000
- Calculate run hours: (minutes per piece × {quantity}) ÷ 60
- Keep operations simple and realistic
- Output ONLY the CSV (no markdown, no code blocks, no explanation)

CRITICAL - NO HTML TAGS:
- DO NOT use <strong>, <td>, <tr>, <th>, <table>, or ANY HTML tags
- DO NOT use HTML entities like &nbsp; or &#160;
- Output PLAIN TEXT CSV only - just commas and values
- The Totals row should be: Totals,,,,2.25,0.50,0.00,0.00,0.00,$ 0.00
- NOT: Totals,,,,<strong>2.25</strong>,<strong>0.50</strong>...
"""
        
        model = genai.GenerativeModel(
            model_name,
            generation_config={
                "temperature": 0.1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
        
        uploaded = genai.upload_file(io.BytesIO(pdf_bytes), mime_type='application/pdf')
        response = model.generate_content([uploaded, prompt], request_options={"timeout": 60})

        csv_text = response.text.strip()
        if '```' in csv_text:
            csv_text = csv_text.split('```csv')[-1].split('```')[0].strip()

        # CRITICAL: Clean any HTML tags that Gemini might have added
        csv_text = clean_html_from_csv(csv_text)

        return csv_text
        
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check:\n- API key is valid\n- PDF is readable\n- Network connection is stable"

def csv_to_html(csv_text):
    """Convert CSV to HTML table for display - M2M Format"""

    def clean_cell(cell):
        """Remove any HTML tags from a cell value - safety net"""
        if not cell:
            return cell
        # Remove all HTML tags
        cleaned = re.sub(r'<[^>]+>', '', str(cell))
        # Remove HTML entities
        cleaned = re.sub(r'&[a-zA-Z]+;', '', cleaned)
        cleaned = re.sub(r'&#\d+;', '', cleaned)
        # Remove quotes that might wrap values
        cleaned = cleaned.strip().strip('"').strip("'")
        return cleaned

    lines = csv_text.strip().split('\n')
    html = '<div class="router-output">'

    in_operations_table = False

    for i, line in enumerate(lines):
        parts = line.split(',')
        # Clean all parts upfront
        parts = [clean_cell(p) for p in parts]

        # Header line - MAC logo, title, page info
        if i == 0:
            page_info = parts[9] if len(parts) > 9 else ""
            html += f'''
            <div class="router-header">
                <div class="router-logo">{parts[0]}</div>
                <div class="router-title">{parts[5] if len(parts) > 5 else ""}</div>
                <div class="router-info">{page_info}</div>
            </div>
            '''
        # Date and Time lines
        elif i in [1, 2]:
            date_time_info = parts[8] if len(parts) > 8 else ""
            if date_time_info:
                # Append to router-info div (hacky but works)
                html = html.replace('</div>\n            </div>',
                                   f'<br>{date_time_info}</div>\n            </div>')

        # Part info table header
        elif 'Facility' in line and 'Part Number' in line:
            html += '<table class="part-info-table"><thead><tr>'
            for cell in parts[:6]:
                if cell.strip():
                    html += f'<th>{cell}</th>'
            html += '</tr></thead><tbody>'

        # Operations table header
        elif 'Op' in line and 'Work Center' in line:
            html += '</tbody></table><table class="operations-table"><thead><tr>'
            for cell in parts[:11]:  # Now 11 columns instead of 10
                if cell.strip():
                    html += f'<th>{cell}</th>'
            html += '</tr></thead><tbody>'
            in_operations_table = True

        # Totals rows (handles both "Totals" and "Totals per Unit")
        elif parts[0].strip().startswith('Totals'):
            html += '<tr class="totals-row">'
            for j, cell in enumerate(parts[:11]):  # Now 11 columns
                if cell.strip():
                    html += f'<td><strong>{cell}</strong></td>'
                else:
                    html += '<td></td>'
            html += '</tr>'

        # End of Report
        elif 'End of Report' in line:
            html += '</tbody></table>'
            html += '<div class="footer-line"></div>'
            html += '<div class="footer"><strong>End of Report</strong></div>'

        # Footer message (last line)
        elif i == len(lines) - 1 and len(parts) > 5:
            footer_msg = parts[5] if parts[5] else ""
            if footer_msg:
                html += f'<div class="footer-text">{footer_msg}</div>'

        # Data rows
        elif parts[0] and parts[0].strip() and not line.startswith(','):
            html += '<tr>'
            for cell in parts[:11 if in_operations_table else 6]:  # Now 11 columns for operations
                html += f'<td>{cell}</td>'
            html += '</tr>'

        # Instruction rows (start with comma)
        elif line.startswith(',') and len(parts) > 1 and parts[1].strip():
            html += '<tr class="instruction-row">'
            colspan = "11" if in_operations_table else "6"  # Now colspan 11
            html += f'<td colspan="{colspan}">{parts[1]}</td>'
            html += '</tr>'

    html += '</div>'
    return html

# ==========================================
# Main Interface
# ==========================================

# Load MAC logo for chat avatars
def load_logo_as_base64():
    """Load MAC logo from same directory as script and convert to base64"""
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        logo_path = os.path.join(script_dir, "mac_logo.png")
        
        if not os.path.exists(logo_path):
            logo_path = "mac_logo.png"
        
        with open(logo_path, "rb") as f:
            logo_bytes = f.read()
        logo_b64 = base64.b64encode(logo_bytes).decode()
        return f"data:image/png;base64,{logo_b64}"
    except Exception as e:
        return None

# Display chat history using st.chat_message
logo_b64 = load_logo_as_base64()

for message in st.session_state.chat_history:
    # Use MAC logo for both user and assistant if available
    if logo_b64:
        with st.chat_message(message['role'], avatar=logo_b64):
            st.markdown(message['content'], unsafe_allow_html=True)
    else:
        with st.chat_message(message['role']):
            st.markdown(message['content'], unsafe_allow_html=True)

# Chat input with file attachment
if prompt := st.chat_input("Attach a PDF drawing and enter quantity...", key="chat_input", accept_file=True):
    
    # Check if user attached a file
    has_file = hasattr(prompt, 'files') and prompt.files
    user_text = prompt.text if hasattr(prompt, 'text') else str(prompt)
    
    # Extract quantity from text
    quantity = None
    try:
        import re
        numbers = re.findall(r'\d+', user_text)
        if numbers:
            quantity = int(numbers[0])
    except:
        pass
    
    if has_file and quantity:
        # User uploaded PDF AND provided quantity
        pdf_file = prompt.files[0]
        pdf_name = pdf_file.name
        
        # Check if API key is configured
        if not api_key:
            st.session_state.chat_history.append({
                'role': 'user',
                'content': f"Uploaded: **{pdf_name}** | Quantity: **{quantity}**"
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': "⚠️ Please enter your Gemini API key in the sidebar to generate routers."
            })
            st.rerun()
        
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': f"Uploaded: **{pdf_name}** | Quantity: **{quantity}**"
        })
        
        # Generate router
        with st.spinner("Analyzing drawing and generating router..."):
            router_csv = generate_router_with_gemini(pdf_file, quantity, api_key, selected_model)
            st.session_state.router_csv = router_csv
            st.session_state.router_generated = True
            
            html_output = csv_to_html(router_csv)
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"<strong>Router Generated Successfully</strong><br><br>{html_output}"
            })
        
        st.rerun()
    
    elif has_file and not quantity:
        # Has file but no quantity
        st.session_state.chat_history.append({
            'role': 'user',
            'content': f"Uploaded: **{prompt.files[0].name}**"
        })
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': "Please include the production quantity in your message (e.g., 'Generate router for 50 pieces')."
        })
        
        st.rerun()
    
    else:
        # Normal message or request
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_text
        })
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': "Please attach a PDF engineering drawing and include the quantity in your message. For example: 'Generate router for 50 pieces' (then attach the PDF)."
        })
        
        st.rerun()

# Download buttons
if st.session_state.router_generated and st.session_state.router_csv:
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    st.markdown("### Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="Download CSV",
            data=st.session_state.router_csv,
            file_name=f"router_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("View Raw CSV", use_container_width=True):
            st.code(st.session_state.router_csv, language="csv")
    
    with col3:
        st.button("Export to Excel", use_container_width=True, disabled=True, help="Coming in Phase 2")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9CA3AF; font-size: 0.875rem; padding: 1.5rem;">
    <strong>MAC Products</strong> • Router Generator v1.0 • Powered by Google Gemini 3 Flash Preview
</div>
""", unsafe_allow_html=True)
