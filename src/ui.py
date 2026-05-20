from __future__ import annotations
import streamlit as st
from .calculations import score_status


def apply_brand_css() -> None:
    st.markdown(
        """
        <style>
        @font-face { font-family: 'SIMPLO'; src: local('SIMPLO'), local('Simplo'); }
        :root {
            --charth-black: #1F1F1F;
            --charth-gray: #6D6E71;
            --charth-silver: #B8B8B8;
            --charth-rose: #C9A0A0;
            --charth-rose-deep: #B98585;
            --charth-rose-soft: #F3E8E6;
            --charth-cream: #F8F6F3;
            --charth-card: #FFFDFC;
            --charth-gold: #C8A24A;
            --charth-bronze: #A66A3F;
            --charth-critical: #9E3F45;
            --charth-alert: #B8875D;
            --charth-good: #6D6E71;
            --charth-great: #C9A0A0;
        }

        html, body, [class*="css"], .stMarkdown, .stTextInput, .stSelectbox, .stRadio, .stDateInput {
            font-family: 'SIMPLO', 'Avenir Next', 'Segoe UI', Arial, sans-serif !important;
        }
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(201,160,160,.16) 0%, rgba(248,246,243,1) 34%, rgba(244,239,236,1) 100%);
            color: var(--charth-black);
        }
        h1, h2, h3 {
            letter-spacing: .01em;
            color: var(--charth-black);
            font-weight: 650;
        }
        h1 { font-size: 2.25rem !important; }
        h2 { font-size: 1.45rem !important; }
        h3 { font-size: 1.12rem !important; }

        .brand-title {
            letter-spacing: .52em;
            font-size: 40px;
            text-align:center;
            color:#1F1F1F;
            margin-bottom:2px;
            font-weight:300;
        }
        .brand-subtitle {
            letter-spacing:.25em;
            text-transform:uppercase;
            text-align:center;
            color:#6D6E71;
            font-size:12px;
            margin-bottom:28px;
        }
        .section-card, .login-card, .metric-card, .charth-premium-card {
            background: rgba(255,253,252,.94);
            border: 1px solid rgba(201,160,160,.32);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 18px 45px rgba(31,31,31,.055);
            margin-bottom: 18px;
        }
        .section-kicker {
            color:#8A7775;
            text-transform:uppercase;
            letter-spacing:.18em;
            font-size:12px;
            margin-bottom:4px;
            font-weight:800;
        }
        .small-muted { color:#6D6E71; font-size:12px; line-height:1.5; }

        .charth-form-hero {
            background: linear-gradient(135deg, #FFFDFC 0%, #F3E8E6 100%);
            border: 1px solid rgba(201,160,160,.34);
            border-radius: 28px;
            padding: 26px 28px;
            margin: 12px 0 22px 0;
            box-shadow: 0 18px 42px rgba(31,31,31,.055);
        }
        .charth-form-hero-title {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: .02em;
            color: #1F1F1F;
        }
        .charth-form-hero-subtitle {
            font-size: 14px;
            color:#6D6E71;
            line-height:1.55;
            margin-top: 6px;
        }
        .charth-section-header {
            background: #FFFDFC;
            border-top: 1px solid rgba(201,160,160,.35);
            border-bottom: 1px solid rgba(201,160,160,.22);
            padding: 16px 4px 14px 4px;
            margin-top: 18px;
            margin-bottom: 14px;
        }
        .charth-section-number {
            color:#B98585;
            font-size:12px;
            font-weight:800;
            text-transform:uppercase;
            letter-spacing:.16em;
            margin-bottom:4px;
        }
        .charth-section-title {
            color:#1F1F1F;
            font-size:22px;
            font-weight:800;
            letter-spacing:.01em;
        }
        .charth-field-hint {
            color:#6D6E71;
            font-size:12px;
            margin-top:-4px;
            margin-bottom:12px;
        }
        .status-pill {
            display:inline-block;
            border-radius:999px;
            padding:6px 12px;
            color:white;
            font-size:12px;
            letter-spacing:.05em;
            font-weight:750;
            margin-top:6px;
            margin-bottom:8px;
        }
        .charth-score-wrap {
            background:#FFFDFC;
            border:1px solid rgba(109,110,113,.14);
            border-radius:18px;
            padding:14px 16px 10px 16px;
            margin: 0 0 12px 0;
        }

        /* Streamlit controls: marca e legibilidade */
        div[data-testid="stSlider"] div[role="slider"] {
            background-color: var(--charth-rose) !important;
            border-color: var(--charth-rose) !important;
            box-shadow: 0 0 0 4px rgba(201,160,160,.14) !important;
        }
        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
            background-color: var(--charth-rose) !important;
        }
        div[data-testid="stWidgetLabel"] p, label, .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label, .stDateInput label {
            color: #1F1F1F !important;
            font-weight: 750 !important;
            font-size: 14px !important;
            line-height: 1.35 !important;
        }
        input, textarea, [data-baseweb="select"] {
            color: #1F1F1F !important;
            background: #F7F4F2 !important;
            border-radius: 14px !important;
        }
        input::placeholder, textarea::placeholder { color: #7E7E7E !important; opacity: 1 !important; }
        .stButton>button {
            border-radius: 999px;
            border: 1px solid #C9A0A0;
            background: #1F1F1F;
            color: white;
            letter-spacing:.05em;
            font-weight:700;
        }
        .stButton>button:hover {
            border-color: #C9A0A0;
            background:#C9A0A0;
            color:#1F1F1F;
        }
        [data-testid="stSidebar"] { background: #F2ECE9; }
        [data-testid="stSidebar"] * { color: #1F1F1F; }
        .dataframe { font-size: 13px; }

        @media (max-width: 768px) {
            .brand-title { font-size: 28px; letter-spacing:.36em; text-align:left; }
            .brand-subtitle { text-align:left; letter-spacing:.14em; font-size:10px; }
            h1 { font-size: 1.75rem !important; }
            h2 { font-size: 1.25rem !important; }
            h3 { font-size: 1.05rem !important; }
            .charth-form-hero { padding: 20px 18px; border-radius:22px; }
            .charth-section-title { font-size:19px; }
            .section-card, .login-card, .metric-card, .charth-premium-card { padding:18px; border-radius:20px; }
            div[data-testid="stWidgetLabel"] p, label, .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label, .stDateInput label {
                font-size: 15px !important;
                color: #111 !important;
            }
            input, textarea { font-size: 16px !important; color:#111 !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header(title: str, subtitle: str = "") -> None:
    st.markdown('<div class="brand-title">CHARTH</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Supervisão de Varejo</div>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"<div class='small-muted'>{subtitle}</div>", unsafe_allow_html=True)


def score_badge(score: float) -> None:
    label, color = score_status(score)
    st.markdown(
        f"<span class='status-pill' style='background:{color};'>{label} · {float(score):.2f}</span>",
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, detail: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="section-kicker">{title}</div>
            <div style="font-size:30px; color:#1f1f1f; font-weight:650;">{value}</div>
            <div class="small-muted">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
