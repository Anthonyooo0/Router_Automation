# MAC Router Generator - Technical Portfolio Entry

## Project Overview

**MAC Router Generator** is an AI-powered manufacturing router creation system that automates the traditionally manual process of creating production routing documents for Made2Manage (M2M) ERP systems. The application leverages Google's Gemini multimodal AI to analyze engineering drawings (PDFs) and generate standardized manufacturing routing summaries—a task that previously required experienced manufacturing engineers to complete manually.

### Core Technologies

| Category | Technology |
|----------|------------|
| **Language** | Python 3.11 |
| **Web Framework** | Streamlit 1.28+ |
| **AI/ML Engine** | Google Gemini API (multimodal) |
| **Image Processing** | Pillow (PIL) |
| **Data Processing** | Python CSV, RegEx, io |
| **Deployment** | VS Code DevContainers, Streamlit Cloud-ready |

### Architecture Pattern

**Single-File Monolithic with Functional Decomposition**

The application follows a deliberately streamlined architecture optimized for maintainability and deployment simplicity:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  Streamlit UI • Chat Interface • Session State Management    │
├─────────────────────────────────────────────────────────────┤
│                    BUSINESS LOGIC LAYER                      │
│  AI Prompt Engineering • CSV Validation Pipeline             │
├─────────────────────────────────────────────────────────────┤
│                    INTEGRATION LAYER                         │
│  Gemini API Client • PDF Processing • File I/O               │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Highlights

### 1. Advanced AI Prompt Engineering with Few-Shot Learning

The system implements sophisticated prompt engineering using **14 real-world manufacturing examples** as a knowledge base for few-shot learning. This approach constrains the AI's output to realistic, factory-validated parameters.

```python
# Knowledge base includes real production data:
# - Z110001B045: Sleeve Wiping Cap (115 pcs) - 2 OPERATIONS
# - Z005002A019: Position Holder Bracket (30 pcs) - WATERJET + BEND
# - TS01000B086: Spray Manifold Weldment (12 pcs) - WELD + SUB-PL
```

**Key Innovation:** Rather than relying solely on the AI's general knowledge, the embedded knowledge base provides:
- Standard setup times per work center (SAW: 0.25 hrs, CNC-L: 2.00 hrs, etc.)
- Realistic run time ranges (CNC-L: 2-3 min/piece max)
- Operation-specific instruction templates
- Decision trees for operation selection

### 2. 8-Step Deterministic CSV Validation Pipeline

The most technically sophisticated component is the **multi-stage CSV cleaning and validation pipeline** (lines 791-1083). This addresses a critical challenge: LLMs occasionally generate malformed output containing HTML tags, code snippets, or structural errors.

```
INPUT: Raw Gemini response (potentially malformed)
   ↓
Step 1: Extract text, remove markdown code blocks
Step 2: Remove HTML/XML tags via regex
Step 3: Filter code-like patterns (&&, ||, ==, <td>, etc.)
Step 4: Normalize whitespace
Step 5: Validate line structure (70% valid character threshold)
Step 6: Enforce operation→instruction→empty row pattern
Step 6.5: Auto-inject missing instruction rows per work center
Step 6.6: DETERMINISTIC totals calculation (override AI)
Step 7: Ensure proper spacing before totals
Step 8: Validate critical sections exist (add if missing)
   ↓
OUTPUT: Clean, M2M-compliant CSV
```

**Critical Design Decision:** Totals are calculated deterministically from parsed operation data rather than trusting AI-generated values—ensuring mathematical accuracy even when the AI makes calculation errors.

### 3. Multimodal Document Understanding

The system leverages Gemini's multimodal capabilities to:
- Process PDF engineering drawings as visual input
- Extract part numbers and descriptions from title blocks
- Interpret geometric features to determine appropriate operations
- Recognize material specifications and finish requirements

```python
uploaded = genai.upload_file(io.BytesIO(pdf_bytes), mime_type='application/pdf')
response = model.generate_content([uploaded, prompt], request_options={"timeout": 60})
```

### 4. ERP Integration Format Compliance

Output strictly adheres to Made2Manage (M2M) Standard Routing Summary format:

```csv
MAC,,,,,Standard Routing Summary,,,,,Page : 1 of 1
,,,,,,,,,Date : 01/19/2026
Facility,Part Number,Rev,Description,Unit of Measure,Standard Process Qty,,,
Default,Z110001B045,0,SLEEVE WIPING CAP,EA,115.00000,,,
Op,Work Center,Operation Description,Operation Qty,Setup Hours,Production Hours,Move Hours,Sub-Contract Costs,Other Costs,Standard Cost/Operation
10,SAW,CUT TO LENGTH,1.0000,0.25,0.01,0.00,0.00,0.00,0.00
,CUT MATERIAL TO LENGTH PER THE DWG.,,,,,,,,,
Totals,,,,2.25,3.84,0.00,0.00,0.00,0.00
```

### 5. Intelligent Operation-Specific Fallback System

When instruction rows are missing, the system auto-generates appropriate instructions based on work center type:

```python
# router_generator_app.py:949-964
if work_center.strip() == 'SAW':
    operation_fixed_lines.append(',CUT MATERIAL TO LENGTH PER THE DWG.,,,,,,,,,')
elif work_center.strip() == 'CNC-L':
    operation_fixed_lines.append(',MACHINE PART PER THE DWG AND DEBURR.,,,,,,,,,')
elif work_center.strip() == 'WATERJT':
    operation_fixed_lines.append(',VETTED S.O. [DATE] CUT OUT PER THE DWG AND DEBURR.,,,,,,,,,')
# ... (8 work center types supported)
```

### 6. Real-Time Session State Management

Streamlit's session state is leveraged for persistent conversation management:

```python
# Maintains across reruns:
st.session_state.chat_history = []      # Full conversation
st.session_state.router_generated = False
st.session_state.router_csv = ""        # Cached for export
st.session_state.quantity = 50          # Default production qty
```

### 7. ChatGPT-Style UI with Custom Theming

~400 lines of custom CSS implement a polished, branded interface:
- MAC Products corporate color scheme (#1E3A8A primary blue)
- Animated chat message bubbles with fade-in transitions
- Custom M2M-formatted router output tables with dashed instruction rows
- Responsive number input styling (hidden spin buttons)
- Keyboard shortcut support (Enter to submit)

---

## Key Features Built

| Feature | Technical Implementation |
|---------|-------------------------|
| **PDF Drawing Analysis** | Gemini multimodal API with 60s timeout, base64 encoding |
| **Router Generation** | Structured prompting with temperature 0.1 for deterministic output |
| **Multi-Model Support** | 6 Gemini models (3-flash-preview, 3-pro, 2.0-flash, etc.) |
| **CSV Export** | Direct download with timestamped filenames |
| **Raw CSV Viewer** | Syntax-highlighted code display for debugging |
| **Session Statistics** | Real-time router count tracking |
| **Conversation History** | Full chat persistence within session |
| **API Key Management** | Secure password-masked input with validation feedback |
| **One-Click Reset** | Clear conversation while preserving configuration |

---

## Technical Challenges Solved

### Challenge 1: LLM Output Inconsistency

**Problem:** Gemini occasionally outputs HTML tags, code operators, or malformed CSV structure despite explicit instructions.

**Solution:** Implemented a defense-in-depth validation pipeline with 8 distinct cleaning stages. Each stage addresses a specific failure mode:
- Regex-based HTML/XML tag removal
- Code pattern filtering (`<td>`, `&&`, `==`, etc.)
- Character validation with 70% threshold
- Structural pattern enforcement

### Challenge 2: Arithmetic Accuracy in AI-Generated Data

**Problem:** LLMs sometimes make calculation errors when summing operation hours.

**Solution:** Implemented deterministic totals calculation that parses operation rows and computes totals programmatically, overriding any AI-generated values:

```python
# router_generator_app.py:997-1023
for line in lines:
    if parts[0].strip().isdigit():  # Operation row
        setup_hours = float(parts[4].strip())
        run_hours = float(parts[5].strip())
        total_setup += setup_hours
        total_run += run_hours
```

### Challenge 3: Instruction Row Preservation

**Problem:** CSV parsing sometimes corrupted instruction rows containing commas (e.g., "PLATE, OUTSIDE VENDOR, ZINC PLATE").

**Solution:**
1. Used `csv.reader` for proper quoted-field handling
2. Implemented special SUB-PL instruction validation
3. Auto-quotes instruction fields containing commas

### Challenge 4: Constraining AI to Realistic Manufacturing Parameters

**Problem:** Without guidance, the AI might generate unrealistic operation counts or times.

**Solution:** Embedded a comprehensive knowledge base with 14 real examples emphasizing:
- "MOST MAC PARTS USE ONLY 2 OPERATIONS" (repeated for emphasis)
- Specific time ranges: "CNC-L: 2-3 min/piece MAX (if >5 min YOU'RE WRONG!)"
- Decision trees for operation selection

---

## Code Quality Indicators

### Design Patterns Used

| Pattern | Implementation |
|---------|----------------|
| **Pipeline Pattern** | 8-stage CSV validation with sequential transformations |
| **Template Method** | Operation-specific instruction templates |
| **State Pattern** | Streamlit session state for UI state management |
| **Factory Pattern** | Dynamic Gemini model instantiation |
| **Defensive Programming** | Multiple fallback mechanisms for missing data |

### Code Organization

```
router_generator_app.py (1,331 lines)
├── Configuration (17-22)           # Page setup
├── Theme/Styling (25-446)          # CSS with color constants
├── Session State (451-458)         # State initialization
├── Sidebar UI (463-546)            # Configuration panel
├── Knowledge Base (551-663)        # Manufacturing examples
├── Core Logic (668-1087)           # Router generation
├── CSV-to-HTML (1089-1181)         # Rendering
└── Main Interface (1184-1331)      # Chat and exports
```

### Error Handling Approach

- **API Errors:** Try/except with user-friendly messages
- **File Validation:** PDF format checking before upload
- **State Recovery:** Graceful handling of missing session data
- **Timeout Management:** 60-second request timeout with clear feedback
- **Fallback Content:** Auto-generated instructions when AI output incomplete

### Documentation Quality

- Module-level docstring describing purpose
- Section separators with clear labels
- Inline comments for complex logic
- Knowledge base doubles as documentation for manufacturing engineers

---

## Metrics & Scale

### Codebase Statistics

| Metric | Value |
|--------|-------|
| **Total Lines of Code** | 1,331 |
| **Python Source Lines** | ~900 (excluding CSS) |
| **Custom CSS Lines** | ~400 |
| **Core Functions** | 3 (generate_router, csv_to_html, load_logo) |
| **Validation Steps** | 8 |
| **Supported Work Centers** | 8 (SAW, CNC-L, CNC-M, WATERJT, BEND, WELD, PAINT, SUB-PL) |
| **Knowledge Base Examples** | 14 real manufacturing cases |
| **Supported Gemini Models** | 6 |

### API Configuration

| Parameter | Value |
|-----------|-------|
| **Temperature** | 0.1 (highly deterministic) |
| **Top P** | 0.95 |
| **Top K** | 40 |
| **Max Output Tokens** | 8,192 |
| **Request Timeout** | 60 seconds |

### Dependencies

```
streamlit>=1.28.0       # Web framework
google-generativeai>=0.2.0  # Gemini API
Pillow>=10.0.0          # Image processing
```

Minimal dependency footprint (3 packages) ensures easy deployment and maintenance.

---

## What Makes This Project Stand Out

1. **Domain Expertise Embedded in Code:** The knowledge base represents years of manufacturing experience codified into AI constraints.

2. **Defense-in-Depth for AI Reliability:** Rather than trusting AI output blindly, the 8-stage validation pipeline ensures data integrity.

3. **Deterministic Overrides:** Critical calculations (totals) are computed programmatically, not delegated to the AI.

4. **Production-Ready Integration:** Output format is immediately usable in Made2Manage ERP systems.

5. **Clean, Maintainable Architecture:** Despite being a single file, clear section separation and functional decomposition enable easy maintenance.

6. **Modern UX Design:** ChatGPT-inspired interface with corporate branding provides professional user experience.

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VS Code DevContainer                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 Python 3.11 Runtime                  │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │            Streamlit Server (:8501)          │    │    │
│  │  │  ┌───────────────────────────────────────┐  │    │    │
│  │  │  │         MAC Router Generator          │  │    │    │
│  │  │  │  ┌─────────────────────────────────┐  │  │    │    │
│  │  │  │  │    Google Gemini API Client     │──┼──┼────┼────┼──→ Gemini API
│  │  │  │  └─────────────────────────────────┘  │  │    │    │
│  │  │  └───────────────────────────────────────┘  │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Future Roadmap (Phase 2)

- Excel export functionality (currently disabled)
- User authentication integration
- Router versioning and history
- Batch PDF processing
- Integration with Made2Manage API for direct import

---

*This portfolio entry was generated from codebase analysis. The MAC Router Generator demonstrates expertise in AI integration, data validation, prompt engineering, and manufacturing domain knowledge.*
