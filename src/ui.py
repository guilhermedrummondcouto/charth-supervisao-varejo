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
            --charth-silver-line: #CFC8C4;
            --charth-rose: #C9A0A0;
            --charth-rose-deep: #B98585;
            --charth-rose-soft: #F3E8E6;
            --charth-cream: #F8F6F3;
            --charth-card: #FFFDFC;
            --charth-gold: #C8A24A;
            --charth-bronze: #A66A3F;
            --charth-critical: #7F3438;
            --charth-alert: #B8875D;
            --charth-good: #6D6E71;
            --charth-great: #C9A0A0;
        }

        html,
        body,
        [class*="css"],
        .stApp,
        .stMarkdown,
        .stTextInput,
        .stTextArea,
        .stSelectbox,
        .stRadio,
        .stDateInput,
        .stNumberInput {
            font-family: 'SIMPLO', 'Avenir Next', 'Segoe UI', Arial, sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(201,160,160,.11) 0%, rgba(248,246,243,1) 34%, rgba(244,239,236,1) 100%);
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
        .charth-premium-card {
            background: rgba(255,253,252,.96);
            border: 1px solid rgba(201,160,160,.24);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 18px 45px rgba(31,31,31,.045);
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
            background: linear-gradient(135deg, #FFFDFC 0%, #F3E8E6 100%);
            border: 1px solid rgba(201,160,160,.28);
            border-radius: 28px;
            padding: 26px 28px;
            margin: 12px 0 22px 0;
            box-shadow: 0 18px 42px rgba(31,31,31,.045);
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
            background: #FFFDFC;
            border-top: 1px solid rgba(201,160,160,.32);
            border-bottom: 1px solid rgba(201,160,160,.18);
            padding: 16px 4px 14px 4px;
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
            margin-top: 6px;
            margin-bottom: 8px;
        }

        .charth-score-wrap {
            background: #FFFDFC;
            border: 1px solid rgba(109,110,113,.14);
            border-radius: 18px;
            padding: 14px 16px 10px 16px;
            margin: 0 0 12px 0;
        }

        /* =========================================================
           SLIDER CHARTH
           Regra: NENHUM vermelho/coral.
           Base em prata suave, trilho ativo preto, bolinha rosê.
           ========================================================= */

        div[data-testid="stSlider"] {
            --slider-track: var(--charth-silver-soft);
            --slider-active: var(--charth-black);
            --slider-handle: var(--charth-rose);
        }

        div[data-testid="stSlider"] label,
        div[data-testid="stSlider"] p,
        div[data-testid="stSlider"] span {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
        }

        div[data-testid="stSlider"] [data-baseweb="slider"] {
            color: var(--charth-black) !important;
        }

        /* Fundo do trilho */
        div[data-testid="stSlider"] [data-baseweb="slider"] > div,
        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div,
        div[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderThumbValue"] {
            border-color: var(--charth-silver-line) !important;
        }

        /* Remove qualquer vermelho/coral aplicado por tema inline */
        div[data-testid="stSlider"] [style*="255, 75, 75"],
        div[data-testid="stSlider"] [style*="255,75,75"],
        div[data-testid="stSlider"] [style*="#ff4b4b"],
        div[data-testid="stSlider"] [style*="#FF4B4B"],
        div[data-testid="stSlider"] [style*="rgb(255"],
        div[data-testid="stSlider"] [style*="coral"] {
            background: var(--charth-black) !important;
            background-color: var(--charth-black) !important;
            color: var(--charth-black) !important;
            border-color: var(--charth-black) !important;
        }

        /* Trilho geral: prata */
        div[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
            background: var(--charth-silver-soft) !important;
            box-shadow: none !important;
        }

        /* Parte ativa: preto */
        div[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child > div {
            background: var(--charth-black) !important;
            box-shadow: none !important;
        }

        /* Cobertura extra para versões diferentes do BaseWeb */
        div[data-testid="stSlider"] [data-baseweb="slider"] > div:nth-child(1) > div:nth-child(1),
        div[data-testid="stSlider"] [data-baseweb="slider"] > div:nth-child(1) > div:nth-child(2),
        div[data-testid="stSlider"] [data-baseweb="slider"] > div:nth-child(2),
        div[data-testid="stSlider"] [data-baseweb="slider"] > div:nth-child(3) {
            background-color: var(--charth-black) !important;
        }

        /* Bolinha */
        div[data-testid="stSlider"] div[role="slider"] {
            background: var(--charth-rose) !important;
            background-color: var(--charth-rose) !important;
            border: 3px solid #FFFFFF !important;
            box-shadow: 0 0 0 2px rgba(31,31,31,.20), 0 5px 14px rgba(31,31,31,.14) !important;
            outline: none !important;
        }

        div[data-testid="stSlider"] div[role="slider"]:hover,
        div[data-testid="stSlider"] div[role="slider"]:focus,
        div[data-testid="stSlider"] div[role="slider"][aria-valuenow] {
            background: var(--charth-rose) !important;
            background-color: var(--charth-rose) !important;
            border-color: #FFFFFF !important;
            box-shadow: 0 0 0 3px rgba(201,160,160,.36), 0 8px 18px rgba(31,31,31,.16) !important;
        }

        /* Número que aparece acima/ao lado da bolinha */
        div[data-testid="stSlider"] [data-testid="stThumbValue"],
        div[data-testid="stSlider"] [data-testid="stSliderThumbValue"],
        div[data-testid="stSlider"] div[role="slider"] + div,
        div[data-testid="stSlider"] div[role="slider"] ~ div {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            background: transparent !important;
        }

        /* Ticks 1 e 10 */
        div[data-testid="stSlider"] [data-testid="stTickBar"],
        div[data-testid="stSlider"] [data-testid="stTickBarMin"],
        div[data-testid="stSlider"] [data-testid="stTickBarMax"],
        div[data-testid="stSlider"] [data-testid="stTickBar"] * {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
        }

        /* Labels, inputs e selects */
        div[data-testid="stWidgetLabel"] p,
        label,
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stRadio label,
        .stDateInput label,
        .stNumberInput label {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            font-weight: 750 !important;
            font-size: 14px !important;
            line-height: 1.35 !important;
        }

        input,
        textarea,
        [data-baseweb="select"] {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            background: #F7F4F2 !important;
            border-radius: 14px !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #7E7E7E !important;
            -webkit-text-fill-color: #7E7E7E !important;
            opacity: 1 !important;
        }

        /* Botões */
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

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #F2ECE9;
        }

        [data-testid="stSidebar"],
        [data-testid="stSidebar"] * {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
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

        [data-testid="stSidebar"] button:hover,
        [data-testid="stSidebar"] .stButton > button:hover {
            background: var(--charth-rose) !important;
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            border-color: var(--charth-rose) !important;
        }

        [data-testid="stSidebar"] button:hover *,
        [data-testid="stSidebar"] .stButton > button:hover * {
            color: var(--charth-black) !important;
            -webkit-text-fill-color: var(--charth-black) !important;
            fill: var(--charth-black) !important;
            stroke: var(--charth-black) !important;
        }

        .dataframe {
            font-size: 13px;
        }

        @media (max-width: 768px) {
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

            div[data-testid="stWidgetLabel"] p,
            label,
            .stTextInput label,
            .stTextArea label,
            .stSelectbox label,
            .stRadio label,
            .stDateInput label,
            .stNumberInput label {
                font-size: 15px !important;
                color: var(--charth-black) !important;
                -webkit-text-fill-color: var(--charth-black) !important;
            }

            html,
            body,
            .stApp,
            .stMarkdown,
            .stMarkdown *,
            p,
            span,
            label,
            div[data-testid="stWidgetLabel"] p,
            .stTextInput label,
            .stTextArea label,
            .stSelectbox label,
            .stRadio label,
            .stDateInput label,
            .stNumberInput label,
            [data-testid="stSidebar"],
            [data-testid="stSidebar"] * {
                color: var(--charth-black) !important;
                -webkit-text-fill-color: var(--charth-black) !important;
            }

            input,
            textarea,
            [data-baseweb="select"],
            [data-baseweb="select"] *,
            [data-baseweb="input"],
            [data-baseweb="input"] * {
                font-size: 16px !important;
                color: var(--charth-black) !important;
                -webkit-text-fill-color: var(--charth-black) !important;
            }

            input::placeholder,
            textarea::placeholder {
                color: var(--charth-gray) !important;
                -webkit-text-fill-color: var(--charth-gray) !important;
                opacity: 1 !important;
            }

            .stButton > button {
                background: var(--charth-black) !important;
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
            }

            .stButton > button * {
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
                fill: #FFFFFF !important;
                stroke: #FFFFFF !important;
            }

            .stButton > button:hover {
                background: var(--charth-rose) !important;
                color: var(--charth-black) !important;
                -webkit-text-fill-color: var(--charth-black) !important;
            }

            .stButton > button:hover * {
                color: var(--charth-black) !important;
                -webkit-text-fill-color: var(--charth-black) !important;
                fill: var(--charth-black) !important;
                stroke: var(--charth-black) !important;
            }

            div[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
                background: var(--charth-silver-soft) !important;
            }

            div[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child > div {
                background: var(--charth-black) !important;
            }

            div[data-testid="stSlider"] div[role="slider"] {
                background: var(--charth-rose) !important;
                background-color: var(--charth-rose) !important;
                border: 3px solid #FFFFFF !important;
            }
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
