
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
from datetime import datetime

# ============================================================
# TERA 2.0 — MIDNIGHT INTELLIGENCE EDITION
# Environmental Risk Analysis | Educational Prototype
# ============================================================

st.set_page_config(
    page_title="TERA 2.0 | Midnight Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- THEME --------------------

BG = "#070B14"
PANEL = "#0B1220"
HEADER = "#111C33"
BORDER = "#263B5A"
CYAN = "#00D9FF"
BLUE = "#448AFF"
PURPLE = "#A78BFA"
TEXT = "#F1F5FF"
MUTED = "#9DB0CE"
GREEN = "#38D996"
YELLOW = "#FFD166"
RED = "#FF5C75"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    [data-testid="stSidebar"] {{
        background: #090F1C;
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stHeader"] {{
        background: rgba(7, 11, 20, 0.95);
    }}

    h1, h2, h3 {{
        color: {TEXT} !important;
    }}

    p, label, li {{
        color: {TEXT};
    }}

    [data-testid="stMetric"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 16px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {CYAN} !important;
    }}

    div[data-testid="stTabs"] button {{
        color: {MUTED};
        font-weight: 600;
    }}

    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: {CYAN} !important;
        border-bottom-color: {CYAN} !important;
    }}

    div.stButton > button {{
        background: linear-gradient(90deg, #12345A, #155E75);
        color: white;
        border: 1px solid {CYAN};
        border-radius: 9px;
        font-weight: 600;
    }}

    div.stButton > button:hover {{
        background: #164E63;
        color: white;
        border-color: white;
    }}

    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    [data-testid="stDataFrame"] [data-testid="glideDataEditor"] {{
        --gdg-bg-cell: {PANEL};
        --gdg-bg-cell-medium: {HEADER};
        --gdg-bg-header: {HEADER};
        --gdg-text-dark: {TEXT};
        --gdg-text-medium: {MUTED};
        --gdg-text-light: {MUTED};
        --gdg-border-color: {BORDER};
        --gdg-accent-color: {CYAN};
    }}

    [data-testid="stTable"] table {{
        background: {PANEL} !important;
        color: {TEXT} !important;
        border-collapse: collapse !important;
    }}

    [data-testid="stTable"] thead th {{
        background: {HEADER} !important;
        color: {CYAN} !important;
        border-bottom: 1px solid {BORDER} !important;
    }}

    [data-testid="stTable"] tbody td {{
        background: {PANEL} !important;
        color: {TEXT} !important;
        border-bottom: 1px solid {BORDER} !important;
    }}

    .hero {{
        padding: 26px;
        border-radius: 18px;
        border: 1px solid #155E75;
        background: linear-gradient(120deg, #0B1220 0%, #10243D 60%, #10102A 100%);
        margin-bottom: 18px;
    }}

    .hero-label {{
        color: {CYAN};
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 800;
    }}

    .hero-title {{
        color: {TEXT};
        font-size: clamp(28px, 4vw, 44px);
        font-weight: 900;
        line-height: 1.1;
        margin: 8px 0;
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 15px;
    }}

    .small-note {{
        color: {MUTED};
        font-size: 12px;
    }}

    .status-chip {{
        display: inline-block;
        color: {CYAN};
        border: 1px solid #155E75;
        background: #0A2533;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 700;
    }}

    div[data-testid="stAlert"] {{
        background: #111C33;
        border: 1px solid {BORDER};
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- DATA AND MODEL --------------------

FACTORS = [
    "Hazard",
    "Vulnerability",
    "Population",
    "Exposure",
    "Urgency",
]

WEIGHTS = {
    "Hazard": 0.30,
    "Vulnerability": 0.25,
    "Population": 0.20,
    "Exposure": 0.15,
    "Urgency": 0.10,
}

ZONES = {
    "Forest": [72, 65, 35, 95, 75],
    "Residential Area": [80, 85, 95, 45, 90],
    "Hospital": [75, 90, 90, 30, 95],
    "Smart Farm": [60, 65, 45, 75, 60],
    "River & Dam": [85, 75, 70, 85, 85],
    "Industrial Zone": [82, 70, 75, 65, 80],
}


def calculate_risk(scores):
    """Calculate a weighted priority index from 0 to 100."""
    return round(
        sum(scores[factor] * WEIGHTS[factor] for factor in FACTORS),
        1,
    )


def classify_risk(score):
    if score >= 80:
        return "CRITICAL"
    if score >= 65:
        return "HIGH"
    if score >= 45:
        return "MODERATE"
    return "LOWER"


def risk_color(level):
    colors = {
        "CRITICAL": RED,
        "HIGH": "#FF9F43",
        "MODERATE": YELLOW,
        "LOWER": GREEN,
    }
    return colors.get(level, CYAN)


def make_zone_dataframe():
    rows = []

    for zone, values in ZONES.items():
        scores = dict(zip(FACTORS, values))
        risk = calculate_risk(scores)

        row = {
            "Zone": zone,
            **scores,
            "Risk Index": risk,
            "Priority": classify_risk(risk),
        }
        rows.append(row)

    return (
        pd.DataFrame(rows)
        .sort_values("Risk Index", ascending=False)
        .reset_index(drop=True)
    )


def style_table(df):
    """Apply a dark navy style to pandas-rendered tables."""
    styler = (
        df.style
        .set_properties(
            **{
                "background-color": PANEL,
                "color": TEXT,
                "border-color": BORDER,
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", HEADER),
                        ("color", CYAN),
                        ("border-color", BORDER),
                        ("font-weight", "bold"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("background-color", PANEL),
                        ("color", TEXT),
                        ("border-color", BORDER),
                    ],
                },
                {
                    "selector": "tr:nth-child(even) td",
                    "props": [("background-color", "#101A2D")],
                },
                {
                    "selector": "table",
                    "props": [
                        ("border-collapse", "collapse"),
                        ("border", f"1px solid {BORDER}"),
                    ],
                },
            ]
        )
    )

    if "Priority" in df.columns:
        def priority_style(value):
            color = risk_color(str(value))
            return f"color: {color}; font-weight: bold;"

        styler = styler.map(priority_style, subset=["Priority"])

    return styler


def show_table(df, height=300):
    """Render a consistently dark table."""
    st.dataframe(
        style_table(df),
        use_container_width=True,
        hide_index=True,
        height=height,
    )


def style_plot(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT, family="Arial"),
        margin=dict(l=20, r=20, t=45, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
        ),
        title_font=dict(color=TEXT, size=17),
        xaxis=dict(
            gridcolor="#1C2A42",
            linecolor=BORDER,
            tickfont=dict(color=MUTED),
            title_font=dict(color=MUTED),
        ),
        yaxis=dict(
            gridcolor="#1C2A42",
            linecolor=BORDER,
            tickfont=dict(color=MUTED),
            title_font=dict(color=MUTED),
        ),
    )
    return fig


def make_report(df):
    lines = [
        "TERA 2.0 — MIDNIGHT INTELLIGENCE EDITION",
        "Environmental Risk Analysis Prototype",
        f"Report generated: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        "",
        "IMPORTANT: Scores are illustrative weighted priority indices.",
        "They are not probabilities, validated forecasts, or live sensor readings.",
        "",
        "MODEL FORMULA:",
        "Risk Index = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U",
        "",
        "ZONE RESULTS:",
        df.to_string(index=False),
        "",
        "LIMITATIONS:",
        "- Uses illustrative example scores.",
        "- Does not ingest live sensor, satellite, or weather feeds.",
        "- Does not claim a trained machine-learning model.",
        "- Real-world deployment requires validated data and expert review.",
    ]
    return "\n".join(lines)


# -------------------- HEADER --------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">TERA 2.0 • ENVIRONMENTAL INTELLIGENCE</div>
        <div class="hero-title">MIDNIGHT INTELLIGENCE</div>
        <div class="hero-subtitle">
            Technology for Environmental Risk Analysis
            · THE SIGNATURE EDITION
        </div>
        <br>
        <span class="status-chip">● SYSTEM ONLINE</span>
        &nbsp;
        <span class="status-chip">RULE-BASED PROTOTYPE</span>
    </div>
    """,
    unsafe_allow_html=True,
)

df = make_zone_dataframe()
top_zone = df.iloc[0]
average_risk = round(df["Risk Index"].mean(), 1)
critical_count = int((df["Priority"] == "CRITICAL").sum())
high_or_critical = int(df["Priority"].isin(["HIGH", "CRITICAL"]).sum())

# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("## 🌍 TERA 2.0")
    st.caption("MIDNIGHT INTELLIGENCE")
    st.divider()

    st.markdown("### System overview")
    st.write("**Zones monitored:** 6")
    st.write("**Scoring factors:** 5")
    st.write("**Model:** Weighted risk index")

    st.divider()
    st.markdown("### Risk thresholds")
    st.markdown(f"🔴 **Critical:** 80–100")
    st.markdown(f"🟠 **High:** 65–79.9")
    st.markdown(f"🟡 **Moderate:** 45–64.9")
    st.markdown(f"🟢 **Lower:** Below 45")

    st.divider()
    st.markdown("### Data integrity")
    st.caption(
        "Demonstration values only. This dashboard does not "
        "receive live environmental sensor readings."
    )

# -------------------- NAVIGATION --------------------

(
    tab_command,
    tab_zone,
    tab_compare,
    tab_scenario,
    tab_mission,
    tab_method,
) = st.tabs(
    [
        "⚡ Command Centre",
        "🛰️ Zone Intelligence",
        "📊 Compare Zones",
        "🧪 Scenario Lab",
        "🎯 Mission Control",
        "📘 Methodology",
    ]
)

# ============================================================
# TAB 1 — COMMAND CENTRE
# ============================================================

with tab_command:
    st.subheader("Environmental Command Centre")
    st.caption(
        "A consolidated view of illustrative environmental-risk priorities."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Zones Analysed", len(df))
    c2.metric("Average Risk Index", f"{average_risk}/100")
    c3.metric("Highest-Risk Zone", str(top_zone["Zone"]))
    c4.metric("High / Critical Zones", high_or_critical)

    st.markdown("### Risk priority overview")

    left, right = st.columns([1.4, 1])

    with left:
        bar = px.bar(
            df.sort_values("Risk Index"),
            x="Risk Index",
            y="Zone",
            orientation="h",
            color="Risk Index",
            color_continuous_scale=[
                [0, GREEN],
                [0.45, YELLOW],
                [0.65, "#FF9F43"],
                [1, RED],
            ],
            range_color=[0, 100],
            text="Risk Index",
            title="Zone priority ranking",
        )
        bar.update_traces(textposition="outside", cliponaxis=False)
        bar.update_coloraxes(showscale=False)
        st.plotly_chart(style_plot(bar, 400), use_container_width=True)

    with right:
        counts = (
            df["Priority"]
            .value_counts()
            .reindex(["CRITICAL", "HIGH", "MODERATE", "LOWER"])
            .fillna(0)
            .reset_index()
        )
        counts.columns = ["Priority", "Zones"]

        donut = px.pie(
            counts,
            names="Priority",
            values="Zones",
            hole=0.65,
            title="Priority distribution",
            color="Priority",
            color_discrete_map={
                "CRITICAL": RED,
                "HIGH": "#FF9F43",
                "MODERATE": YELLOW,
                "LOWER": GREEN,
            },
        )
        donut.update_traces(
            textposition="inside",
            textinfo="label+value",
        )
        st.plotly_chart(style_plot(donut, 400), use_container_width=True)

    st.markdown("### Zone assessment table")
    show_table(df, 285)

    st.info(
        "Interpretation: a higher index indicates higher relative priority "
        "within this illustrative model. It does not mean a disaster is "
        "certain or that the score is a percentage probability."
    )

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download zone results (CSV)",
        data=csv_data,
        file_name="tera_zone_results.csv",
        mime="text/csv",
        key="command_csv",
    )

# ============================================================
# TAB 2 — ZONE INTELLIGENCE
# ============================================================

with tab_zone:
    st.subheader("Zone Intelligence")
    st.caption("Inspect a zone's factor profile and weighted contributions.")

    selected_zone = st.selectbox(
        "Select a zone",
        list(ZONES.keys()),
        key="zone_select",
    )

    values = ZONES[selected_zone]
    scores = dict(zip(FACTORS, values))
    score = calculate_risk(scores)
    level = classify_risk(score)

    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Index", f"{score}/100")
    m2.metric("Priority Level", level)
    m3.metric("Largest Factor Score", max(values))

    left, right = st.columns(2)

    with left:
        radar = go.Figure()
        radar.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=FACTORS + [FACTORS[0]],
                fill="toself",
                name=selected_zone,
                line=dict(color=CYAN, width=3),
                fillcolor="rgba(0,217,255,0.18)",
            )
        )
        radar.update_layout(
            polar=dict(
                bgcolor=PANEL,
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor=BORDER,
                    tickfont=dict(color=MUTED),
                ),
                angularaxis=dict(
                    gridcolor=BORDER,
                    tickfont=dict(color=TEXT),
                ),
            ),
            title="Factor profile",
        )
        st.plotly_chart(style_plot(radar, 420), use_container_width=True)

    with right:
        contributions = pd.DataFrame(
            {
                "Factor": FACTORS,
                "Raw Score": values,
                "Weight (%)": [WEIGHTS[f] * 100 for f in FACTORS],
                "Weighted Contribution": [
                    round(scores[f] * WEIGHTS[f], 2) for f in FACTORS
                ],
            }
        )

        contribution_chart = px.bar(
            contributions,
            x="Factor",
            y="Weighted Contribution",
            color="Weighted Contribution",
            color_continuous_scale=["#174A70", CYAN, PURPLE],
            title="Contribution to the total index",
            text="Weighted Contribution",
        )
        contribution_chart.update_traces(textposition="outside")
        contribution_chart.update_coloraxes(showscale=False)
        st.plotly_chart(
            style_plot(contribution_chart, 420),
            use_container_width=True,
        )

    st.markdown("### Factor breakdown")
    show_table(contributions, 260)

    st.markdown("### Suggested review focus")

    if level == "CRITICAL":
        st.warning(
            "Priority review: verify the input assumptions, inspect "
            "the highest-contributing factors, and consider whether "
            "expert assessment is required."
        )
    elif level == "HIGH":
        st.warning(
            "Elevated review priority: check the most influential "
            "factors and identify practical prevention measures."
        )
    elif level == "MODERATE":
        st.info(
            "Moderate review priority: monitor the assumptions and "
            "consider measures that reduce exposure or vulnerability."
        )
    else:
        st.success(
            "Lower relative priority in this demonstration model. "
            "This is not a guarantee of safety."
        )

# ============================================================
# TAB 3 — COMPARE ZONES
# ============================================================

with tab_compare:
    st.subheader("Compare Zones")
    st.caption("Compare factor scores across selected zones.")

    selected_zones = st.multiselect(
        "Choose zones to compare",
        options=list(ZONES.keys()),
        default=["Forest", "Residential Area", "Hospital"],
        key="compare_zones",
    )

    if selected_zones:
        comparison_rows = []

        for zone in selected_zones:
            values = ZONES[zone]
            row = {"Zone": zone}
            row.update(dict(zip(FACTORS, values)))
            row["Risk Index"] = calculate_risk(dict(zip(FACTORS, values)))
            row["Priority"] = classify_risk(row["Risk Index"])
            comparison_rows.append(row)

        comparison_df = pd.DataFrame(comparison_rows)

        compare_chart = px.bar(
            comparison_df.melt(
                id_vars="Zone",
                value_vars=FACTORS,
                var_name="Factor",
                value_name="Score",
            ),
            x="Zone",
            y="Score",
            color="Factor",
            barmode="group",
            title="Factor-by-factor comparison",
            color_discrete_sequence=[CYAN, BLUE, PURPLE, GREEN, YELLOW],
        )
        st.plotly_chart(
            style_plot(compare_chart, 420),
            use_container_width=True,
        )

        st.markdown("### Comparison results")
        show_table(comparison_df, 260)

        radar_compare = go.Figure()

        for zone in selected_zones:
            values = ZONES[zone]
            radar_compare.add_trace(
                go.Scatterpolar(
                    r=values + [values[0]],
                    theta=FACTORS + [FACTORS[0]],
                    name=zone,
                    fill="none",
                )
            )

        radar_compare.update_layout(
            title="Environmental factor profiles",
            polar=dict(
                bgcolor=PANEL,
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor=BORDER,
                    tickfont=dict(color=MUTED),
                ),
                angularaxis=dict(
                    gridcolor=BORDER,
                    tickfont=dict(color=TEXT),
                ),
            ),
        )

        st.plotly_chart(
            style_plot(radar_compare, 440),
            use_container_width=True,
        )
    else:
        st.info("Select at least one zone to display comparisons.")

# ============================================================
# TAB 4 — SCENARIO LAB
# ============================================================

with tab_scenario:
    st.subheader("Scenario Lab")
    st.caption(
        "Change illustrative factor values and observe how the "
        "weighted index responds. This is a scenario demonstration, "
        "not a real-world prediction."
    )

    scenario_zone = st.selectbox(
        "Choose the zone for your scenario",
        list(ZONES.keys()),
        key="scenario_zone",
    )

    base_values = dict(zip(FACTORS, ZONES[scenario_zone]))

    st.markdown("### Adjust the factor assumptions")

    slider_cols = st.columns(2)
    scenario_scores = {}

    for i, factor in enumerate(FACTORS):
        with slider_cols[i % 2]:
            scenario_scores[factor] = st.slider(
                f"{factor} score",
                min_value=0,
                max_value=100,
                value=int(base_values[factor]),
                step=1,
                key=f"slider_{scenario_zone}_{factor}",
                help="Illustrative input from 0 to 100.",
            )

    baseline_score = calculate_risk(base_values)
    scenario_score = calculate_risk(scenario_scores)
    change = round(scenario_score - baseline_score, 1)

    st.markdown("### Scenario outcome")
    s1, s2, s3 = st.columns(3)
    s1.metric("Original Index", f"{baseline_score}/100")
    s2.metric("Scenario Index", f"{scenario_score}/100")
    s3.metric("Change", f"{change:+.1f}", delta=f"{change:+.1f}")

    new_level = classify_risk(scenario_score)
    st.markdown(
        f"**Scenario priority:** "
        f"<span style='color:{risk_color(new_level)};"
        f"font-weight:bold'>{new_level}</span>",
        unsafe_allow_html=True,
    )

    scenario_table = pd.DataFrame(
        [
            {
                "Factor": factor,
                "Original Score": base_values[factor],
                "Scenario Score": scenario_scores[factor],
                "Weight (%)": WEIGHTS[factor] * 100,
                "New Contribution": round(
                    scenario_scores[factor] * WEIGHTS[factor], 2
                ),
            }
            for factor in FACTORS
        ]
    )

    show_table(scenario_table, 260)

    scenario_chart = go.Figure()

    scenario_chart.add_trace(
        go.Bar(
            name="Original",
            x=FACTORS,
            y=[base_values[f] for f in FACTORS],
            marker_color=BLUE,
        )
    )

    scenario_chart.add_trace(
        go.Bar(
            name="Scenario",
            x=FACTORS,
            y=[scenario_scores[f] for f in FACTORS],
            marker_color=CYAN,
        )
    )

    scenario_chart.update_layout(
        title="Original vs scenario factor scores",
        barmode="group",
        yaxis=dict(range=[0, 100]),
    )

    st.plotly_chart(
        style_plot(scenario_chart, 390),
        use_container_width=True,
    )

    st.caption(
        "A change in this index reflects the chosen inputs and fixed "
        "weights. It does not establish that an actual environmental "
        "risk has increased or decreased."
    )

# ============================================================
# TAB 5 — MISSION CONTROL
# ============================================================

with tab_mission:
    st.subheader("Mission Control")
    st.caption(
        "Use this checklist to structure a responsible environmental "
        "risk review. It does not issue real emergency alerts."
    )

    st.markdown("### Assessment checklist")

    checklist_items = [
        "Confirm the source and date of the input data",
        "Check whether scores are supported by evidence",
        "Identify the factors contributing most to the index",
        "Verify the assessment with relevant experts",
        "Identify feasible prevention or preparedness actions",
        "Record assumptions, uncertainty, and limitations",
    ]

    completed = []

    checklist_cols = st.columns(2)

    for i, item in enumerate(checklist_items):
        with checklist_cols[i % 2]:
            checked = st.checkbox(item, key=f"mission_check_{i}")
            completed.append(checked)

    completion = (
        sum(completed) / len(checklist_items) * 100
        if checklist_items
        else 0
    )

    st.progress(int(completion))
    st.write(f"Checklist progress: **{int(completion)}%**")

    st.markdown("### Current illustrative priorities")
    show_table(df[["Zone", "Risk Index", "Priority"]], 260)

    st.markdown("### Generate a briefing")

    briefing = st.text_area(
        "Add notes for your team",
        placeholder=(
            "Example: verify the assumptions for the highest-ranked "
            "zone and identify what data would be needed next."
        ),
        height=120,
    )

    report_text = make_report(df)

    if briefing.strip():
        report_text += "\n\nTEAM NOTES:\n" + briefing.strip()

    report_text += (
        "\n\nCHECKLIST COMPLETION: "
        + str(int(completion))
        + "%\n"
    )

    st.download_button(
        "⬇ Download mission briefing (TXT)",
        data=report_text,
        file_name="tera_mission_briefing.txt",
        mime="text/plain",
        key="mission_report",
    )

    st.warning(
        "TERA is an educational prototype. Do not use this dashboard "
        "as a substitute for official warnings, emergency services, "
        "professional environmental assessment, or validated forecasts."
    )

# ============================================================
# TAB 6 — METHODOLOGY
# ============================================================

with tab_method:
    st.subheader("Methodology & Transparency")
    st.caption("Understand how the index is calculated and what it means.")

    st.markdown("### Weighted risk-index formula")

    st.latex(
        r"R = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U"
    )

    st.write(
        "Each input is scored from 0 to 100. The weighted contributions "
        "are added to produce a demonstration index between 0 and 100."
    )

    weights_df = pd.DataFrame(
        {
            "Factor": FACTORS,
            "Weight": [WEIGHTS[f] for f in FACTORS],
            "Weight (%)": [WEIGHTS[f] * 100 for f in FACTORS],
            "Meaning": [
                "Illustrative hazard score",
                "Illustrative vulnerability score",
                "Illustrative population score",
                "Illustrative exposure score",
                "Illustrative urgency score",
            ],
        }
    )

    show_table(weights_df, 260)

    st.markdown("### Classification thresholds")

    thresholds_df = pd.DataFrame(
        [
            {"Priority": "CRITICAL", "Index Range": "80–100"},
            {"Priority": "HIGH", "Index Range": "65–79.9"},
            {"Priority": "MODERATE", "Index Range": "45–64.9"},
            {"Priority": "LOWER", "Index Range": "Below 45"},
        ]
    )

    show_table(thresholds_df, 220)

    st.markdown("### What the prototype does")

    st.markdown(
        """
        - Stores illustrative scores for six example environmental zones.
        - Calculates a weighted priority index using fixed factor weights.
        - Classifies zones according to predefined thresholds.
        - Displays interactive charts and comparisons.
        - Lets users explore hypothetical scenarios.
        - Exports tables and a text briefing.
        """
    )

    st.markdown("### What the prototype does not do")

    st.markdown(
        """
        - It does not use live sensor, satellite, or weather feeds.
        - It does not establish a scientifically validated disaster forecast.
        - It does not calculate the probability of a disaster.
        - It does not contain a trained machine-learning model in this version.
        - It does not replace expert assessment or official emergency alerts.
        """
    )

    st.markdown("### Technology stack")

    tech_df = pd.DataFrame(
        [
            {"Technology": "Python", "Purpose": "Calculations and application logic"},
            {"Technology": "Streamlit", "Purpose": "Interactive dashboard interface"},
            {"Technology": "Pandas", "Purpose": "Organising and displaying tabular data"},
            {"Technology": "Plotly", "Purpose": "Interactive visualisations"},
            {"Technology": "GitHub", "Purpose": "Source-code version control and hosting workflow"},
        ]
    )

    show_table(tech_df, 250)

    st.markdown("### Download complete results")

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    st.download_button(
        "⬇ Download complete results (CSV)",
        data=csv_buffer.getvalue().encode("utf-8"),
        file_name="tera_2_complete_results.csv",
        mime="text/csv",
        key="method_csv",
    )

    st.download_button(
        "⬇ Download methodology report (TXT)",
        data=make_report(df),
        file_name="tera_2_methodology_report.txt",
        mime="text/plain",
        key="method_txt",
    )

# -------------------- FOOTER --------------------

st.divider()

st.markdown(
    f"""
    <div style="text-align:center; padding:10px; color:{MUTED};">
        <div style="color:{CYAN}; font-weight:800; letter-spacing:2px;">
            TERA 2.0 • MIDNIGHT INTELLIGENCE
        </div>
        <div style="font-size:12px; margin-top:6px;">
            Technology for Environmental Risk Analysis
        </div>
        <div style="font-size:11px; margin-top:5px;">
            Educational prototype · Illustrative inputs · Not an operational
            early-warning system
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
