from __future__ import annotations

import streamlit as st

from .calculations import score_status


def apply_brand_css() -> None:
    st.markdown(
        """
        <style>
        @font-face {
            font-family: 'SIMPLO';
            src: local('SIMPLO'), local('Simplo'), local('SIMPLO Regular');
        }

        :root {
            --charth-black: #1F1F1F;
            --charth-ink: #111111;
            --charth-gray: #6D6E71;
            --charth-silver: #B8B8B8;
            --charth-silver-soft: #E7E2DF;
            --charth-silver-line: #D8D2CF;
            --charth-rose: #C9A0A0;
            --charth-rose-deep: #B98585;
            --charth-rose-soft: #F3E8E6;
            --charth-cream: #F8F6F3;
            --charth-card: #FFFDFC;
            --charth-gold: #C8A24A;
            --charth-gold-soft: #E7CFA2;
            --charth-bronze: #A66A3F;
            --charth-critical: #7F3438;
            --charth-gradient: linear-gradient(135deg, #FFFDFC 0%, #F3E8E6 100%);
        }

        html,
        body,
        .stApp,
        .stMarkdown,
        .stTextInput,
        .stTextArea,
        .stSelectbox,
        .stRadio,
        .stDateInput,
        .stNumberInput,
        button,
        input,
        textarea {
            font-family: 'SIMPLO', 'Simplo', 'Avenir Next', 'Montserrat', 'Segoe UI', Arial, sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(201,160,160,.10) 0%, rgba(248,246,243,1) 38%, rgba(244,239,236,1) 100%);
            color: var(--charth-black);
        }

        h1, h2, h3 {
            color: var(--charth-black);
            letter-spacing: .01em;
            font-weight: 650;
        }

        h1 { font-size: 2.25rem !important; }
        h2 { font-size: 1.45rem !important; }
        h3 { font-size: 1.12rem !important; }

        .brand-title {
            color: var(--charth-black);
            font-size: 40px;
            font-weight: 300;
            letter-spacing: .52em;
            text-align: center;
            margin-bottom: 2px;
        }

        .brand-subtitle {
            color: var(--charth-gray);
            font-size: 12px;
            letter-spacing: .25em;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 28px;
        }

        .section-card,
        .login-card,
        .metric-card,
        .charth-premium-card,
        .charth-form-hero,
        .charth-section-header,
        div[data-testid="stForm"] .charth-score-wrap,
        div[data-testid="stForm"] div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--charth-gradient) !important;
            border: 1px solid rgba(201,160,160,.28) !important;
            box-shadow: 0 12px 30px rgba(31,31,31,.035) !important;
        }

        .section-card,
        .login-card,
        .metric-card,
        .charth-premium-card {
            border-radius: 24px;
            padding: 24px;
            margin-bottom: 18px;
        }

        .section-kicker {
            color: #8A7775;
            text-transform: uppercase;
            letter-spacing: .18em;
            font-size: 12px;
            margin-bottom: 4px;
            font-weight: 800;
        }

        .small-muted {
            color: var(--charth-gray);
            font-size: 12px;
            line-height: 1.5;
        }

        .charth-form-hero {
            border-radius: 28px;
            padding: 26px 28px;
            margin: 12px 0 22px 0;
        }

        .charth-form-hero-title {
            color: var(--charth-black);
            font-size: 24px;
            font-weight: 800;
            letter-spacing: .02em;
        }

        .charth-form-hero-subtitle {
            color: var(--charth-gray);
            font-size: 14px;
            line-height: 1.55;
            margin-top: 6px;
        }

        .charth-section-header {
            border-radius: 22px;
            padding: 22px 26px;
            margin-top: 18px;
            margin-bottom: 14px;
        }

        .charth-section-number {
            color: var(--charth-rose-deep);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .16em;
            margin-bottom: 4px;
        }

        .charth-section-title {
            color: var(--charth-black);
            font-size: 22px;
            font-weight: 800;
            letter-spacing: .01em;
        }

        .charth-field-hint {
            color: var(--charth-gray);
            font-size: 12px;
            margin-top: -4px;
            margin-bottom: 12px;
        }

        .status-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 6px 12px;
            color: white;
            font-size: 12px;
            letter-spacing: .05em;
            font-weight: 750;
            margin-top: 8px;
            margin-bottom: 8px;
        }

        div[data-testid="stWidgetLabel"] p,
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stDateInput label,
        .stNumberInput label {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            font-weight: 750 !important;
            font-size: 14px !important;
            line-height: 1.35 !important;
        }

        input:not([type="radio"]):not([type="checkbox"]),
        textarea,
        [data-baseweb="select"],
        [data-baseweb="input"] {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            background: #FFFDFC !important;
            border-radius: 14px !important;
            border-color: var(--charth-silver-line) !important;
        }

        [data-baseweb="select"] > div {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            background: #FFFDFC !important;
            border-color: var(--charth-silver-line) !important;
        }

        textarea,
        textarea:focus {
            background: #FFFDFC !important;
            border: 1px solid var(--charth-silver-line) !important;
            box-shadow: 0 6px 18px rgba(31,31,31,.035) !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #7E7E7E !important;
            -webkit-text-fill-color: #7E7E7E !important;
            opacity: 1 !important;
        }

        div[data-testid="stForm"] .charth-score-wrap {
            border-radius: 18px !important;
            padding: 16px !important;
            margin: 0 0 14px 0 !important;
        }

        div[data-testid="stForm"] .charth-question-rule {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        div[data-testid="stForm"] .charth-score-helper {
            color: var(--charth-gray) !important;
            -webkit-text-fill-color: var(--charth-gray) !important;
            font-size: 10px !important;
            font-weight: 650 !important;
            text-transform: uppercase !important;
            letter-spacing: .08em !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] > label {
            display: block !important;
            height: auto !important;
            width: auto !important;
            margin: 0 0 10px 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] > label p {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            font-size: 14px !important;
            font-weight: 780 !important;
            line-height: 1.35 !important;
            margin: 0 !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 8px !important;
            align-items: center !important;
            margin-top: 0 !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] input[type="radio"] {
            position: absolute !important;
            opacity: 0 !important;
            width: 1px !important;
            height: 1px !important;
            min-width: 1px !important;
            min-height: 1px !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            pointer-events: none !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label {
            position: relative !important;
            min-width: 46px !important;
            height: 40px !important;
            padding: 0 16px !important;
            margin: 0 4px 8px 0 !important;
            border: 1px solid var(--charth-silver-line) !important;
            border-radius: 999px !important;
            background: linear-gradient(180deg, #FFFFFF 0%, #FFFDFC 100%) !important;
            box-shadow: 0 6px 15px rgba(31,31,31,.045) !important;
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            transition: all .16s ease-in-out !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background: linear-gradient(135deg, #FFFDFC 0%, var(--charth-rose-soft) 100%) !important;
            border-color: var(--charth-rose) !important;
            box-shadow: 0 8px 20px rgba(201,160,160,.22) !important;
            transform: translateY(-1px);
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, var(--charth-rose) 0%, var(--charth-gold-soft) 100%) !important;
            border: 1px solid var(--charth-gold) !important;
            box-shadow:
                inset 0 0 0 1px rgba(255,255,255,.55),
                0 9px 22px rgba(185,133,133,.27),
                0 2px 0 rgba(200,162,74,.42) !important;
        }

        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label p,
        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label span,
        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p,
        div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            font-weight: 850 !important;
        }

        .stButton > button {
            border-radius: 999px;
            border: 1px solid var(--charth-black);
            background: var(--charth-black);
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            letter-spacing: .05em;
            font-weight: 700;
        }

        .stButton > button * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }

        .stButton > button:hover {
            border-color: var(--charth-rose);
            background: var(--charth-rose);
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
        }

        .stButton > button:hover * {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            fill: var(--charth-black) !important;
            stroke: var(--charth-black) !important;
        }

        [data-testid="stSidebar"] {
            background: #F2ECE9;
        }

        [data-testid="stSidebar"],
        [data-testid="stSidebar"] * {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
        }

        [data-testid="stSidebar"] div[data-testid="stRadio"] label {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            height: auto !important;
            min-width: unset !important;
            padding: 2px 0 !important;
            margin: 0 !important;
            display: flex !important;
            justify-content: flex-start !important;
        }

        [data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {
            display: flex !important;
        }

        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] .stButton > button {
            background: var(--charth-black) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: 1px solid var(--charth-black) !important;
            box-shadow: none !important;
        }

        [data-testid="stSidebar"] button *,
        [data-testid="stSidebar"] .stButton > button * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }

        .dataframe {
            font-size: 13px;
        }

        @media (max-width: 768px) {

            /* Mobile: fundo com mais contraste */
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(201,160,160,.22) 0%, rgba(248,246,243,1) 36%, rgba(232,224,220,1) 100%) !important;
            }

            /* Mobile: cards mais destacados */
            .charth-form-hero,
            .charth-section-header,
            div[data-testid="stForm"] .charth-score-wrap,
            .section-card,
            .login-card,
            .metric-card,
            .charth-premium-card,
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: linear-gradient(135deg, #FFFFFF 0%, #F3E8E6 100%) !important;
                border: 1px solid rgba(185,133,133,.36) !important;
                box-shadow: 0 12px 28px rgba(31,31,31,.085) !important;
            }

            /* Mobile: campos internos mais legíveis */
            input:not([type="radio"]):not([type="checkbox"]),
            textarea,
            [data-baseweb="select"],
            [data-baseweb="input"] {
                background: #FFFFFF !important;
                border: 1px solid rgba(109,110,113,.24) !important;
            }

            .brand-title {
                font-size: 28px;
                letter-spacing: .36em;
                text-align: left;
            }

            .brand-subtitle {
                text-align: left;
                letter-spacing: .14em;
                font-size: 10px;
            }

            h1 { font-size: 1.75rem !important; }
            h2 { font-size: 1.25rem !important; }
            h3 { font-size: 1.05rem !important; }

            .charth-form-hero {
                padding: 20px 18px;
                border-radius: 22px;
            }

            .charth-section-title {
                font-size: 19px;
            }

            .section-card,
            .login-card,
            .metric-card,
            .charth-premium-card {
                padding: 18px;
                border-radius: 20px;
            }

            div[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label {
                min-width: 42px !important;
                height: 38px !important;
                padding: 0 13px !important;
                margin: 0 3px 7px 0 !important;
            }

            input:not([type="radio"]):not([type="checkbox"]),
            textarea,
            [data-baseweb="select"],
            [data-baseweb="select"] *,
            [data-baseweb="input"],
            [data-baseweb="input"] * {
                font-size: 16px !important;
                color: var(--charth-black) !important;
                -webkit-text-fill-color: var(--charth-black) !important;
            }
        }

        /* =========================================================
           Upload de foto: botão claro com gradiente CHARTH
           Especialmente importante no mobile, onde o botão preto
           prejudicava a leitura.
           ========================================================= */
        div[data-testid="stFileUploader"] button,
        div[data-testid="stFileUploader"] section button,
        div[data-testid="stFileUploader"] [data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #FFFDFC 0%, #F3E8E6 100%) !important;
            color: #1F1F1F !important;
            -webkit-text-fill-color: #1F1F1F !important;
            border: 1px solid rgba(201,160,160,.45) !important;
            border-radius: 999px !important;
            box-shadow: 0 8px 18px rgba(31,31,31,.06) !important;
            font-weight: 750 !important;
            letter-spacing: .03em !important;
        }

        div[data-testid="stFileUploader"] button *,
        div[data-testid="stFileUploader"] section button *,
        div[data-testid="stFileUploader"] [data-testid="baseButton-secondary"] * {
            color: #1F1F1F !important;
            -webkit-text-fill-color: #1F1F1F !important;
            fill: #1F1F1F !important;
            stroke: #1F1F1F !important;
        }

        div[data-testid="stFileUploader"] button:hover,
        div[data-testid="stFileUploader"] section button:hover,
        div[data-testid="stFileUploader"] [data-testid="baseButton-secondary"]:hover {
            background: linear-gradient(135deg, #F3E8E6 0%, #E7CFA2 100%) !important;
            color: #1F1F1F !important;
            -webkit-text-fill-color: #1F1F1F !important;
            border-color: #C8A24A !important;
            box-shadow: 0 10px 22px rgba(201,160,160,.20) !important;
        }

        div[data-testid="stFileUploader"] section {
            background: linear-gradient(135deg, #FFFDFC 0%, #F3E8E6 100%) !important;
            border: 1px dashed rgba(201,160,160,.55) !important;
            border-radius: 18px !important;
        }

        div[data-testid="stFileUploader"] section *,
        div[data-testid="stFileUploader"] small,
        div[data-testid="stFileUploader"] span,
        div[data-testid="stFileUploader"] p {
            color: #1F1F1F !important;
            -webkit-text-fill-color: #1F1F1F !important;
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
            <div style="font-size:30px; color:#1F1F1F; font-weight:650;">{value}</div>
            <div class="small-muted">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
