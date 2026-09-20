"""
Agribusiness Market Analysis & Planning Report Generator
Generates a comprehensive, professional Word (.docx) report for Week 1 of the Agribusiness Data Science Project.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# --- Color Palette ---
COLOR_PRIMARY = RGBColor(19, 78, 52)      # Deep Forest Green #134E34
COLOR_SECONDARY = RGBColor(168, 104, 36)  # Warm Earth Amber #A86824
COLOR_DARK_TEXT = RGBColor(30, 41, 59)    # Slate Slate-800 #1E293B
COLOR_MUTED_TEXT = RGBColor(100, 116, 139)# Muted Slate #64748B
HEX_PRIMARY = "134E34"
HEX_LIGHT_BG = "F0FDF4"                   # Mint Tint
HEX_ALT_ROW = "F8FAFC"                    # Subtle Gray-Blue
HEX_BORDER = "CBD5E1"                     # Soft Border Gray

def set_cell_background(cell, fill_hex):
    """Sets background shading for a table cell."""
    tc_pr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    """Sets internal padding (in twips) for a table cell."""
    tc_pr = cell._element.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_cell_border(cell, **kwargs):
    """
    Sets specific borders on a cell.
    Format for kwargs: top={"val": "single", "sz": "4", "color": "HEX", "space": "0"}
    """
    tc_pr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge, attrs in kwargs.items():
        val = attrs.get("val", "single")
        sz = attrs.get("sz", "4")
        space = attrs.get("space", "0")
        color = attrs.get("color", "CBD5E1")
        border_elem = parse_xml(
            f'<w:{edge} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="{space}" w:color="{color}"/>'
        )
        borders.append(border_elem)
    tc_pr.append(borders)

def format_table(table, col_widths, col_alignments=None):
    """Applies standardized styling, borders, and column widths to a table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    num_rows = len(table.rows)
    num_cols = len(col_widths)

    for i, row in enumerate(table.rows):
        is_header = (i == 0)
        # Prevent row split across pages
        tr_pr = row._tr.get_or_add_trPr()
        tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if is_header:
            tr_pr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for j, cell in enumerate(row.cells):
            cell.width = col_widths[j]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

            if is_header:
                set_cell_background(cell, HEX_PRIMARY)
                set_cell_border(cell,
                                top={"sz": "6", "val": "single", "color": HEX_PRIMARY},
                                bottom={"sz": "12", "val": "single", "color": "0C3322"},
                                left={"sz": "0", "val": "none", "color": "auto"},
                                right={"sz": "0", "val": "none", "color": "auto"})
                for p in cell.paragraphs:
                    if col_alignments:
                        p.alignment = col_alignments[j]
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.name = "Calibri"
                        run.font.size = Pt(10)
            else:
                bg = HEX_ALT_ROW if (i % 2 == 1) else "FFFFFF"
                set_cell_background(cell, bg)
                set_cell_border(cell,
                                top={"sz": "4", "val": "single", "color": HEX_BORDER},
                                bottom={"sz": "4", "val": "single", "color": HEX_BORDER},
                                left={"sz": "0", "val": "none", "color": "auto"},
                                right={"sz": "0", "val": "none", "color": "auto"})
                for p in cell.paragraphs:
                    if col_alignments:
                        p.alignment = col_alignments[j]
                    for run in p.runs:
                        run.font.name = "Calibri"
                        run.font.size = Pt(9.5)
                        run.font.color.rgb = COLOR_DARK_TEXT

def add_callout(doc, text, bold_prefix=None):
    """Creates an executive callout box with a colored left accent border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.rows[0].cells[0].width = Inches(6.5)

    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, HEX_LIGHT_BG)
    set_cell_margins(cell, top=160, bottom=160, left=220, right=200)
    set_cell_border(cell,
                    left={"sz": "24", "val": "single", "color": HEX_PRIMARY},
                    top={"sz": "0", "val": "none", "color": "auto"},
                    bottom={"sz": "0", "val": "none", "color": "auto"},
                    right={"sz": "0", "val": "none", "color": "auto"})

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix + " ")
        r_bold.font.bold = True
        r_bold.font.color.rgb = COLOR_PRIMARY
        r_bold.font.name = "Calibri"
        r_bold.font.size = Pt(10)
    r_text = p.add_run(text)
    r_text.font.italic = True
    r_text.font.color.rgb = COLOR_DARK_TEXT
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10)

    # Empty spacer paragraph after callout
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def setup_document_styles(doc):
    """Sets standard typography and spacing across document styles."""
    styles = doc.styles

    # Normal Style
    normal = styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(11)
    normal.font.color.rgb = COLOR_DARK_TEXT
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    # Heading 1
    h1 = styles['Heading 1']
    h1.font.name = 'Calibri'
    h1.font.size = Pt(18)
    h1.font.bold = True
    h1.font.color.rgb = COLOR_PRIMARY
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(8)
    h1.paragraph_format.keep_with_next = True

    # Heading 2
    h2 = styles['Heading 2']
    h2.font.name = 'Calibri'
    h2.font.size = Pt(14)
    h2.font.bold = True
    h2.font.color.rgb = COLOR_SECONDARY
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.keep_with_next = True

    # Heading 3
    h3 = styles['Heading 3']
    h3.font.name = 'Calibri'
    h3.font.size = Pt(12)
    h3.font.bold = True
    h3.font.color.rgb = COLOR_DARK_TEXT
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(4)
    h3.paragraph_format.keep_with_next = True

def add_bullet_point(doc, bold_text, normal_text):
    """Adds a structured bullet point with bold lead-in."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r1 = p.add_run(bold_text)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_TEXT
    r2 = p.add_run(" " + normal_text)
    r2.font.color.rgb = COLOR_DARK_TEXT

def add_header_footer(doc):
    """Adds running headers and footers to the document."""
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

    # Header
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run("Agribusiness Market Analysis & Planning | Data Science Internship")
    hr.font.name = "Calibri"
    hr.font.size = Pt(8.5)
    hr.font.color.rgb = COLOR_MUTED_TEXT

    # Footer
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = fp.add_run("Confidential & Proprietary — Virtual Internship Foundation Deliverable")
    fr.font.name = "Calibri"
    fr.font.size = Pt(8.5)
    fr.font.color.rgb = COLOR_MUTED_TEXT

def build_full_report(output_path):
    """Constructs the comprehensive 10-section Agribusiness Analysis and Planning report."""
    doc = Document()
    setup_document_styles(doc)
    add_header_footer(doc)

    # =========================================================================
    # TITLE & METADATA SECTION
    # =========================================================================
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_before = Pt(20)
    r_badge = p_pre.add_run("WEEK 1 FOUNDATIONAL DELIVERABLE | APPLIED DATA SCIENCE")
    r_badge.font.bold = True
    r_badge.font.size = Pt(9.5)
    r_badge.font.color.rgb = COLOR_SECONDARY

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("Agribusiness Market Analysis & Planning:")
    r_title.font.bold = True
    r_title.font.size = Pt(24)
    r_title.font.color.rgb = COLOR_PRIMARY
    p_subtitle = doc.add_paragraph()
    p_subtitle.paragraph_format.space_after = Pt(16)
    r_sub = p_subtitle.add_run("A Comprehensive Industry Landscape, Stakeholder Matrix, and Conceptual Data Science Framework")
    r_sub.font.size = Pt(14)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED_TEXT

    # Metadata Box
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Inches(2.2), Inches(4.3)]
    meta_data = [
        ("Author / Intern Role:", "Agribusiness Data Science & Strategy Intern"),
        ("Project Scope:", "Week 1: Market Intelligence, Architecture & Research Roadmap"),
        ("Industry Domain:", "Agritechnology, Commodity Markets, Farm Management & Food Systems"),
        ("Analytical Focus:", "Predictive Modeling, Remote Sensing, Supply Chain Optimization & ESG")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_tbl.rows[idx]
        row.cells[0].width = col_w[0]
        row.cells[1].width = col_w[1]
        set_cell_background(row.cells[0], HEX_ALT_ROW)
        set_cell_background(row.cells[1], "FFFFFF")
        set_cell_margins(row.cells[0], 60, 60, 100, 100)
        set_cell_margins(row.cells[1], 60, 60, 100, 100)
        set_cell_border(row.cells[0], bottom={"sz": "4", "val": "single", "color": HEX_BORDER})
        set_cell_border(row.cells[1], bottom={"sz": "4", "val": "single", "color": HEX_BORDER})
        
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_DARK_TEXT

        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY
    # =========================================================================
    doc.add_heading("1. Executive Summary", level=1)
    
    doc.add_paragraph(
        "The global agribusiness sector represents a foundational pillar of human survival, economic vitality, "
        "and geopolitical stability. Encompassing an expansive global value chain valued in excess of $3.8 trillion, "
        "the industry is responsible for feeding an expanding world population projected to reach 9.8 billion by 2050. "
        "To satisfy this burgeoning caloric and nutritional demand, agricultural production must increase by an estimated "
        "60% to 70% from current baselines. However, this production surge must be achieved in an era characterized by acute "
        "arable land constraints, freshwater depletion, catastrophic climate volatility, escalating geopolitical friction, "
        "and stringent global regulatory decarbonization mandates."
    )
    doc.add_paragraph(
        "Historically dominated by empirical intuition, localized trial-and-error, and fragmented commodity intermediaries, "
        "the agribusiness sector is currently experiencing a historic paradigm shift: the transition toward hyper-precision, "
        "data-driven agriculture (AgTech 4.0). This revolution unites ubiquitous Internet of Things (IoT) sensors, multi-spectral "
        "satellite remote sensing, automated farm machinery telemetry, genomics, and advanced artificial intelligence. "
        "Despite this technological inflection point, agribusiness stakeholders—ranging from resource-constrained smallholders "
        "to multi-national grain conglomerates—continue to grapple with persistent structural inefficiencies, severe post-harvest "
        "spoilage (averaging 30% to 40% in emerging economies), extreme commodity price elasticity, and asymmetrical information distribution."
    )

    add_callout(
        doc,
        "This foundational report serves as the strategic anchor for the Data Science Virtual Internship. "
        "It provides a multi-dimensional examination of the macro agribusiness landscape, decomposes key sub-sectors, "
        "evaluates stakeholder dynamics, formulates a 4-tier Key Performance Indicator (KPI) taxonomy, and constructs "
        "an end-to-end Conceptual Data Science Framework. This architecture bridges raw agronomic/remote sensing data with "
        "advanced predictive machine learning to guide subsequent technical weeks.",
        bold_prefix="Core Strategic Purpose:"
    )

    doc.add_paragraph(
        "The subsequent analytical tasks of this internship will directly leverage the conceptual data pipeline, feature schemas, "
        "and empirical research directions synthesized in this report. By harmonizing disparate data domains—such as satellite-derived "
        "vegetation indices, gridded reanalysis climatology, soil geochemical metrics, and wholesale commodity futures—data scientists "
        "can build resilient, scalable models that optimize farm profitability, mitigate systemic climate risks, and secure "
        "global food distribution systems."
    )

    # =========================================================================
    # SECTION 2: MACRO ENVIRONMENT & GLOBAL VALUE CHAIN ARCHITECTURE
    # =========================================================================
    doc.add_heading("2. Macro Environment & Value Chain Architecture", level=1)

    doc.add_paragraph(
        "A rigorous analysis of agribusiness requires deconstructing the macro-environmental forces shaping the sector, "
        "followed by a structural examination of its value chain components. The macro environment can be comprehensively "
        "mapped through the PESTLE (Political, Economic, Social, Technological, Legal, Environmental) analytical paradigm."
    )

    doc.add_heading("2.1 PESTLE Environmental Analysis", level=2)

    pestle_tbl = doc.add_table(rows=7, cols=3)
    p_widths = [Inches(1.2), Inches(2.3), Inches(3.0)]
    p_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    pestle_tbl.rows[0].cells[0].paragraphs[0].text = "Dimension"
    pestle_tbl.rows[0].cells[1].paragraphs[0].text = "Macro-Environmental Factor"
    pestle_tbl.rows[0].cells[2].paragraphs[0].text = "Structural Agribusiness Impact"

    pestle_data = [
        ("Political", "Geopolitical conflicts & trade protectionism (e.g., Black Sea grain disruptions, fertilizer export bans).", 
         "Causes sudden commodity supply shortages, drives domestic food sovereignty policies, and triggers rapid price volatility across cereal imports."),
        ("Economic", "Inflationary pressure on synthetic inputs, fluctuating energy tariffs, and interest rate hikes.",
         "Compresses operational margins for farmers, elevates credit default risk, and forces consolidation among agricultural retailers and equipment financiers."),
        ("Social", "Consumer preference shifts toward organic, clean-label, non-GMO, and carbon-neutral food sources.",
         "Requires farm-to-fork traceability, incentivizes regenerative farming, and reshapes demand for plant-based alternative proteins and functional crops."),
        ("Technological", "Convergence of Edge-AI, robotic automation, low-Earth orbit (LEO) satellite constellations, and synthetic biology.",
         "Democratizes real-time field diagnostics, enables variable-rate input application, and enhances crop resilience via targeted genetic editing (CRISPR)."),
        ("Legal", "Rigorous environmental mandates (e.g., EU Deforestation Regulation [EUDR], SEC Climate Disclosures, pesticide bans).",
         "Imposes mandatory spatial supply chain auditing, penalizes undocumented land conversion, and necessitates verifiable ESG data reporting."),
        ("Environmental", "Anthropogenic climate change, mega-droughts, erratic monsoon cycles, and topsoil erosion.",
         "Reduces historical harvest predictability, shifts arable agro-ecological zones poleward, and elevates systemic multi-breadbasket failure risks.")
    ]

    for idx, (dim, factor, impact) in enumerate(pestle_data, start=1):
        r = pestle_tbl.rows[idx]
        r.cells[0].paragraphs[0].text = dim
        r.cells[1].paragraphs[0].text = factor
        r.cells[2].paragraphs[0].text = impact

    format_table(pestle_tbl, p_widths, p_aligns)

    doc.add_heading("2.2 Deconstructing the Agribusiness Value Chain", level=2)
    doc.add_paragraph(
        "The agribusiness value chain is characterized by a high degree of interdependency spanning three distinct stages: "
        "Upstream, Midstream, and Downstream. Inefficiencies or information bottlenecks in any one tier propagate non-linear "
        "disruptions across the entire system, commonly termed the agricultural 'bullwhip effect'."
    )

    doc.add_heading("Upstream Sector (Agricultural Inputs & Technology)", level=3)
    add_bullet_point(doc, "Crop Genetics & Seed Production:", "Dominated by consolidated life-science conglomerates (Bayer CropScience, Corteva Agriscience, Syngenta) investing heavily in germplasm optimization, drought-tolerant hybrid traits, and disease-resistant transgenic cultivars.")
    add_bullet_point(doc, "Crop Nutrition & Protection:", "Includes macro-nutrients (Nitrogen via Haber-Bosch, Phosphorus, Potassium - NPK), specialized micro-nutrients, and crop protection chemicals (herbicides, insecticides, fungicides). The sector is experiencing rapid expansion in biologicals (microbials, bio-stimulants, and pheromone-based biocontrol).")
    add_bullet_point(doc, "Agricultural Machinery & Hardware:", "Global original equipment manufacturers (John Deere, CNH Industrial, AGCO, Kubota) integrating GPS auto-steer, ISOBUS telematics, variable-rate seeding/spraying actuators, and autonomous field robotics.")
    add_bullet_point(doc, "Digital Agronomy & Telemetry:", "IoT soil moisture probes, weather stations, drone multi-spectral imaging rigs, and farm management software (FMS) capturing granular spatial data at field scale.")

    doc.add_heading("Midstream Sector (Farming Operations & Primary Consolidation)", level=3)
    add_bullet_point(doc, "Farm Enterprise Operations:", "Encompasses primary cultivation, planting, crop scouting, irrigation management, and mechanical harvesting. Operational profiles diverge sharply between large-scale industrial farms (>500 hectares) and fragmented smallholders (<2 hectares).")
    add_bullet_point(doc, "First-Mile Aggregation & Post-Harvest Storage:", "Local collection centers, grain elevators, on-farm silo networks, and co-operative aggregation hubs. Critical operational challenges include grain drying, moisture stabilization, fumigation, and sorting.")
    add_bullet_point(doc, "Cold Chain Infrastructure:", "Temperature- and humidity-controlled logistics crucial for perishable horticulture, floriculture, dairy, and meat. A lack of uninterrupted cold chains is the primary driver of upstream food loss in tropical developing economies.")

    doc.add_heading("Downstream Sector (Processing, Distribution & Consumption)", level=3)
    add_bullet_point(doc, "Global Commodity Trading & Crushing:", "Dominated by the historic 'ABCD' quadrumvirate (Archer Daniels Midland, Bunge, Cargill, Louis Dreyfus Company), responsible for bulk international grain chartering, oilseed crushing, wet milling, and global arbitrage.")
    add_bullet_point(doc, "Secondary Food & Industrial Processing:", "Fast-Moving Consumer Goods (FMCG) corporations (Nestle, PepsiCo, Unilever, Danone) converting raw agricultural commodities into branded food, beverage, livestock feed, biofuels (ethanol, biodiesel), and biochemical inputs.")
    add_bullet_point(doc, "Wholesale, Retail & Foodservice Distribution:", "Supermarket chains, institutional food service distributors, and emerging quick-commerce platforms dictating rigorous quality standards, traceability protocols, and supplier delivery windows.")

    # =========================================================================
    # SECTION 3: INDUSTRY TRENDS, CRITICAL CHALLENGES & INNOVATION OPPORTUNITIES
    # =========================================================================
    doc.add_heading("3. Industry Trends, Critical Challenges & Innovation Opportunities", level=1)

    doc.add_paragraph(
        "A rigorous appraisal of the contemporary agribusiness landscape reveals a dynamic tension between pressing systemic "
        "vulnerabilities and transformative technological frontiers. Navigating these dynamics requires an evidence-based "
        "assessment of macroeconomic trends and the application of data-driven solutions."
    )

    doc.add_heading("3.1 Major Industry Trends", level=2)
    add_bullet_point(doc, "Hyperspectral & Satellite-Driven Precision Agronomy:", "The transition from broad field-level management to sub-meter, intra-field variable rate management. The proliferation of high-revisit Earth Observation constellations (Copernicus Sentinel-2, PlanetScope) allows weekly monitoring of vegetation health, nitrogen uptake, and canopy water stress.")
    add_bullet_point(doc, "Autonomous Field Equipment & Edge-AI:", "Commercial deployment of autonomous tractors, targeted robotic weeding systems (e.g., John Deere See & Spray utilizing high-speed edge computer vision to reduce herbicide volumes by up to 75%), and autonomous drone swarms for aerial spraying.")
    add_bullet_point(doc, "Regenerative Agriculture & Biological Transition:", "Rapid adoption of conservation tillage, multi-species cover cropping, bio-fertilizers, and microbial seed coatings designed to restore degraded soil microbiomes and sequester atmospheric carbon.")
    add_bullet_point(doc, "Agri-FinTech & Parametric Index Insurance:", "Financial inclusion platforms leveraging alternative digital agronomic footprints (satellite yield estimates, mobile money payment histories) to underwrite smallholder micro-loans and execute smart-contract parametric drought insurance payouts without manual claims adjustment.")
    add_bullet_point(doc, "Supply Chain Provenance & Digital Traceability:", "Integration of QR-code serialization and distributed ledger technologies to comply with regulatory mandates regarding deforestation-free commodity supply chains and corporate Scope 3 greenhouse gas reporting.")

    doc.add_heading("3.2 Critical Industry Challenges", level=2)
    
    chal_tbl = doc.add_table(rows=5, cols=3)
    c_widths = [Inches(1.8), Inches(2.4), Inches(2.3)]
    c_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    chal_tbl.rows[0].cells[0].paragraphs[0].text = "Core Challenge"
    chal_tbl.rows[0].cells[1].paragraphs[0].text = "Underlying Causal Mechanism"
    chal_tbl.rows[0].cells[2].paragraphs[0].text = "Socio-Economic & Environmental Consequence"

    chal_data = [
        ("Post-Harvest Spoilage & Wastage",
         "Sub-optimal grain storage structures, inadequate hermetic sealing, moisture control failure, and severed cold-chain links.",
         "Loss of 30-40% of total harvested food in developing markets; severe income degradation for smallholders; wasted embedded irrigation water and carbon."),
        ("Water Depletion & Salinization",
         "Inefficient flood irrigation practices, unmetered groundwater overdraft, and poor drainage inducing soil salinization.",
         "Depletion of critical aquifers (e.g., Ogallala, Indo-Gangetic Basin); desertification of fertile arable land; escalating regional resource conflict."),
        ("Commodity Price Volatility & Asymmetry",
         "Severe weather shocks, speculative commodity index trading, and fragmented local spot market information.",
         "Producers forced into distress selling at harvest lows; price gouging by middlemen; inability for growers to secure long-term capital investments."),
        ("Soil Degradation & Nutrient Depletion",
         "Decades of intensive mono-cropping, synthetic chemical over-application, and neglect of soil organic matter (SOM).",
         "Diminishing marginal crop yield returns per unit of chemical fertilizer; accelerated topsoil erosion; catastrophic loss of soil biodiversity.")
    ]

    for idx, (c, m, cons) in enumerate(chal_data, start=1):
        r = chal_tbl.rows[idx]
        r.cells[0].paragraphs[0].text = c
        r.cells[1].paragraphs[0].text = m
        r.cells[2].paragraphs[0].text = cons

    format_table(chal_tbl, c_widths, c_aligns)

    doc.add_heading("3.3 High-Value Innovation Opportunities for Data Science", level=2)
    doc.add_paragraph(
        "Data science and advanced quantitative modeling represent the highest-leverage intervention points to resolve "
        "these systemic challenges. Specifically, four key innovation clusters present immediate viability for analytical execution:"
    )

    add_bullet_point(doc, "1. Predictive In-Season Crop Yield Estimation:", "Combining multi-temporal satellite vegetation indices (NDVI, EVI, NDRE) with gridded meteorological reanalysis (ERA5 temperature, precipitation, vapor pressure deficit) and soil moisture profiles within gradient-boosted decision trees (XGBoost/LightGBM) or Long Short-Term Memory (LSTM) neural networks. This equips grain traders, insurers, and food security planners with reliable harvest forecasts 60 to 90 days prior to combine operation.")
    add_bullet_point(doc, "2. Real-Time Computer Vision for Crop Diagnostics:", "Deploying convolutional neural network architectures (e.g., YOLOv8, EfficientNet) trained on annotated plant pathology datasets (e.g., PlantVillage) directly on mobile edge devices. Smallholders can photograph leaf lesions to receive instantaneous disease identification (e.g., Northern Corn Leaf Blight, Fall Armyworm) and calibrated pesticide dosage recommendations.")
    add_bullet_point(doc, "3. Multi-Variate Commodity Price Forecasting:", "Engineering hybrid statistical and deep learning forecasting engines (e.g., SARIMAX with exogenous macroeconomic regressors, Prophet, Temporal Fusion Transformers) that ingest global ocean-atmospheric climate oscillation indices (ENSO, Indian Ocean Dipole), regional crop condition scores, port inventory volumes, and energy prices to forecast wholesale spot prices.")
    add_bullet_point(doc, "4. Spatial Logistics & Cold-Chain Fleet Optimization:", "Utilizing mixed-integer linear programming (MILP) and graph neural networks to optimize milk and fresh produce collection routes, dynamically routing temperature-controlled fleets to minimize fuel burn and prevent cold-chain decay.")

    # =========================================================================
    # SECTION 4: MARKET SEGMENTATION & STAKEHOLDER ANALYSIS
    # =========================================================================
    doc.add_heading("4. Comprehensive Market Segmentation & Stakeholder Analysis", level=1)

    doc.add_paragraph(
        "Developing effective data-driven strategies requires a granular segmentation of the agribusiness landscape, "
        "coupled with a systematic analysis of stakeholder power dynamics, operational incentives, and strategic bottlenecks."
    )

    doc.add_heading("4.1 Market Segmentation Dimensions", level=2)
    doc.add_paragraph(
        "The agribusiness sector cannot be treated as a monolithic industry. It must be segmented across four structural axes: "
        "Sub-sector taxonomy, Farm operational scale, Geographical agro-ecological zones, and Value chain orientation."
    )

    seg_tbl = doc.add_table(rows=5, cols=4)
    s_widths = [Inches(1.5), Inches(1.6), Inches(1.8), Inches(1.6)]
    s_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    seg_tbl.rows[0].cells[0].paragraphs[0].text = "Segmentation Axis"
    seg_tbl.rows[0].cells[1].paragraphs[0].text = "Primary Categories"
    seg_tbl.rows[0].cells[2].paragraphs[0].text = "Key Operational Attributes"
    seg_tbl.rows[0].cells[3].paragraphs[0].text = "Data Science Applicability"

    seg_data = [
        ("Sub-Sector", 
         "• Arable Row Crops\n• High-Value Horticulture\n• Livestock & Dairy\n• Aquaculture\n• Forestry & Biomass",
         "Varying production cycles, perishability windows, capital intensity, and storage durability.",
         "Spectral index monitoring for row crops; vision-based grading for horticulture; acoustic monitoring in livestock."),
        ("Operational Scale", 
         "• Smallholder (<2 ha)\n• Medium Commercial (2-50 ha)\n• Industrial Mega-Farms (>50 ha)",
         "Smallholders feature high labor density and low capital; industrial farms exhibit high mechanization and telemetry adoption.",
         "Low-bandwidth mobile advisory for smallholders; complex multi-spectral variable-rate prescription maps for mega-farms."),
        ("Geographical & Agro-Ecological", 
         "• Temperate Plains (US Midwest, Ukraine)\n• Tropical Monsoon (SE Asia, India)\n• Semi-Arid (Sub-Saharan Africa)\n• Mediterranean",
         "Determines soil moisture balance, frost risk, pest pressure, growing degree days, and double-cropping feasibility.",
         "Localized transfer learning; regional climate-adjusted yield baselines; drought anomaly detection algorithms."),
        ("Value Chain Orientation", 
         "• Input Manufacturers\n• Commercial Producers\n• Aggregators / Co-ops\n• Processors & Retailers",
         "Disparate profit margins, regulatory exposures, capital turn cycles, and inventory perishability profiles.",
         "Demand forecasting for inputs; production optimization for farms; routing and spoilage reduction for distributors.")
    ]

    for idx, (axis, cat, attr, app) in enumerate(seg_data, start=1):
        r = seg_tbl.rows[idx]
        r.cells[0].paragraphs[0].text = axis
        r.cells[1].paragraphs[0].text = cat
        r.cells[2].paragraphs[0].text = attr
        r.cells[3].paragraphs[0].text = app

    format_table(seg_tbl, s_widths, s_aligns)

    doc.add_heading("4.2 Comprehensive Stakeholder Analysis", level=2)
    doc.add_paragraph(
        "To ensure analytical solutions create tangible commercial and societal value, we map primary stakeholders across "
        "a Power-Interest matrix, detailing their core objectives, primary pain points, and high-priority data science touchpoints."
    )

    stk_tbl = doc.add_table(rows=7, cols=5)
    stk_widths = [Inches(1.2), Inches(0.9), Inches(1.4), Inches(1.5), Inches(1.5)]
    stk_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    stk_tbl.rows[0].cells[0].paragraphs[0].text = "Stakeholder"
    stk_tbl.rows[0].cells[1].paragraphs[0].text = "Power / Interest"
    stk_tbl.rows[0].cells[2].paragraphs[0].text = "Strategic Objective"
    stk_tbl.rows[0].cells[3].paragraphs[0].text = "Critical Pain Point"
    stk_tbl.rows[0].cells[4].paragraphs[0].text = "Data Science Opportunity"

    stk_data = [
        ("Farmers & Growers (Smallholders)", "Low Power\nHigh Interest",
         "Maximize net yield per hectare; minimize debt; ensure household food security.",
         "Asymmetrical spot market pricing, unpredictable weather shocks, limited working capital.",
         "Hyper-local weather alerts, SMS pest diagnostics, transparent digital marketplace pricing."),
        ("Commercial Farm Enterprises", "Medium Power\nHigh Interest",
         "Maximize Return on Invested Capital (ROIC); optimize input efficiency; automate labor.",
         "Equipment telematics fragmentation, escalating fertilizer costs, skilled operator shortages.",
         "Variable-rate input algorithms, automated yield monitor calibration, predictive equipment maintenance."),
        ("Input Manufacturers (Seeds / Agrochem)", "High Power\nHigh Interest",
         "Drive sales volume of proprietary seeds/chemicals; forecast regional demand; protect patents.",
         "Regulatory scrutiny over chemical toxicity, long R&D cycles (8-10 years), supply chain bottlenecks.",
         "Genomic prediction algorithms for trait discovery; regional demand forecasting based on satellite planting data."),
        ("Grain Traders & Aggregators (ABCD)", "High Power\nHigh Interest",
         "Maintain crushing/storage margins; optimize international bulk shipping; manage commodity risk.",
         "Macro supply shocks, port congestion, sudden tariff shifts, storage grain insect infestations.",
         "Global satellite-based pre-harvest yield modeling, spatial commodity flow tracking, trade-route optimization."),
        ("Financial Institutions & Crop Insurers", "High Power\nMedium Interest",
         "Deploy agricultural capital safely; reduce non-performing loans (NPLs); scale insurance portfolios.",
         "High cost of manual loss adjustments, lack of credit bureau coverage in rural areas, adverse selection.",
         "Satellite-verified parametric drought payouts, digital credit scoring incorporating farm vegetation vigor."),
        ("Government Ministries & Multilaterals", "High Power\nHigh Interest",
         "Ensure national food sovereignty; stabilize consumer food inflation; meet net-zero carbon pledges.",
         "Lack of reliable census data, delayed yield reporting, fiscal waste in untargeted input subsidies.",
         "National food balance sheet modeling, geospatial disaster damage assessment, subsidy targeting algorithms.")
    ]

    for idx, (s, p, o, pp, ds) in enumerate(stk_data, start=1):
        r = stk_tbl.rows[idx]
        r.cells[0].paragraphs[0].text = s
        r.cells[1].paragraphs[0].text = p
        r.cells[2].paragraphs[0].text = o
        r.cells[3].paragraphs[0].text = pp
        r.cells[4].paragraphs[0].text = ds

    format_table(stk_tbl, stk_widths, stk_aligns)

    # =========================================================================
    # SECTION 5: KEY PERFORMANCE INDICATORS (KPIS) TAXONOMY
    # =========================================================================
    doc.add_heading("5. Agribusiness Key Performance Indicators (KPIs) Taxonomy", level=1)

    doc.add_paragraph(
        "A rigorous data-driven agribusiness framework demands a standardized, multi-tiered hierarchy of Key Performance "
        "Indicators (KPIs). These metrics bridge raw sensor and transactional inputs with strategic enterprise outcomes, "
        "spanning four essential domains: Agronomic, Operational & Supply Chain, Financial & Market, and Sustainability & ESG."
    )

    kpi_tbl = doc.add_table(rows=13, cols=4)
    k_widths = [Inches(1.3), Inches(1.8), Inches(1.8), Inches(1.6)]
    k_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    kpi_tbl.rows[0].cells[0].paragraphs[0].text = "Domain"
    kpi_tbl.rows[0].cells[1].paragraphs[0].text = "Key Performance Indicator"
    kpi_tbl.rows[0].cells[2].paragraphs[0].text = "Measurement Methodology / Formula"
    kpi_tbl.rows[0].cells[3].paragraphs[0].text = "Target / Benchmark Standard"

    kpis = [
        ("Agronomic", "Yield per Hectare (YPH)", "Total Clean Harvest Mass (kg) / Harvested Area (ha)", "Crop-specific (e.g., Corn: 10-12 t/ha US, 2-3 t/ha Sub-Saharan Africa)"),
        ("Agronomic", "Normalized Difference Veg. Index (NDVI)", "(NIR - Red) / (NIR + Red) via Satellite / UAV Multispectral", "Dense Healthy Canopy: 0.65 - 0.85; Bare/Stressed: < 0.30"),
        ("Agronomic", "Water Use Efficiency (WUE)", "Crop Yield Output (kg/ha) / Total Water Consumed (ET in mm)", "Maize: 1.5 - 2.5 kg/m³; Wheat: 1.0 - 1.8 kg/m³"),
        ("Agronomic", "Nitrogen Use Efficiency (NUE)", "Harvested N in Biomass / Total N Applied from Fertilizer", "Global benchmark: >65%; Typical actual: 40-50%"),
        ("Operational", "Post-Harvest Loss Rate (PHL)", "(Mass Lost between Harvest & Retail / Total Harvest Mass) * 100", "Developed: < 5-8%; Developing: Target < 15% (Current: 30-40%)"),
        ("Operational", "Cold-Chain Temperature Compliance", "(Hours within Specified Temp Envelope / Total Transit Hours) * 100", "Strict Pharmaceutical / Fresh Produce: > 99.5%"),
        ("Operational", "Grain Silo Moisture Equilibrium", "Continuous Moisture Meter Sampling (%) within Aeration Range", "Long-term safe cereal storage: 12.5% - 13.5%"),
        ("Financial", "Net Margin per Hectare (NMH)", "(Gross Crop Revenue - Total Variable & Fixed Operating Costs) / ha", "Row crops target: > $250 - $400/ha net margin"),
        ("Financial", "Farm-Gate to Retail Price Spread", "((Retail Consumer Price - Farm-Gate Price) / Retail Price) * 100", "Grains: 40-60%; Perishables: 60-80% (Middlemen capture)"),
        ("Financial", "Loan Default Rate (NPL)", "(Total Value of Defaulted Agricultural Loans / Total Agri-Loan Portfolio) * 100", "Commercial bank standard: < 3.5%; Agri-lending target: < 5.0%"),
        ("Sustainability", "Soil Organic Carbon (SOC)", "Dry Combustion elemental analysis (% C in top 30cm soil)", "Healthy agricultural soil: > 2.0% - 3.5% organic carbon"),
        ("Sustainability", "Emissions Intensity per Unit", "Total kg CO2-equivalent emitted / kg finished produce", "Target: Year-over-year 5-7% decarbonization reduction")
    ]

    for idx, (dom, name, meth, bench) in enumerate(kpis, start=1):
        r = kpi_tbl.rows[idx]
        r.cells[0].paragraphs[0].text = dom
        r.cells[1].paragraphs[0].text = name
        r.cells[2].paragraphs[0].text = meth
        r.cells[3].paragraphs[0].text = bench

    format_table(kpi_tbl, k_widths, k_aligns)

    # =========================================================================
    # SECTION 6: CONCEPTUAL DATA SCIENCE & ANALYTICS FRAMEWORK
    # =========================================================================
    doc.add_heading("6. Conceptual Data Science & Analytics Framework", level=1)

    doc.add_paragraph(
        "To systematically bridge agribusiness market intelligence with technical execution, we propose an enterprise-grade "
        "Conceptual Data Science Architecture. This framework governs end-to-end data pipelines: from multi-modal ingestion "
        "of heterogeneous geospatial, weather, and market data, through feature engineering and predictive modeling, to downstream "
        "decision-support interfaces."
    )

    doc.add_heading("6.1 Architectural Overview: The 4-Tier Pipeline", level=2)

    doc.add_paragraph(
        "The architecture is organized into four sequential, decoupled layers designed to handle high-volume spatio-temporal datasets, "
        "ensure reproducibility, and deliver low-latency inference for field stakeholders:"
    )

    add_bullet_point(doc, "Tier 1: Multi-Modal Ingestion & Storage:", "Continuous ingestion from four heterogeneous domains: Earth Observation satellites (Sentinel-2, Landsat-8/9 via Cloud-Optimized GeoTIFFs), Numerical Weather Prediction reanalysis (ECMWF ERA5, NOAA GFS), ground-truth telemetry (ISOBUS tractor logs, soil moisture probes, IoT weather stations), and transactional market APIs (USDA NASS, FAOSTAT, CBOT futures, regional mandi spot prices). Data lands in an Amazon S3/GCS object storage data lake partitioned by H3 geospatial index and ISO timestamp.")
    add_bullet_point(doc, "Tier 2: Preprocessing, Geospatial Harmonization & Feature Store:", "Cloud-native ETL pipelines executing cloud-masking (SCL band), radiometric calibration, spatial resampling to unified 10m grids, temporal interpolation of missing satellite observations, and gridded reanalysis downscaling. Features are registered in a centralized Feature Store (e.g., Feast/Hopsworks), facilitating consistent training-serving skew prevention.")
    add_bullet_point(doc, "Tier 3: Analytical & Machine Learning Modeling Engine:", "Specialized machine learning pipelines executing four core workloads: (a) In-season yield prediction via XGBoost/LightGBM and Temporal Fusion Transformers; (b) Phenology stage classification via 1D-CNNs on NDVI time-series; (c) Crop pathology detection via YOLOv8 object detection; and (d) Wholesale price forecasting using hybrid SARIMAX-LSTM architectures.")
    add_bullet_point(doc, "Tier 4: Operational Decision Support & API Services:", "Model outputs deployed via containerized FastAPI microservices powering role-specific user interfaces: mobile USSD/SMS advisory for smallholders, GIS prescription map export for autonomous sprayers, and executive risk dashboards for commodity traders.")

    doc.add_heading("6.2 Data Points & Schema Catalog for Exploration", level=2)
    doc.add_paragraph(
        "The following catalog details the exact feature schema and public data sources designated for analytical exploration "
        "in subsequent internship tasks:"
    )

    data_tbl = doc.add_table(rows=8, cols=5)
    d_widths = [Inches(1.4), Inches(1.3), Inches(1.2), Inches(1.2), Inches(1.4)]
    d_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    data_tbl.rows[0].cells[0].paragraphs[0].text = "Variable Name"
    data_tbl.rows[0].cells[1].paragraphs[0].text = "Primary Data Source"
    data_tbl.rows[0].cells[2].paragraphs[0].text = "Spatial / Temporal Res."
    data_tbl.rows[0].cells[3].paragraphs[0].text = "Data Type & Format"
    data_tbl.rows[0].cells[4].paragraphs[0].text = "Analytical Target / Purpose"

    data_points = [
        ("Surface Reflectance (B2, B3, B4, B8, B11, B12)", "Copernicus Sentinel-2 (ESA)", "10m - 20m / 5-day revisit", "Raster GeoTIFF (Float32)", "Calculate vegetation indices (NDVI, NDRE, NDWI); crop canopy vigor."),
        ("Precipitation & Cumulative Rainfall", "CHIRPS / ECMWF ERA5-Land", "0.05° (~5km) / Daily", "Gridded NetCDF / Zarr", "Quantify drought stress, water deficit anomalies, and flood inundation."),
        ("Surface Temperature (T2m Min/Max/Mean)", "ECMWF ERA5 / NOAA GFS", "0.1° (~9km) / Hourly - Daily", "Gridded NetCDF (Kelvin)", "Compute Growing Degree Days (GDD), heat shock degree days, frost exposure."),
        ("Soil Volumetric Water Content (0-7cm, 7-28cm)", "NASA SMAP / ERA5-Land", "0.1° (~9km) / Daily", "Gridded NetCDF (m³/m³)", "Evaluate root-zone soil moisture exhaustion and irrigation requirements."),
        ("Soil Geochemical Properties (pH, SOC, Clay, Sand)", "ISRIC SoilGrids 250m", "250m / Static baseline", "Raster GeoTIFF / CSV", "Model baseline soil fertility, cation exchange capacity, yield potential."),
        ("Wholesale Commodity Spot & Futures Prices", "CME/CBOT, World Bank, Local Mandi APIs", "Market-level / Daily", "Tabular Time-Series (JSON/CSV)", "Train multi-variate commodity price forecasting and arbitrage models."),
        ("Historical Harvest Yields & Cultivated Area", "USDA NASS, FAOSTAT, National Agri-Portals", "County / District / Annual", "Tabular CSV (Float)", "Ground-truth target variable (kg/ha) for supervised yield regression.")
    ]

    for idx, (var, src, res, typ, purp) in enumerate(data_points, start=1):
        r = data_tbl.rows[idx]
        r.cells[0].paragraphs[0].text = var
        r.cells[1].paragraphs[0].text = src
        r.cells[2].paragraphs[0].text = res
        r.cells[3].paragraphs[0].text = typ
        r.cells[4].paragraphs[0].text = purp

    format_table(data_tbl, d_widths, d_aligns)

    doc.add_heading("6.3 Mathematical & Algorithmic Formulations", level=2)
    doc.add_paragraph(
        "To ground future data science tasks in empirical rigor, key predictive models are formulated mathematically below:"
    )

    doc.add_heading("1. In-Season Crop Yield Regression Model", level=3)
    doc.add_paragraph(
        "Crop yield Y_i for field i at harvest time T is modeled as a non-linear function of time-integrated vegetation indices, "
        "accumulated agro-climatic indices, and static soil attributes:"
    )
    add_callout(
        doc,
        "Y_i = f( ∫_{t_0}^{T} NDVI_i(t) dt, GDD_i(T), CWD_i(T), SOC_i, pH_i ) + ε_i\n\n"
        "Where:\n"
        "• GDD_i(T) = ∑_{t=t_0}^{T} max( (T_max(t) + T_min(t))/2 - T_base, 0 ) [Growing Degree Days]\n"
        "• CWD_i(T) = ∑_{t=t_0}^{T} (ET_0(t) - P(t)) [Crop Water Deficit: Reference Evapotranspiration minus Precipitation]\n"
        "• SOC_i, pH_i = Baseline Soil Organic Carbon and soil acidity from SoilGrids\n"
        "• f(·) is approximated via Gradient Boosted Decision Trees (LightGBM) with Bayesian Hyperparameter Tuning.",
        bold_prefix="Predictive Formulation:"
    )

    doc.add_heading("2. Commodity Price Volatility & Forecast Model", level=3)
    doc.add_paragraph(
        "Wholesale spot prices P_t are modeled using a hybrid Autoregressive Integrated Moving Average with Exogenous Regressors "
        "(SARIMAX(p,d,q)(P,D,Q)_s) and Long Short-Term Memory (LSTM) residual network:"
    )
    add_callout(
        doc,
        "Φ_P(B^s) ϕ_p(B) (1 - B)^d (1 - B^s)^D P_t = Θ_Q(B^s) θ_q(B) ε_t + ∑_{k=1}^K β_k X_{k, t-L}\n\n"
        "Where X_{k, t-L} represents lagged exogenous drivers including:\n"
        "• Global crude oil futures (representing input fertilizer & transport costs)\n"
        "• Oceanic Niño Index (ONI / ENSO phase indicator)\n"
        "• Projected national stock-to-use ratios from USDA WASDE reports.",
        bold_prefix="Price Time-Series Formulation:"
    )

    # =========================================================================
    # SECTION 7: DATA GOVERNANCE, QUALITY & ETHICAL CONSIDERATIONS
    # =========================================================================
    doc.add_heading("7. Data Governance, Quality Assurance & Ethics", level=1)

    doc.add_paragraph(
        "Deploying data science models in agriculture carries severe real-world consequences: inaccurate drought forecasts "
        "can bankrupt farmers, while flawed price predictions can disrupt national food reserves. Therefore, data governance "
        "and ethical integrity must be engineered into the system from inception."
    )

    add_bullet_point(doc, "Geospatial Alignment & Pixel Cloud-Masking Integrity:", "Optical satellite imagery frequently suffers from cloud contamination, atmospheric aerosol scattering, and shadow occlusion. All automated pipelines must incorporate strict cloud-masking protocols (e.g., utilizing Sentinel-2 Scene Classification Layer - SCL) and reconstruct missing values using temporal spline interpolation or synthetic aperture radar (SAR Sentinel-1) backscatter cross-calibration.")
    add_bullet_point(doc, "Algorithmic Bias & Smallholder Inclusion:", "Machine learning models trained predominantly on industrial farm datasets (e.g., Iowa, USA or Mato Grosso, Brazil) fail catastrophically when applied to fragmented smallholder polycultures in Sub-Saharan Africa or South Asia. Models must be evaluated for regional performance equity, incorporating localized transfer learning and stratified cross-validation.")
    add_bullet_point(doc, "Farmer Data Sovereignty & Commercial Confidentiality:", "Farm boundary polygons, yield monitor records, and soil health assays constitute sensitive intellectual and financial property. Data science platforms must ensure anonymized spatial aggregation, preventing predatory land speculation or exploitative pricing by agricultural input monopolies.")
    add_bullet_point(doc, "Model Explainability in Agronomic Advisory:", "Black-box neural networks providing automated fertilizer prescriptions without interpretable agronomic rationale risk rejection by agronomists. Implement SHAP (SHapley Additive exPlanations) and TreeSHAP to provide transparent feature contribution breakdowns (e.g., 'Nitrogen recommendation lowered due to low moisture availability in topsoil').")

    # =========================================================================
    # SECTION 8: STRATEGIC ROADMAP FOR SUBSEQUENT INTERNSHIP WEEKS
    # =========================================================================
    doc.add_heading("8. Strategic Roadmap for Subsequent Technical Tasks", level=1)

    doc.add_paragraph(
        "With the agribusiness market landscape analyzed and the conceptual framework established, the remaining technical weeks "
        "of the virtual internship are structured systematically to transition from raw data acquisition to deployed predictive intelligence:"
    )

    road_tbl = doc.add_table(rows=5, cols=4)
    r_widths = [Inches(1.2), Inches(1.8), Inches(2.2), Inches(1.3)]
    r_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    road_tbl.rows[0].cells[0].paragraphs[0].text = "Internship Phase"
    road_tbl.rows[0].cells[1].paragraphs[0].text = "Core Technical Milestone"
    road_tbl.rows[0].cells[2].paragraphs[0].text = "Key Methodologies & Tools"
    road_tbl.rows[0].cells[3].paragraphs[0].text = "Target Deliverable"

    roadmap_data = [
        ("Week 2: Data Acquisition & EDA", 
         "Ingest public crop yield, satellite NDVI, and meteorological datasets; conduct rigorous exploratory data analysis.",
         "Pandas, GeoPandas, Xarray, Copernicus Open Access Hub, Seaborn, Matplotlib.",
         "Jupyter Notebook + EDA Summary Report with correlation matrices."),
        ("Week 3: Feature Engineering & Preprocessing", 
         "Compute time-series rolling anomalies, vegetation indices, Growing Degree Days, and lag variables; handle spatial autocorrelation.",
         "Scikit-learn, Rasterio, Feast Feature Store, Spatial Lag Models (PySAL).",
         "Processed analytical feature store & engineered tabular dataset."),
        ("Week 4: Model Development & Validation", 
         "Train and benchmark baseline vs. advanced models for crop yield prediction and price forecasting; optimize hyper-parameters.",
         "LightGBM, XGBoost, PyTorch (LSTM), Optuna hyperparameter optimization.",
         "Model Evaluation Matrix (RMSE, R², MAPE, MAE) + Cross-Validation curves."),
        ("Week 5: Deployment & Decision Support", 
         "Containerize the best-performing model into an interactive inference API and executive dashboard.",
         "FastAPI, Docker, Streamlit / Plotly Dash, RESTful JSON schema.",
         "Interactive Agribusiness Advisory Dashboard & Technical Documentation.")
    ]

    for idx, (ph, m, tools, deliv) in enumerate(roadmap_data, start=1):
        r = road_tbl.rows[idx]
        r.cells[0].paragraphs[0].text = ph
        r.cells[1].paragraphs[0].text = m
        r.cells[2].paragraphs[0].text = tools
        r.cells[3].paragraphs[0].text = deliv

    format_table(road_tbl, r_widths, r_aligns)

    # =========================================================================
    # SECTION 9: CONCLUSION & ACTIONABLE INSIGHTS
    # =========================================================================
    doc.add_heading("9. Conclusion & Actionable Insights", level=1)

    doc.add_paragraph(
        "Agribusiness stands at the nexus of the 21st century's most defining global challenges: feeding a growing human "
        "population while reversing environmental degradation and adapting to a volatile climate. As demonstrated in this "
        "market analysis, solving these challenges cannot rely on incremental manual adjustments or outdated empirical heuristics. "
        "The path forward requires rigorous, scalable data science architectures capable of synthesizing high-frequency geospatial "
        "telemetry, atmospheric reanalysis, and market signals into actionable intelligence."
    )

    doc.add_paragraph(
        "By establishing clear market segmentations, decoding stakeholder pain points across the value chain, standardizing "
        "a 4-tier KPI taxonomy, and laying out an end-to-end conceptual data science framework, this Week 1 foundation "
        "transforms agribusiness from an ambiguous macro domain into a structured, highly tractable analytical problem space. "
        "The data points, schemas, and mathematical formulations established herein will serve as the exact technical blueprint "
        "for the data ingestion, feature engineering, and predictive modeling tasks in the upcoming phases of this project."
    )

    # =========================================================================
    # SECTION 10: ACADEMIC & INDUSTRY REFERENCES
    # =========================================================================
    doc.add_heading("10. Academic, Government & Industry References", level=1)

    references = [
        ("Food and Agriculture Organization (FAO)", "The State of Food and Agriculture 2023: Revealing the true cost of food to transform agrifood systems. Rome: FAO Publications. https://doi.org/10.4060/cc7724en"),
        ("United States Department of Agriculture (USDA) ERS", "Agricultural Productivity in the U.S. / Global Agricultural Productivity Report (GAPS). Economic Research Service, USDA."),
        ("European Space Agency (ESA)", "Sentinel-2 User Handbook: High-Resolution Optical Earth Observation Mission for Land Monitoring. Document Ref: GMES-S2-EOPG-TN-13-0001."),
        ("World Bank Group", "What's Cooking: Digital Transformation of the Agrifood System. Agriculture and Food Series. Washington, DC: World Bank. License: CC BY 3.0 IGO."),
        ("Lobell, D. B., et al.", "The critical role of extreme heat for maize production in the United States. Nature Climate Change, 3(5), 497-501. https://doi.org/10.1038/nclimate1832"),
        ("Basso, B., & Antle, J.", "Digital agriculture to design sustainable agricultural systems. Nature Sustainability, 3(4), 254-262. https://doi.org/10.1038/s41893-020-0510-0"),
        ("McKinsey & Company", "Agtech: Breaking our way out of the agricultural productivity plateau. McKinsey Center for Agricultural Transformation, Agriculture Practice Report."),
        ("Copernicus Climate Change Service (C3S)", "ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate. Copernicus Climate Change Service Climate Data Store (CDS).")
    ]

    for author, citation in references:
        p_ref = doc.add_paragraph(style='Normal')
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        r_auth = p_ref.add_run(author + " ")
        r_auth.font.bold = True
        r_auth.font.color.rgb = COLOR_PRIMARY
        r_cit = p_ref.add_run(citation)
        r_cit.font.color.rgb = COLOR_DARK_TEXT
        r_cit.font.size = Pt(9.5)

    # Save document
    doc.save(output_path)
    print(f"Report successfully built and saved to: {output_path}")

if __name__ == "__main__":
    target_path = r"c:\Agridatascience project\Agribusiness_Market_Analysis_and_Planning_Report.docx"
    build_full_report(target_path)
