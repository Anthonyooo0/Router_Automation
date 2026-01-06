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
import csv

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
⚠️ CRITICAL: MOST MAC PARTS USE ONLY 2 OPERATIONS ⚠️
Review the 14 real examples below - notice that simple parts rarely need more than 2 operations!

REAL ROUTER EXAMPLES FROM THE SHOP:

MACHINED PARTS (Simple Lathe - THE BASELINE):
1. Z110001B045 - Sleeve Wiping Cap (115 pcs) - 2 OPERATIONS
   Op 10: SAW - Setup: 0.25 hrs, Run: 0.03 hrs (0.5 min/pc)
   Op 20: CNC-L - Setup: 2.00 hrs, Run: 3.83 hrs (2 min/pc)
   Instruction: "CUT MATERIAL TO 36" / "MACHINE PART PER THE DWG AND DEBURR."

2. Z110001B046 - Sleeve Wiping Tube (23 pcs) - 2 OPERATIONS
   Op 10: SAW - Setup: 0.25 hrs, Run: 0.77 hrs (2 min/pc)
   Op 20: CNC-L - Setup: 2.00 hrs, Run: 0.77 hrs (2 min/pc)
   Instruction: "CUT MATERIAL TO LENGTH PER THE DWG." / "MACHINE PART PER THE DWG AND DEBURR."

3. Z110001B037 - Sleeve Disc (550 pcs) - 3 OPERATIONS (Complex with plating)
   Op 10: SAW - Setup: 0.25 hrs, Run: 4.58 hrs (0.5 min/pc)
   Op 20: CNC-L - Setup: 2.00 hrs, Run: 18.33 hrs (2 min/pc)
   Op 30: SUB-PL - Setup: 0.00 hrs, Run: 0.00 hrs - PLATE, OUTSIDE VENDOR, ZINC PLATE
   Instruction: "CUT MATERIAL TO LENGTH PER THE DWG." / "MACHINE PART PER THE DWG AND DEBURR." / "PLATE, OUTSIDE VENDOR, ZINC PLATE"

SHEET METAL (Simple - 2 Operations):
4. Z005002A019 - Position Holder Bracket (30 pcs) - 2 OPERATIONS
   Op 10: WATERJT - Setup: 0.50 hrs, Run: 1.50 hrs (3 min/pc)
   Op 20: BEND - Setup: 0.50 hrs, Run: 0.38 hrs (0.76 min/pc)
   Instruction: "VETTED S.O. 04/08/25 CUT OUT PER THE DWG AND DEBURR." / "BEND PART TO THE DWG."

5. Z005002C026 - Side Door (10 pcs) - 2 OPERATIONS
   Op 10: WATERJT - Setup: 0.50 hrs, Run: 2.00 hrs (12 min/pc - larger part)
   Op 20: BEND - Setup: 2.00 hrs (complex bends), Run: 0.50 hrs (3 min/pc)

6. Z110001D007 - Clamp Swivel (50 pcs) - 2 OPERATIONS
   Op 10: WATERJT - Setup: 0.50 hrs, Run: 12.50 hrs (15 min/pc - thick stainless)
   Op 20: CNC-M - Setup: 2.00 hrs, Run: 6.25 hrs (7.5 min/pc)

7. Z110001D005 - Latch Receiver (30 pcs) - 2 OPERATIONS
   Op 10: WATERJT - Setup: 0.50 hrs, Run: 6.00 hrs (12 min/pc)
   Op 20: CNC-M - Setup: 1.50 hrs, Run: 2.00 hrs (4 min/pc)

8. TS01000B072-1 - Slide Plate (40 pcs) - 2 OPERATIONS
   Op 10: WATERJT - Setup: 0.50 hrs, Run: 3.33 hrs (5 min/pc)
   Op 20: CNC-M - Setup: 1.50 hrs, Run: 3.33 hrs (5 min/pc)

SHEET METAL (Single Operation):
9. Z005002A017 - Lifting Plate (20 pcs) - 1 OPERATION ONLY
   Op 10: WATERJT - Setup: 0.50 hrs, Run: 1.00 hrs (3 min/pc)
   Instruction: "VETTED S.O. 04/08/25 CUT OUT PER THE DWG AND DEBURR."

10. Z110001B034 - Gasket (200 pcs) - 1 OPERATION ONLY
    Op 10: WATERJT - Setup: 0.50 hrs, Run: 10.00 hrs (3 min/pc)

WELDMENTS (Simple - 2 Operations):
11. TS01000B086 - Spray Manifold Weldment (12 pcs) - 2 OPERATIONS
    Op 10: WELD - Setup: 3.00 hrs, Run: 4.00 hrs (20 min/pc)
    Op 20: SUB-PL - Setup: 0.00 hrs, Run: 0.00 hrs - PLATE, OUTSIDE VENDOR, ZINC PLATE

12. TS01000C047 - Control Panel Door (6 pcs) - 2 OPERATIONS
    Op 10: WELD - Setup: 1.00 hrs, Run: 2.00 hrs (20 min/pc)
    Op 20: PAINT - Setup: 0.50 hrs, Run: 0.00 hrs, Move: 4.00 hrs - PAINT PARTS PER THE DWG.

COMPLEX PARTS (3+ Operations - RARE):
13. Z110001A030 - Contact Plate (200 pcs) - 3 OPERATIONS
    Op 10: WATERJT - Setup: 0.50 hrs, Run: 13.33 hrs (4 min/pc)
    Op 20: ASSY-PP - Setup: 0.50 hrs, Run: 6.67 hrs (2 min/pc) - TAP HOLES
    Op 30: SUB-PL - Setup: 0.00 hrs, Run: 0.00 hrs - PLATE, OUTSIDE VENDOR, TIN PLATE

14. 2651C2858-1 - Complex Weldment Assembly (1 pc) - 4 OPERATIONS
    Op 10: WELD - Setup: 3.00 hrs, Run: 5.00 hrs (5 hrs for 1 pc)
    Op 20: CNC-M - Setup: 2.00 hrs, Run: 2.00 hrs (2 hrs for 1 pc)
    Op 30: WELD - Setup: 3.00 hrs, Run: 3.00 hrs (3 hrs for 1 pc)
    Op 40: PAINT - Setup: 1.00 hrs, Run: 0.00 hrs, Move: 4.00 hrs

SETUP TIMES (Standard - Use These Exactly):
- SAW: 0.25 hrs (ALWAYS)
- WATERJT: 0.50 hrs (ALWAYS)
- BEND: 0.50 hrs (simple), 2.00 hrs (complex)
- CNC-L: 2.00 hrs (ALWAYS 2.00, NEVER 1.00)
- CNC-M: 1.50-2.00 hrs
- WELD: 0.50-3.00 hrs
- PAINT: 0.50-1.00 hrs + 4.00 hrs move time (dry time)
- SUB-PL: 0.00 hrs (outside vendor)

RUN TIMES PER PIECE (Typical):
- SAW: 0.5-2 min/piece
- WATERJET (simple flat): 3-5 min/piece
- WATERJET (complex/thick): 10-15 min/piece
- BEND (simple): 0.5-1 min/piece
- BEND (complex): 2-3 min/piece
- CNC-L (simple turning): 2-3 min/piece ← IF YOU GO OVER 5 MIN, YOU'RE WRONG!
- CNC-M (drilling/tapping): 2-7.5 min/piece
- WELD: 5-40 min/piece

INSTRUCTIONS (Copy These Formats Exactly):
- Waterjet: "VETTED S.O. [DATE] CUT OUT PER THE DWG AND DEBURR."
- Saw: "CUT MATERIAL TO LENGTH PER THE DWG."
- CNC-L: "MACHINE PART PER THE DWG AND DEBURR."
- CNC-M: "MACHINE PART PER THE DWG AND DEBURR."
- Bend: "BEND PART TO THE DWG."
- Weld: "VETTED S.O. [DATE] WELD PARTS PER DRAWING."
- Paint: "PAINT PARTS PER THE DWG."
- Plating: "PLATE, OUTSIDE VENDOR, [TYPE]"

HOW TO SELECT OPERATIONS:
1. **Simple lathe part?** → SAW + CNC-L (2 operations) - See examples Z110001B045, Z110001B046
2. **Simple sheet metal?** → WATERJET + BEND (2 operations) - See example Z005002A019
3. **Flat waterjet only?** → WATERJET (1 operation) - See examples Z005002A017, Z110001B034
4. **Complex machining?** → WATERJET + CNC-M (2 operations) - See example Z110001D007
5. **DO NOT add unnecessary operations!** Most parts need 2 or fewer operations.
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
1. **MATCH THE EXAMPLES - MOST PARTS USE ONLY 2 OPERATIONS**
   - Simple lathe: 2 ops (SAW + CNC-L) - see examples Z110001B045, Z110001B046
   - Simple sheet metal: 2 ops (WATERJET + BEND) - see example Z005002A019
   - Only complex weldments or very intricate parts need 3+ operations
   - DO NOT add extra machining steps unless the drawing clearly shows complex features
2. CNC-L setup = 2.00 hrs ALWAYS (not 1.00)
3. Simple lathe parts = 2-3 min/piece MAX (if >5 min YOU'RE WRONG)
4. Use examples as baseline for times - reference the most similar example in your reasoning
5. Match instruction templates exactly
6. DESCRIPTION FORMATTING: Always put the complete description in the Description field (e.g., "SLEEVE WIPING CAP" as one entry, not split)

OUTPUT: Generate M2M Standard Routing Summary in CSV format.

⚠️ CRITICAL CSV OUTPUT RULES - READ CAREFULLY:
- Output PURE CSV TEXT ONLY - NO CODE, NO HTML, NO XML, NO FORMATTING
- DO NOT include ANY HTML/XML tags like <td>, <tr>, <strong>, <div>, etc.
- DO NOT include ANY code operators like <, >, ==, !=, &&, ||
- DO NOT include ANY programming syntax or logic
- Each field must contain ONLY: letters, numbers, spaces, periods, dollar signs, hyphens
- Use ONLY commas to separate fields
- The last column should contain ONLY "0.00" - nothing else
- If you accidentally generate code or HTML, the output will be REJECTED

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
  Totals,,,,[TOTAL SETUP],[TOTAL RUN],0.00,0.00,0.00,0.00
  Totals per Unit,,,,[SETUP÷{quantity}],[RUN÷{quantity}],0.00,0.00,0.00,0.00
  Empty rows
  ,,,,,,End of Report,,,,,
  Empty row
  ,,,,,,This report was requested by MAC ROUTER GENERATOR,,,,,

EXAMPLE TOTALS ROWS (copy this format EXACTLY - count the commas!):
Totals,,,,2.25,0.06,0.00,0.00,0.00,0.00
Totals per Unit,,,,0.03,0.07,0.00,0.00,0.00,0.00

CRITICAL: Both Totals rows MUST have the same number of commas and columns!
- Start with "Totals" or "Totals per Unit"
- Then 3 empty fields (,,,)
- Then 6 numeric values separated by commas

Remember:
- Read part number and description from the drawing title block
- IMPORTANT: The Description field must contain the COMPLETE description as a single entry (e.g., "SLEEVE WIPING CAP" not split across fields)
- Unit of Measure must be "EA"
- Standard Process Qty must be the quantity value {quantity}.00000
- Calculate run hours: (minutes per piece × {quantity}) ÷ 60
- Keep operations simple and realistic
- Output ONLY the CSV (no markdown, no code blocks, no explanation, NO HTML TAGS)
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

        # AGGRESSIVE CLEANING - Remove any malformed HTML/XML/code
        import re

        # Step 1: Remove HTML/XML tags
        csv_text = re.sub(r'<[^>]+>', '', csv_text)

        # Step 2: Remove any lines that contain code-like patterns (but keep valid CSV)
        lines = csv_text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Skip lines with obvious code patterns: <, >, ==, !=, <=, >=, etc. in operations column
            # But allow normal CSV commas and decimals
            if not any([
                ' < ' in line and ' > ' in line,  # Code comparison operators
                '<td' in line.lower(),
                '<tr' in line.lower(),
                '</td' in line.lower(),
                '</tr' in line.lower(),
                '<strong' in line.lower(),
                'colspan' in line.lower(),
                '&&' in line,
                '||' in line,
                ' == ' in line,
                ' != ' in line,
                '</' in line,  # Any closing tag
                ' />' in line,  # Self-closing tag
            ]):
                cleaned_lines.append(line)
        csv_text = '\n'.join(cleaned_lines)

        # Step 3: Clean up extra whitespace
        csv_text = re.sub(r'\s{2,}', ' ', csv_text)

        # Step 4: Validate each line has proper CSV structure (but be less aggressive)
        lines = csv_text.split('\n')
        validated_lines = []
        for i, line in enumerate(lines):
            # Always keep empty lines
            if not line.strip():
                validated_lines.append(line)
                continue

            # Check if line has reasonable structure (not too many problematic characters)
            # Valid CSV should mostly be: alphanumeric, spaces, commas, periods, $, -, :, /
            clean_chars = sum(1 for c in line if c.isalnum() or c in ' ,.:-$/()\'\"')
            total_chars = len(line)

            # Be more permissive - allow 70% valid chars instead of 80%
            # This helps preserve instruction rows and other valid content
            if total_chars > 0 and (clean_chars / total_chars) > 0.70:
                validated_lines.append(line)
            else:
                # Only skip lines that are REALLY malformed
                continue

        csv_text = '\n'.join(validated_lines)

        # Step 5: Fix malformed Totals per Unit rows (ensure same structure as Totals row)
        lines = csv_text.split('\n')
        for i in range(len(lines)):
            # If line starts with "Totals per Unit" but has too few commas
            if lines[i].startswith('Totals per Unit'):
                parts = lines[i].split(',')
                # Should have at least 10 parts (label + 3 empty + 6 values)
                if len(parts) < 10:
                    # Pad with empty strings to match structure
                    while len(parts) < 10:
                        parts.insert(1, '')  # Insert empty fields after label
                    lines[i] = ','.join(parts)
        csv_text = '\n'.join(lines)

        # Step 6: Fix operation rows - ensure all have 10 fields (including final 0.00)
        lines = csv_text.split('\n')
        fixed_lines = []
        for line in lines:
            # Check if this is an operation data row (starts with a number like "10" or "20")
            if line and line[0].isdigit() and ',' in line:
                parts = line.split(',')
                # Operation rows should have exactly 10 parts: Op, Work Center, Desc, Qty, Setup, Run, Move, Sub, Other, Cost
                # Ensure it has 10 parts, padding with "0.00" if needed
                while len(parts) < 10:
                    parts.append('0.00')
                # Ensure the last 6 columns (hours and costs) are 0.00 if empty
                for j in range(4, 10):  # Columns 4-9 (Setup through Standard Cost)
                    if not parts[j] or parts[j].strip() == '':
                        parts[j] = '0.00'
                fixed_lines.append(','.join(parts))
            else:
                fixed_lines.append(line)

        csv_text = '\n'.join(fixed_lines)

        # Step 7: Ensure proper spacing before Totals rows
        lines = csv_text.split('\n')
        spaced_lines = []
        for i, line in enumerate(lines):
            # Add line to output
            spaced_lines.append(line)

            # If this is an instruction row (starts with comma) and the NEXT line is Totals
            # Add an empty row between them for proper spacing
            if i < len(lines) - 1:
                if line.startswith(',') and lines[i + 1].startswith('Totals'):
                    # Add empty row for spacing
                    spaced_lines.append(',,,,,,,,,')

        csv_text = '\n'.join(spaced_lines)

        # Step 8: Final validation - ensure we have ALL critical sections
        # Check each required section individually and add if missing
        lines = csv_text.split('\n')

        # Check for "Totals" row (must appear first)
        has_totals = any('Totals' in line and not 'Totals per Unit' in line for line in lines)
        if not has_totals:
            csv_text += '\n,,,,,,,,,\nTotals,,,,0.00,0.00,0.00,0.00,0.00,0.00'

        # Check for "Totals per Unit" row
        has_totals_per_unit = any('Totals per Unit' in line for line in lines)
        if not has_totals_per_unit:
            csv_text += '\nTotals per Unit,,,,0.00,0.00,0.00,0.00,0.00,0.00'

        # Check for "End of Report"
        has_end_of_report = any('End of Report' in line for line in lines)
        if not has_end_of_report:
            csv_text += '\n,,,,,,,,,\n,,,,,,End of Report,,,'

        # Check for footer message
        has_footer = any('MAC ROUTER GENERATOR' in line or 'This report was requested' in line for line in lines)
        if not has_footer:
            csv_text += '\n,,,,,,,,,\n,,,,,,This report was requested by MAC ROUTER GENERATOR,,,'

        return csv_text
        
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check:\n- API key is valid\n- PDF is readable\n- Network connection is stable"

def csv_to_html(csv_text):
    """Convert CSV to HTML table for display - M2M Format"""
    # Use csv.reader to properly parse quoted fields
    lines_raw = csv_text.strip().split('\n')
    lines = list(csv.reader(lines_raw))

    html = '<div class="router-output">'
    in_operations_table = False

    for i, parts in enumerate(lines):
        # Get original line for string matching
        line_str = lines_raw[i] if i < len(lines_raw) else ""

        # Header line - MAC logo, title, page info (collect all 3 lines for header)
        if i == 0:
            page_info = parts[10] if len(parts) > 10 else (parts[9] if len(parts) > 9 else "")
            # Get date and time from lines 1 and 2
            date_info = ""
            time_info = ""
            if len(lines) > 1 and len(lines[1]) > 9:
                date_info = lines[1][9]
            if len(lines) > 2 and len(lines[2]) > 9:
                time_info = lines[2][9]

            html += f'''
            <div class="router-header">
                <div class="router-logo">{parts[0]}</div>
                <div class="router-title">{parts[5] if len(parts) > 5 else ""}</div>
                <div class="router-info">{page_info}<br>{date_info}<br>{time_info}</div>
            </div>
            '''
        # Skip date and time lines (already processed in header)
        elif i in [1, 2]:
            continue

        # Part info table header
        elif 'Facility' in line_str and 'Part Number' in line_str:
            html += '<table class="part-info-table"><thead><tr>'
            for cell in parts[:6]:
                if cell.strip():
                    html += f'<th>{cell}</th>'
            html += '</tr></thead><tbody>'

        # Operations table header
        elif 'Op' in line_str and 'Work Center' in line_str:
            html += '</tbody></table><table class="operations-table"><thead><tr>'
            for cell in parts[:11]:  # Now 11 columns instead of 10
                if cell.strip():
                    html += f'<th>{cell}</th>'
            html += '</tr></thead><tbody>'
            in_operations_table = True

        # Totals rows
        elif line_str.startswith('Totals'):
            html += '<tr class="totals-row">'
            # Ensure we always have 11 columns, padding with empty cells if needed
            padded_parts = parts + [''] * (11 - len(parts))  # Pad to 11 columns
            for j in range(11):
                cell = padded_parts[j] if j < len(padded_parts) else ''
                if cell.strip():
                    html += f'<td><strong>{cell}</strong></td>'
                else:
                    html += '<td></td>'
            html += '</tr>'

        # End of Report
        elif 'End of Report' in line_str:
            html += '</tbody></table>'
            html += '<div class="footer-line"></div>'
            html += '<div class="footer"><strong>End of Report</strong></div>'

        # Footer message (last line)
        elif i == len(lines) - 1 and len(parts) > 5:
            footer_msg = parts[5] if parts[5] else ""
            if footer_msg:
                html += f'<div class="footer-text">{footer_msg}</div>'

        # Data rows
        elif parts and parts[0] and parts[0].strip() and not line_str.startswith(','):
            html += '<tr>'
            for cell in parts[:11 if in_operations_table else 6]:  # Now 11 columns for operations
                html += f'<td>{cell}</td>'
            html += '</tr>'

        # Instruction rows (start with comma)
        elif line_str.startswith(',') and len(parts) > 1 and parts[1].strip():
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
                'content': "Please enter your Gemini API key in the sidebar to generate routers."
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
