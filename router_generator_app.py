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
    
    /* Router output styling */
    .router-output {{
        background: white;
        border: 2px solid #333;
        padding: 2rem;
        border-radius: 8px;
        font-family: Arial, sans-serif;
        margin-top: 1rem;
    }}
    
    .router-header {{
        display: flex;
        justify-content: space-between;
        border-bottom: 2px solid black;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }}
    
    .router-logo {{
        font-size: 48px;
        font-weight: bold;
    }}
    
    .router-title {{
        font-size: 28px;
        font-weight: bold;
    }}
    
    .router-info {{
        text-align: right;
        font-size: 12px;
    }}
    
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }}
    
    th, td {{
        border: 1px solid black;
        padding: 8px;
        text-align: center;
        font-size: 12px;
    }}
    
    th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}
    
    .totals-row {{
        background-color: #fff0f0;
        color: red;
        font-weight: bold;
    }}
    
    .instruction-row {{
        font-style: italic;
        text-align: left;
        border-top: none;
    }}
    
    .footer {{
        text-align: center;
        margin-top: 30px;
        font-style: italic;
        border-top: 2px solid black;
        padding-top: 20px;
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
    
    st.markdown("### Model Information")
    st.info("**Gemini 2.0 Flash Experimental**\n\nFREE for 1,500 requests/day\nFast and accurate")
    
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
def generate_router_with_gemini(pdf_file, quantity, api_key):
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

OUTPUT: Generate M2M Standard Routing Summary in CSV format.

CSV STRUCTURE (output EXACTLY this format):
Line 1: MAC,,,,,Standard Routing Summary,,,,Page : 1 of 1
Line 2: ,,,,,,,,Date : {datetime.now().strftime('%m/%d/%Y')}
Line 3: ,,,,,,,,Time : {datetime.now().strftime('%I:%M:%S %p')} EST
Line 4: ,,,,,,,,
Line 5: Facility,Part Number,Rev,Description,Unit of Measure,Standard Process Qty,,,
Line 6: Default,[PART# from drawing],0,[DESCRIPTION from drawing],EA,{quantity}.00000,,,
Line 7-8: Empty rows (just commas)
Line 9: Op,Work Center,,Operation Qty,Setup Hours,Production Hours,Move Hours,Sub-Contract Costs,Other Costs,Standard Cost/Operation
Then for each operation (2 lines):
  Data row: [OP#],[CODE],[DESC],{quantity}.0000,[SETUP],[RUN],0.00,0.00,0.00,0.00
  Instruction row: ,[INSTRUCTION],,,,,,,,
  Empty row: ,,,,,,,,
After all operations:
  Totals,,,,[TOTAL SETUP],[TOTAL RUN],0.00,0.00,0.00,"$ 0.00"
  Totals per Unit,,,,[SETUP÷{quantity}],[RUN÷{quantity}],0.00,0.00,0.00,$ 0.00
  Empty rows
  ,,,,,End of Report,,,,
  Empty row
  ,,,,,This report was requested by MAC ROUTER GENERATOR,,,,

Remember:
- Read part number and description from the drawing title block
- Calculate run hours: (minutes per piece × {quantity}) ÷ 60
- Keep operations simple and realistic
- Output ONLY the CSV (no markdown, no code blocks, no explanation)
"""
        
        model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
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
        
        return csv_text
        
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check:\n- API key is valid\n- PDF is readable\n- Network connection is stable"

def csv_to_html(csv_text):
    """Convert CSV to HTML table for display"""
    lines = csv_text.strip().split('\n')
    html = '<div class="router-output">'
    
    for i, line in enumerate(lines):
        parts = line.split(',')
        
        if i == 0:
            html += f'''
            <div class="router-header">
                <div class="router-logo">{parts[0]}</div>
                <div class="router-title">{parts[5] if len(parts) > 5 else ""}</div>
                <div class="router-info">{parts[9] if len(parts) > 9 else ""}</div>
            </div>
            '''
        elif i in [1, 2]:
            html += f'<div style="text-align: right; font-size: 12px;">{parts[8] if len(parts) > 8 else ""}</div>'
        elif 'Facility,Part Number' in line:
            html += '<table><thead><tr>'
            for cell in parts[:6]:
                if cell:
                    html += f'<th>{cell}</th>'
            html += '</tr></thead><tbody>'
        elif 'Op,Work Center' in line:
            html += '</tbody></table><table><thead><tr>'
            for cell in parts[:10]:
                if cell:
                    html += f'<th>{cell}</th>'
            html += '</tr></thead><tbody>'
        elif line.startswith('Totals'):
            html += '<tr class="totals-row">'
            for j, cell in enumerate(parts[:10]):
                if j == 0:
                    html += f'<td colspan="4"><strong>{cell}</strong></td>'
                elif cell:
                    html += f'<td><strong>{cell}</strong></td>'
            html += '</tr>'
        elif 'End of Report' in line:
            html += '</tbody></table><div class="footer">'
            html += '<div style="font-size: 14px; font-weight: bold; margin-bottom: 10px;">End of Report</div>'
        elif i == len(lines) - 1:
            html += f'<div>{parts[5] if len(parts) > 5 else ""}</div></div>'
        elif parts[0] and parts[0].strip() and not line.startswith(','):
            html += '<tr>'
            for cell in parts[:10]:
                html += f'<td>{cell}</td>'
            html += '</tr>'
        elif line.startswith(',') and parts[1]:
            html += '<tr class="instruction-row"><td></td>'
            html += f'<td colspan="9" style="text-align: left; font-style: italic;">{parts[1]}</td></tr>'
    
    html += '</div>'
    return html

# ==========================================
# Main Interface
# ==========================================

# Show chat history if exists
if len(st.session_state.chat_history) > 0:
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="user-message chat-message">
                <div class="message-role">You</div>
                <div class="message-content">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message chat-message">
                <div class="message-role">MAC AI Assistant</div>
                <div class="message-content">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# Main content area - PROPERLY CENTERED
has_chat = len(st.session_state.chat_history) > 0
content_class = "main-content with-chat" if has_chat else "main-content"
st.markdown(f'<div class="{content_class}">', unsafe_allow_html=True)

# Only show heading if no chat history
if len(st.session_state.chat_history) == 0:
    st.markdown('<h1 class="welcome-heading">Import a Drawing</h1>', unsafe_allow_html=True)

# File uploader and quantity in one line
col1, col2 = st.columns([5, 1])

with col1:
    uploaded_file = st.file_uploader("Upload", type=['pdf'], label_visibility="collapsed", key="file_upload")

with col2:
    # Quantity input embedded next to browse files
    quantity = st.number_input("Qty", min_value=1, value=50, key="quantity_input", label_visibility="collapsed", placeholder="Qty")

# Generate Router button - visible and centered
st.markdown('<div class="generate-button-container">', unsafe_allow_html=True)
generate_clicked = st.button("🚀 Generate Router", type="primary", key="generate_button", use_container_width=False)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle generation
if generate_clicked:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar")
    elif not uploaded_file:
        st.error("Please upload an engineering drawing")
    else:
        user_message = f"Generate router for **{uploaded_file.name}** with quantity: **{quantity}**"
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_message
        })
        
        with st.spinner("Analyzing drawing and generating router..."):
            router_csv = generate_router_with_gemini(uploaded_file, quantity, api_key)
            st.session_state.router_csv = router_csv
            st.session_state.router_generated = True
            
            html_output = csv_to_html(router_csv)
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"<strong>Router generated successfully</strong><br><br>{html_output}"
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
    <strong>MAC Products</strong> • Router Generator v1.0 • Powered by Google Gemini 2.0 Flash
</div>
""", unsafe_allow_html=True)
