from __future__ import annotations
from datetime import date
import streamlit as st
from .calculations import compute_bonus, compute_section_scores, compute_weighted_score, status_from_weighted
from .config import DNA_OPTIONS, FORM_SECTIONS, STORES, STRATEGIC_FIELDS
from .db import insert_evaluation, save_uploaded_file
from .ui import header, score_badge


def score_input(question: dict, section_name: str) -> float:
    key = f"score_{section_name}_{question['key']}"
    qtype = question["type"]
    if qtype == "score":
        val = st.slider(question["label"], min_value=1, max_value=10, value=10, step=1, key=key)
        score_badge(float(val))
        return float(val)
    if qtype == "binary":
        val = st.radio(question["label"], options=["Sim", "Não"], horizontal=True, key=key)
        score = 10.0 if val == "Sim" else 0.0
        score_badge(score)
        return score
    if qtype == "binary_inverse":
        val = st.radio(question["label"], options=["Não", "Sim"], horizontal=True, key=key, help="Não = 10, Sim = 0")
        score = 10.0 if val == "Não" else 0.0
        score_badge(score)
        return score
    raise ValueError(f"Tipo desconhecido: {qtype}")


def render_evaluation_form(user: dict) -> None:
    header("Nova Avaliação", "Formulário oficial de avaliação de supervisão das lojas CHARTH.")
    with st.form("evaluation_form", clear_on_submit=False):
        st.markdown("## Seção 1 de 11 · Identificação")
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
            st.markdown(f"---\n## Seção {idx} de 11 · {section['name']}")
            st.caption("Descrição opcional")
            for q in section["questions"]:
                scores[q["key"]] = score_input(q, section["name"])
            if section.get("photo_key"):
                photo_vm = st.file_uploader("Enviar foto, caso necessário", type=["png", "jpg", "jpeg", "webp"], key="foto_vm_upload")
            observations[section["observation_key"]] = st.text_area(
                f"Observações {section['name']}", key=f"obs_{section['observation_key']}", height=90
            )

        st.markdown("---\n## Seção 11 de 11 · Perguntas Estratégicas")
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
