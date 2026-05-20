from __future__ import annotations
import streamlit as st
from .calculations import score_status


def apply_brand_css() -> None:
    st.markdown(
        """
        <style>
        @font-face { font-family: 'SIMPLO'; src: local('SIMPLO'), local('Simplo'); }
        :root {
            --charth-black: #1f1f1f;
            --charth-gray: #6d6e71;
            --charth-silver: #b8b8b8;
            --charth-rose: #c9a0a0;
            --charth-rose-soft: #f0e4e2;
            --charth-bg: #f8f6f3;
            --charth-card: #fffdfb;
        }
        html, body, [class*="css"] { font-family: 'SIMPLO', 'Avenir Next', 'Segoe UI', Arial, sans-serif; }
        .stApp { background: radial-gradient(circle at top left, #fbf7f4 0%, #f8f6f3 35%, #f4efec 100%); }
        h1, h2, h3 { letter-spacing: .02em; color: var(--charth-black); font-weight: 500; }
        .brand-title { letter-spacing: .48em; font-size: 38px; text-align:center; color:#1f1f1f; margin-bottom:2px; font-weight:300; }
        .brand-subtitle { letter-spacing:.22em; text-transform:uppercase; text-align:center; color:#6d6e71; font-size:12px; margin-bottom:28px; }
        .section-card, .login-card, .metric-card {
            background: rgba(255,253,251,.92);
            border: 1px solid rgba(201,160,160,.35);
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 18px 45px rgba(31,31,31,.06);
            margin-bottom: 18px;
        }
        .section-kicker { color:#8a7775; text-transform:uppercase; letter-spacing:.18em; font-size:12px; margin-bottom:4px; }
        .status-pill { display:inline-block; border-radius:999px; padding:6px 12px; color:white; font-size:12px; letter-spacing:.05em; font-weight:600; margin-top:6px; }
        .small-muted { color:#6d6e71; font-size:12px; }
        div[data-testid="stSlider"] div[role="slider"] { background-color: var(--charth-rose) !important; border-color: var(--charth-rose) !important; }
        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div { background-color: var(--charth-rose) !important; }
        .stButton>button { border-radius: 999px; border: 1px solid #c9a0a0; background: #1f1f1f; color: white; letter-spacing:.05em; }
        .stButton>button:hover { border-color: #c9a0a0; background:#c9a0a0; color:#1f1f1f; }
        [data-testid="stSidebar"] { background: #f2ece9; }
        .dataframe { font-size: 13px; }
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
            <div style="font-size:30px; color:#1f1f1f; font-weight:500;">{value}</div>
            <div class="small-muted">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
