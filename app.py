
import streamlit as st

# ============================================================
# Standardization Pathfinder
# Single-file Streamlit application
# ============================================================

st.set_page_config(
    page_title="Standardization Pathfinder",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f7f9fb;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .pathfinder-header {
            background: white;
            border: 1px solid #e5e9ef;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1.2rem;
        }

        .pathfinder-header h1 {
            margin: 0;
            font-size: 2rem;
            color: #1f2937;
        }

        .pathfinder-header p {
            margin: 0.4rem 0 0 0;
            color: #5f6b7a;
        }

        .section-card {
            background: white;
            border: 1px solid #e5e9ef;
            border-radius: 14px;
            padding: 1.35rem 1.5rem;
            margin-bottom: 1rem;
        }

        .recommendation-card {
            background: white;
            border: 1px solid #dfe5ec;
            border-left: 5px solid #526d82;
            border-radius: 12px;
            padding: 1.1rem 1.25rem;
            margin-bottom: 0.9rem;
        }

        .recommendation-card h3 {
            margin-top: 0;
        }

        .review-label {
            font-weight: 600;
            color: #334155;
        }

        .review-value {
            margin-bottom: 0.8rem;
            color: #111827;
            white-space: pre-wrap;
        }

        div[data-testid="stProgress"] > div > div > div > div {
            background-color: #526d82;
        }

        .small-note {
            color: #667085;
            font-size: 0.92rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Constants
# -----------------------------
PAGES = [
    "Welcome",
    "Problem Definition",
    "Current State Assessment",
    "Standardization Needs",
    "Implementation Context",
    "Review",
    "Recommendations",
]

ROOT_CAUSE_CATEGORIES = [
    "Lack of clarity",
    "Knowledge gap",
    "Process not defined",
    "Process not followed",
    "Missing ownership",
    "Unclear roles or responsibilities",
    "Unclear decision authority",
    "Information not captured",
    "Information captured too late",
    "Information difficult to find",
    "Information scattered across locations",
    "Information not current",
    "Duplicate effort",
    "Manual data transfer",
    "Repetitive calculations",
    "Repetitive administrative work",
    "High complexity",
    "Too many handoffs",
    "Lack of standard inputs",
    "Lack of standard outputs",
    "Inconsistent terminology",
    "Inconsistent file structure or naming",
    "Insufficient QA/QC",
    "Late QA/QC",
    "No feedback loop",
    "System limitations",
    "Systems do not integrate",
]

STANDARDIZATION_OBJECTIVES = [
    "Create a consistent process",
    "Reduce manual effort",
    "Improve data quality",
    "Improve QA/QC",
    "Make information easier to find",
    "Improve role clarity",
    "Improve decision consistency",
    "Reduce training burden",
    "Reduce duplicate work",
    "Standardize inputs",
    "Standardize outputs",
    "Improve handoffs",
    "Automate calculations",
    "Automate repetitive administrative work",
    "Improve traceability",
]

FREQUENCY_OPTIONS = [
    "Daily",
    "Weekly",
    "Monthly",
    "Quarterly",
    "A few times per year",
    "Ad hoc but recurring",
]

USER_COUNT_OPTIONS = [
    "1 person",
    "2–5 people",
    "6–20 people",
    "21–50 people",
    "More than 50 people",
]

VARIABILITY_OPTIONS = [
    "Low — the same process is followed almost every time",
    "Moderate — there are a few common variations",
    "High — the process varies substantially by project or situation",
]

DATA_VOLUME_OPTIONS = [
    "Low — small amounts of information",
    "Moderate — multiple files, records, or calculations",
    "High — large datasets or frequent repeated processing",
]

CHANGE_OPTIONS = [
    "Rarely",
    "Occasionally",
    "Frequently",
]

SYSTEM_DEPENDENCY_OPTIONS = [
    "Low — mostly documents or manual work",
    "Moderate — relies on common tools such as Excel, SharePoint, Teams, or email",
    "High — relies on multiple systems, integrations, or specialized software",
]

# -----------------------------
# Session state initialization
# -----------------------------
DEFAULTS = {
    "page": 0,
    "started": False,
    "problem_title": "",
    "pain_point": "",
    "why_matter": "",
    "current_workflow": "",
    "existing_tools": "",
    "root_cause_category": [],
    "root_cause_details": "",
    "objectives": [],
    "desired_outcome": "",
    "standard_inputs_needed": False,
    "standard_outputs_needed": False,
    "repeatable_decisions": False,
    "calculation_heavy": False,
    "structured_data": False,
    "document_heavy": False,
    "frequency": "Monthly",
    "user_count": "2–5 people",
    "variability": "Moderate — there are a few common variations",
    "data_volume": "Moderate — multiple files, records, or calculations",
    "change_frequency": "Occasionally",
    "system_dependency": "Moderate — relies on common tools such as Excel, SharePoint, Teams, or email",
    "needs_auditability": False,
    "needs_offline_use": False,
    "needs_nontechnical_users": True,
    "recommendations_generated": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------
# Navigation helpers
# -----------------------------
def go_to(page_index: int):
    st.session_state.page = max(0, min(page_index, len(PAGES) - 1))
    st.rerun()


def next_page():
    go_to(st.session_state.page + 1)


def previous_page():
    go_to(st.session_state.page - 1)


def render_header():
    current = st.session_state.page
    completed = max(0, current)
    denominator = len(PAGES) - 1
    progress = min(completed / denominator, 1.0)

    st.markdown(
        """
        <div class="pathfinder-header">
            <h1>Standardization Pathfinder</h1>
            <p>Guided decision support for choosing the right standardization approach.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if current > 0:
        st.progress(progress)
        st.caption(f"Step {current} of {denominator}: {PAGES[current]}")


def navigation_buttons(show_previous=True, next_label="Next", next_disabled=False):
    left, spacer, right = st.columns([1, 5, 1])
    with left:
        if show_previous and st.button("Previous", use_container_width=True):
            previous_page()
    with right:
        if st.button(next_label, use_container_width=True, type="primary", disabled=next_disabled):
            next_page()


# -----------------------------
# Recommendation engine
# -----------------------------
def score_recommendations():
    scores = {
        "Standard Operating Procedure (SOP)": 0,
        "Checklist or Job Aid": 0,
        "Standard Template": 0,
        "Excel Calculation Tool": 0,
        "Automated Script": 0,
        "Internal App": 0,
        "Shared Knowledge Resource": 0,
        "Process / Role Redesign": 0,
    }

    reasons = {key: [] for key in scores}

    roots = set(st.session_state.root_cause_category)
    objectives = set(st.session_state.objectives)

    # SOP
    if roots & {
        "Process not defined",
        "Process not followed",
        "Lack of clarity",
        "Too many handoffs",
        "Inconsistent terminology",
    }:
        scores["Standard Operating Procedure (SOP)"] += 4
        reasons["Standard Operating Procedure (SOP)"].append(
            "The problem involves process definition, consistency, or clarity."
        )
    if "Create a consistent process" in objectives:
        scores["Standard Operating Procedure (SOP)"] += 3
    if st.session_state.variability.startswith("Low"):
        scores["Standard Operating Procedure (SOP)"] += 2

    # Checklist / job aid
    if roots & {
        "Process not followed",
        "Insufficient QA/QC",
        "Late QA/QC",
        "Knowledge gap",
    }:
        scores["Checklist or Job Aid"] += 4
        reasons["Checklist or Job Aid"].append(
            "A lightweight control could improve consistency, QA/QC, or execution."
        )
    if st.session_state.variability.startswith("Moderate"):
        scores["Checklist or Job Aid"] += 1

    # Standard template
    if roots & {
        "Lack of standard inputs",
        "Lack of standard outputs",
        "Inconsistent file structure or naming",
        "Information not captured",
        "Inconsistent terminology",
    }:
        scores["Standard Template"] += 5
        reasons["Standard Template"].append(
            "The issue involves inconsistent inputs, outputs, structure, or captured information."
        )
    if st.session_state.standard_inputs_needed:
        scores["Standard Template"] += 3
    if st.session_state.standard_outputs_needed:
        scores["Standard Template"] += 3

    # Excel tool
    if roots & {
        "Repetitive calculations",
        "Manual data transfer",
        "Duplicate effort",
    }:
        scores["Excel Calculation Tool"] += 4
        reasons["Excel Calculation Tool"].append(
            "The work contains repeatable calculations or manual data handling."
        )
    if st.session_state.calculation_heavy:
        scores["Excel Calculation Tool"] += 5
    if st.session_state.structured_data:
        scores["Excel Calculation Tool"] += 2
    if st.session_state.user_count in {"1 person", "2–5 people", "6–20 people"}:
        scores["Excel Calculation Tool"] += 1
    if st.session_state.system_dependency.startswith("Low") or st.session_state.system_dependency.startswith("Moderate"):
        scores["Excel Calculation Tool"] += 1

    # Script
    if roots & {
        "Manual data transfer",
        "Repetitive calculations",
        "Repetitive administrative work",
        "Duplicate effort",
        "System limitations",
        "Systems do not integrate",
    }:
        scores["Automated Script"] += 4
        reasons["Automated Script"].append(
            "Automation may remove repeated processing, transfer, or administrative effort."
        )
    if st.session_state.data_volume.startswith("High"):
        scores["Automated Script"] += 3
    if st.session_state.frequency in {"Daily", "Weekly"}:
        scores["Automated Script"] += 2
    if st.session_state.structured_data:
        scores["Automated Script"] += 2
    if st.session_state.needs_nontechnical_users:
        scores["Automated Script"] -= 1

    # Internal app
    if roots & {
        "High complexity",
        "Information scattered across locations",
        "Information difficult to find",
        "Manual data transfer",
        "Repetitive administrative work",
        "Unclear decision authority",
    }:
        scores["Internal App"] += 4
        reasons["Internal App"].append(
            "The problem spans multiple tasks, decisions, or information sources."
        )
    if st.session_state.repeatable_decisions:
        scores["Internal App"] += 3
    if st.session_state.needs_nontechnical_users:
        scores["Internal App"] += 2
    if st.session_state.user_count in {"21–50 people", "More than 50 people"}:
        scores["Internal App"] += 2
    if st.session_state.variability.startswith("Moderate"):
        scores["Internal App"] += 1

    # Shared knowledge resource
    if roots & {
        "Knowledge gap",
        "Information difficult to find",
        "Information scattered across locations",
        "Information not current",
        "Lack of clarity",
    }:
        scores["Shared Knowledge Resource"] += 5
        reasons["Shared Knowledge Resource"].append(
            "The issue is primarily about finding, maintaining, or understanding information."
        )
    if st.session_state.document_heavy:
        scores["Shared Knowledge Resource"] += 2
    if "Make information easier to find" in objectives:
        scores["Shared Knowledge Resource"] += 3

    # Process / role redesign
    if roots & {
        "Missing ownership",
        "Unclear roles or responsibilities",
        "Unclear decision authority",
        "Too many handoffs",
        "No feedback loop",
    }:
        scores["Process / Role Redesign"] += 6
        reasons["Process / Role Redesign"].append(
            "The main issue appears structural rather than purely document- or tool-based."
        )
    if "Improve role clarity" in objectives:
        scores["Process / Role Redesign"] += 3
    if "Improve handoffs" in objectives:
        scores["Process / Role Redesign"] += 2

    # Cross-cutting refinements
    if st.session_state.change_frequency == "Frequently":
        scores["Standard Operating Procedure (SOP)"] -= 1
        scores["Standard Template"] -= 1
        scores["Internal App"] += 1
        scores["Shared Knowledge Resource"] += 1

    if st.session_state.needs_auditability:
        scores["Standard Operating Procedure (SOP)"] += 1
        scores["Checklist or Job Aid"] += 1
        scores["Standard Template"] += 1
        scores["Excel Calculation Tool"] += 1
        scores["Internal App"] += 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked, reasons


def recommendation_description(name):
    descriptions = {
        "Standard Operating Procedure (SOP)":
            "Use when the primary need is a defined, repeatable process with clear instructions, roles, controls, and decision points.",
        "Checklist or Job Aid":
            "Use when the process already exists but users need a concise execution aid, quality-control check, or reminder.",
        "Standard Template":
            "Use when consistency is needed in the information collected, file structure, terminology, inputs, or outputs.",
        "Excel Calculation Tool":
            "Use when the work is structured, calculation-heavy, and benefits from transparent formulas, controlled inputs, and standardized outputs.",
        "Automated Script":
            "Use when repeated data processing, file handling, calculations, or transfers can be reliably automated with limited user interaction.",
        "Internal App":
            "Use when users need a guided interface that combines inputs, logic, calculations, decision support, and standardized outputs.",
        "Shared Knowledge Resource":
            "Use when the main problem is fragmented, hard-to-find, unclear, or outdated guidance and reference information.",
        "Process / Role Redesign":
            "Use when the root problem is ownership, decision authority, handoffs, responsibilities, or process structure rather than the absence of a tool.",
    }
    return descriptions[name]


# -----------------------------
# Page rendering
# -----------------------------
render_header()

page = st.session_state.page

# PAGE 1: Welcome
if page == 0:
    st.markdown(
        """
        <div class="section-card">
            <h2>Welcome</h2>
            <p>
                Standardization Pathfinder helps employees determine the most appropriate
                standardization approach for a recurring operational problem.
            </p>
            <p>
                The assessment guides you through the problem, current state, standardization
                needs, and implementation context. It then compares several solution types,
                including procedures, templates, calculation tools, scripts, internal apps,
                and process changes.
            </p>
            <p>
                The goal is not to force every problem into the same solution. It is to identify
                the smallest practical standardization approach that addresses the actual root cause.
            </p>
            <p class="small-note">
                Responses are stored only in your current Streamlit session. This application does
                not use a database, authentication, approvals, workflow management, or draft storage.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([2, 2, 2])
    with center:
        if st.button("Begin Assessment", use_container_width=True, type="primary"):
            st.session_state.started = True
            go_to(1)

# PAGE 2: Problem Definition
elif page == 1:
    st.markdown('<div class="section-card"><h2>Problem Definition</h2>', unsafe_allow_html=True)

    st.text_input(
        "Problem Title",
        key="problem_title",
        placeholder="Example: Repeated manual preparation of project calculation workbooks",
    )

    st.text_area(
        "Pain Point",
        key="pain_point",
        height=140,
        placeholder="Describe the recurring problem, inefficiency, inconsistency, or source of frustration.",
    )

    st.text_area(
        "Why Does It Matter",
        key="why_matter",
        height=140,
        placeholder="Describe the impact on time, quality, risk, consistency, cost, or employee experience.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    required_complete = all(
        [
            st.session_state.problem_title.strip(),
            st.session_state.pain_point.strip(),
            st.session_state.why_matter.strip(),
        ]
    )
    if not required_complete:
        st.caption("Complete all three fields to continue.")

    navigation_buttons(next_disabled=not required_complete)

# PAGE 3: Current State Assessment
elif page == 2:
    st.markdown('<div class="section-card"><h2>Current State Assessment</h2>', unsafe_allow_html=True)

    st.text_area(
        "Current Workflow",
        key="current_workflow",
        height=160,
        placeholder="Describe how the work is currently completed from start to finish.",
    )

    st.text_area(
        "Existing Tools and Controls",
        key="existing_tools",
        height=130,
        placeholder="List current templates, spreadsheets, scripts, SOPs, systems, reviews, QA/QC checks, or other controls.",
    )

    st.multiselect(
        "Root Cause Category",
        options=ROOT_CAUSE_CATEGORIES,
        key="root_cause_category",
        help="Select all categories that materially contribute to the problem.",
    )

    st.text_area(
        "Root Cause Details",
        key="root_cause_details",
        height=140,
        placeholder="Explain the underlying cause in more detail.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    required_complete = all(
        [
            st.session_state.current_workflow.strip(),
            len(st.session_state.root_cause_category) > 0,
            st.session_state.root_cause_details.strip(),
        ]
    )
    if not required_complete:
        st.caption("Complete the Current Workflow, select at least one Root Cause Category, and add Root Cause Details.")

    navigation_buttons(next_disabled=not required_complete)

# PAGE 4: Standardization Needs
elif page == 3:
    st.markdown('<div class="section-card"><h2>Standardization Needs</h2>', unsafe_allow_html=True)

    st.multiselect(
        "What should standardization improve?",
        options=STANDARDIZATION_OBJECTIVES,
        key="objectives",
    )

    st.text_area(
        "Desired Outcome",
        key="desired_outcome",
        height=130,
        placeholder="Describe what a successful future state would look like.",
    )

    st.markdown("#### Work characteristics")

    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("Standard inputs are needed", key="standard_inputs_needed")
        st.checkbox("The work includes repeatable calculations", key="calculation_heavy")
        st.checkbox("The work primarily uses structured data", key="structured_data")

    with c2:
        st.checkbox("Standard outputs are needed", key="standard_outputs_needed")
        st.checkbox("The work includes repeatable decisions or branching logic", key="repeatable_decisions")
        st.checkbox("The work is primarily document- or guidance-heavy", key="document_heavy")

    st.markdown("</div>", unsafe_allow_html=True)

    required_complete = len(st.session_state.objectives) > 0 and st.session_state.desired_outcome.strip()
    if not required_complete:
        st.caption("Select at least one objective and describe the desired outcome.")

    navigation_buttons(next_disabled=not required_complete)

# PAGE 5: Implementation Context
elif page == 4:
    st.markdown('<div class="section-card"><h2>Implementation Context</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox("How often does the work occur?", FREQUENCY_OPTIONS, key="frequency")
        st.selectbox("How many people typically perform or use the process?", USER_COUNT_OPTIONS, key="user_count")
        st.selectbox("How variable is the process?", VARIABILITY_OPTIONS, key="variability")

    with col2:
        st.selectbox("How much data or information is handled?", DATA_VOLUME_OPTIONS, key="data_volume")
        st.selectbox("How often do the requirements or process change?", CHANGE_OPTIONS, key="change_frequency")
        st.selectbox("How dependent is the process on software systems?", SYSTEM_DEPENDENCY_OPTIONS, key="system_dependency")

    st.markdown("#### Additional requirements")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.checkbox("Strong auditability or traceability is important", key="needs_auditability")
    with c2:
        st.checkbox("The solution may need to work offline", key="needs_offline_use")
    with c3:
        st.checkbox("The primary users are nontechnical", key="needs_nontechnical_users")

    st.markdown("</div>", unsafe_allow_html=True)

    navigation_buttons()

# PAGE 6: Review
elif page == 5:
    st.markdown('<div class="section-card"><h2>Review Your Answers</h2>', unsafe_allow_html=True)

    review_sections = [
        (
            "Problem Definition",
            [
                ("Problem Title", st.session_state.problem_title),
                ("Pain Point", st.session_state.pain_point),
                ("Why Does It Matter", st.session_state.why_matter),
            ],
        ),
        (
            "Current State",
            [
                ("Current Workflow", st.session_state.current_workflow),
                ("Existing Tools and Controls", st.session_state.existing_tools or "Not provided"),
                ("Root Cause Categories", ", ".join(st.session_state.root_cause_category)),
                ("Root Cause Details", st.session_state.root_cause_details),
            ],
        ),
        (
            "Standardization Needs",
            [
                ("Objectives", ", ".join(st.session_state.objectives)),
                ("Desired Outcome", st.session_state.desired_outcome),
                ("Standard Inputs Needed", "Yes" if st.session_state.standard_inputs_needed else "No"),
                ("Standard Outputs Needed", "Yes" if st.session_state.standard_outputs_needed else "No"),
                ("Repeatable Decisions", "Yes" if st.session_state.repeatable_decisions else "No"),
                ("Calculation Heavy", "Yes" if st.session_state.calculation_heavy else "No"),
                ("Structured Data", "Yes" if st.session_state.structured_data else "No"),
                ("Document / Guidance Heavy", "Yes" if st.session_state.document_heavy else "No"),
            ],
        ),
        (
            "Implementation Context",
            [
                ("Frequency", st.session_state.frequency),
                ("Users", st.session_state.user_count),
                ("Process Variability", st.session_state.variability),
                ("Data Volume", st.session_state.data_volume),
                ("Change Frequency", st.session_state.change_frequency),
                ("System Dependency", st.session_state.system_dependency),
                ("Auditability Important", "Yes" if st.session_state.needs_auditability else "No"),
                ("Offline Use Needed", "Yes" if st.session_state.needs_offline_use else "No"),
                ("Primary Users Nontechnical", "Yes" if st.session_state.needs_nontechnical_users else "No"),
            ],
        ),
    ]

    for heading, items in review_sections:
        st.subheader(heading)
        for label, value in items:
            st.markdown(f'<div class="review-label">{label}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="review-value">{value}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    left, spacer, right = st.columns([1, 5, 1])
    with left:
        if st.button("Previous", use_container_width=True):
            previous_page()
    with right:
        if st.button("Generate Recommendations", use_container_width=True, type="primary"):
            st.session_state.recommendations_generated = True
            go_to(6)

# PAGE 7: Recommendations
elif page == 6:
    ranked, reasons = score_recommendations()

    st.markdown('<div class="section-card"><h2>Recommended Standardization Approaches</h2>', unsafe_allow_html=True)
    st.write(
        "The results below are based on the root causes, work characteristics, scale, and implementation context you entered."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    top_score = ranked[0][1]
    recommended = [item for item in ranked if item[1] >= max(top_score - 2, 1)]

    st.subheader("Primary recommendations")

    for name, score in recommended[:3]:
        rationale = reasons[name]
        rationale_html = ""
        if rationale:
            rationale_html = "<ul>" + "".join(f"<li>{r}</li>" for r in rationale) + "</ul>"

        st.markdown(
            f"""
            <div class="recommendation-card">
                <h3>{name}</h3>
                <p>{recommendation_description(name)}</p>
                {rationale_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("How to interpret the result")
    st.markdown(
        """
        The strongest solution is not always a single artifact. Many recurring operational
        problems are best addressed with a small combination, such as:

        - an SOP plus a checklist,
        - a standard template plus an Excel calculation tool,
        - a process redesign plus a shared knowledge resource, or
        - an internal app supported by clear standard operating guidance.

        Prefer the simplest solution that directly addresses the root cause. More automation
        is useful only when the underlying process and decision logic are sufficiently stable
        to automate.
        """
    )

    st.subheader("Full fit comparison")
    max_possible_display = max(score for _, score in ranked) if ranked else 1
    for name, score in ranked:
        normalized = int(max(0, score) / max(max_possible_display, 1) * 100)
        st.write(f"**{name}**")
        st.progress(normalized)
        st.caption(recommendation_description(name))

    st.divider()

    left, middle, right = st.columns([1.4, 4.2, 1.8])

    with left:
        if st.button("Previous", use_container_width=True):
            previous_page()

    with right:
        if st.button("Start New Assessment", use_container_width=True):
            for key, value in DEFAULTS.items():
                st.session_state[key] = value
            st.rerun()
