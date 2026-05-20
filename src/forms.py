from __future__ import annotations
from datetime import date
import streamlit as st
from .calculations import compute_bonus, compute_section_scores, compute_weighted_score, status_from_weighted
from .config import DNA_OPTIONS, FORM_SECTIONS, STORES, STRATEGIC_FIELDS
from .db import insert_evaluation, save_uploaded_file
from .ui import header


def _section_header(number: int, title: str, description: str = "Avaliação oficial de performance da loja") -> None:
    st.markdown(
        f"""
        <div class="charth-section-header">
            <div class="charth-section-number">Seção {number} de 11</div>
            <div class="charth-section-title">{title}</div>
            <div class="charth-field-hint">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_input(question: dict, section_name: str) -> float:
    key = f"score_{section_name}_{question['key']}"
    qtype = question["type"]

    st.markdown('<div class="charth-score-wrap">', unsafe_allow_html=True)

    if qtype == "score":
        st.markdown("<div class='charth-score-helper'>Escala de 1 a 10</div>", unsafe_allow_html=True)
        val = st.radio(
            question["label"],
            options=list(range(1, 11)),
            index=9,
            horizontal=True,
            key=key,
            label_visibility="visible",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return float(val)

    if qtype == "binary":
        st.markdown("<div class='charth-score-helper'>Resposta binária: Sim = 10 · Não = 0</div>", unsafe_allow_html=True)
        val = st.radio(question["label"], options=["Sim", "Não"], horizontal=True, key=key)
        st.markdown("</div>", unsafe_allow_html=True)
        return 10.0 if val == "Sim" else 0.0

    if qtype == "binary_inverse":
        st.markdown("<div class='charth-score-helper'>Resposta binária: Não = 10 · Sim = 0</div>", unsafe_allow_html=True)
        val = st.radio(
            question["label"],
            options=["Não", "Sim"],
            horizontal=True,
            key=key,
            help="Não = 10, Sim = 0",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return 10.0 if val == "Não" else 0.0

    st.markdown("</div>", unsafe_allow_html=True)
    raise ValueError(f"Tipo desconhecido: {qtype}")


def render_evaluation_form(user: dict) -> None:
    header("Nova Avaliação", "Formulário oficial de supervisão das lojas CHARTH.")
    st.markdown(
        """
        <div class="charth-form-hero">
            <div class="charth-form-hero-title">Avaliação Supervisão Varejo</div>
            <div class="charth-form-hero-subtitle">
                Preencha com atenção aos detalhes. A avaliação consolida atendimento, VM, resultados, gestão e experiência da cliente,
                preservando o padrão premium e atemporal da CHARTH.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("evaluation_form", clear_on_submit=False):
        _section_header(1, "Identificação", "Dados principais da visita de supervisão")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                evaluation_date = st.date_input("Data", value=date.today())
                supervisor = st.text_input("Supervisora", value=user.get("name", "") if user.get("role") == "supervisora" else "")
            with c2:
                manager = st.text_input("Gerente de Loja")
                store = st.selectbox("Loja", STORES)

        scores: dict[str, float] = {}
        observations: dict[str, str] = {}
        photo_vm = None
        for idx, section in enumerate(FORM_SECTIONS, start=2):
            _section_header(idx, section["name"])
            with st.container(border=True):
                questions = section["questions"]
                for i in range(0, len(questions), 2):
                    cols = st.columns(2)
                    for col, q in zip(cols, questions[i:i+2]):
                        with col:
                            scores[q["key"]] = score_input(q, section["name"])
                if section.get("photo_key"):
                    st.markdown("#### Evidência visual")
                    photo_vm = st.file_uploader("Enviar foto, caso necessário", type=["png", "jpg", "jpeg", "webp"], key="foto_vm_upload")
                observations[section["observation_key"]] = st.text_area(
                    f"Observações {section['name']}", key=f"obs_{section['observation_key']}", height=100,
                    placeholder="Registre aqui os principais pontos observados, combinados e oportunidades de evolução."
                )

        _section_header(11, "Perguntas Estratégicas", "Síntese qualitativa para gestão e evolução da loja")
        with st.container(border=True):
            strategic = {}
            for field in STRATEGIC_FIELDS:
                strategic[field["key"]] = st.text_area(field["label"], key=f"strategic_{field['key']}", height=90)
            strategic["dna_charth"] = st.radio("A loja representa o DNA da Charth?", DNA_OPTIONS, horizontal=True)
            grave_issue = st.radio("Houve falta grave disciplinar no período avaliado?", ["Não", "Sim"], horizontal=True) == "Sim"

        submitted = st.form_submit_button("Salvar avaliação", use_container_width=True)

    if submitted:
        if not supervisor.strip() or not manager.strip():
            st.error("Preencha Supervisora e Gerente de Loja antes de salvar.")
            return
        section_scores = compute_section_scores(scores)
        weighted_score = compute_weighted_score(section_scores)
        overall_status = status_from_weighted(weighted_score)
        bonus = compute_bonus(section_scores, weighted_score, grave_issue)
        photo_path = save_uploaded_file(photo_vm, f"{store}_vm") if photo_vm else None
        evaluation_id = insert_evaluation(
            {
                "evaluation_date": evaluation_date.isoformat(),
                "supervisor": supervisor.strip(),
                "manager": manager.strip(),
                "store": store,
                "scores": scores,
                "observations": observations,
                "strategic": strategic,
                "section_scores": section_scores,
                "weighted_score": weighted_score,
                "overall_status": overall_status,
                "bonus": bonus,
                "grave_disciplinary_issue": grave_issue,
                "photo_vm_path": photo_path,
                "created_by": user.get("username"),
            }
        )
        st.success(f"Avaliação #{evaluation_id} salva com sucesso.")
        st.info(f"Média ponderada: {weighted_score:.2f} · Status: {overall_status} · Bonificação: {bonus['level']}")
