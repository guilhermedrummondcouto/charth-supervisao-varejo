from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import pandas as pd
import streamlit as st
from .auth import can_edit
from .calculations import compute_weighted_score
from .config import BONUS_RULES, GESTORA_CAN_VIEW_ALL_STORES, ROLE_GESTORA, STORES, WEIGHTS
from .db import evaluations_df
from .ui import header, metric_card


def money(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def quarter_from_date(dt: pd.Timestamp) -> str:
    q = int(((dt.month - 1) // 3) + 1)
    return f"{dt.year}T{q}"


def quarter_index(label: str) -> int:
    year = int(label[:4])
    quarter = int(label[-1])
    return year * 4 + quarter


def previous_quarter_label(label: str, steps: int = 1) -> str:
    idx = quarter_index(label) - steps
    year = idx // 4
    q = idx % 4
    if q == 0:
        year -= 1
        q = 4
    return f"{year}T{q}"


def status_from_quarter(
    section_scores: dict[str, float],
    weighted_score: float,
    grave_issue: bool,
    gold_rule_key: str,
    min_block_scope: str,
) -> tuple[str, str]:
    rules = BONUS_RULES
    if min_block_scope == "weighted_sections":
        block_values = [float(section_scores.get(section, 0.0)) for section in WEIGHTS.keys()]
    else:
        block_values = [float(v) for v in section_scores.values()]
    min_block = min(block_values) if block_values else 0.0
    result_score = float(section_scores.get("Resultados e Indicadores", 0.0))
    management_score = float(section_scores.get("Gestão da Gerente", 0.0))

    gold_rule = rules.get(gold_rule_key, rules["gold_strict"])
    if (
        weighted_score >= gold_rule["min_weighted_score"]
        and result_score >= gold_rule["min_results"]
        and management_score >= gold_rule["min_management"]
        and min_block >= gold_rule["min_block"]
        and (not gold_rule.get("requires_no_grave_disciplinary_issue", True) or not grave_issue)
    ):
        return "Ouro", "Média, resultado, gestão, blocos mínimos e ausência de falta grave atendidos."

    silver = rules["silver"]
    if (
        weighted_score >= silver["min_weighted_score"]
        and result_score >= silver["min_results"]
        and management_score >= silver["min_management"]
        and min_block >= silver["min_block"]
    ):
        return "Prata", "Critérios de Loja Forte atendidos. Equipe sem premiação financeira."

    bronze = rules["bronze"]
    if weighted_score >= bronze["min_weighted_score"] and min_block >= bronze["min_block"]:
        return "Bronze", "Critério Bronze configurável atingido."

    return "Sem bônus", "Critérios mínimos de bonificação não atingidos."


def aggregate_store_quarter(df: pd.DataFrame, store: str, quarter: str, gold_rule_key: str, min_block_scope: str) -> dict[str, Any] | None:
    qdf = df[(df["store"] == store) & (df["quarter"] == quarter)].copy()
    if qdf.empty:
        return None
    section_names: set[str] = set()
    for scores in qdf["section_scores_json"]:
        if isinstance(scores, dict):
            section_names.update(scores.keys())
    section_scores = {}
    for section in sorted(section_names):
        vals = [float(scores.get(section, 0.0)) for scores in qdf["section_scores_json"] if isinstance(scores, dict) and section in scores]
        section_scores[section] = round(sum(vals) / len(vals), 2) if vals else 0.0
    weighted_score = compute_weighted_score(section_scores)
    grave_issue = bool(qdf.get("grave_disciplinary_issue", pd.Series(dtype=int)).fillna(0).astype(int).max())
    level, reason = status_from_quarter(section_scores, weighted_score, grave_issue, gold_rule_key, min_block_scope)
    return {
        "loja": store,
        "trimestre": quarter,
        "avaliacoes": int(len(qdf)),
        "media_ponderada": weighted_score,
        "resultado": float(section_scores.get("Resultados e Indicadores", 0.0)),
        "gestao": float(section_scores.get("Gestão da Gerente", 0.0)),
        "menor_bloco": min(section_scores.values()) if section_scores else 0.0,
        "nivel": level,
        "motivo": reason,
        "falta_grave": "Sim" if grave_issue else "Não",
        "section_scores": section_scores,
    }


def compute_consecutive_gold(all_quarter_rows: dict[tuple[str, str], dict[str, Any]], store: str, quarter: str) -> int:
    count = 0
    current = quarter
    while True:
        row = all_quarter_rows.get((store, current))
        if not row or row.get("nivel") != "Ouro":
            break
        count += 1
        current = previous_quarter_label(current)
    return count


def build_quarter_table(df: pd.DataFrame, stores: list[str], gold_rule_key: str, min_block_scope: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    rows = []
    quarters = sorted(df["quarter"].dropna().unique().tolist(), key=quarter_index)
    for quarter in quarters:
        for store in stores:
            agg = aggregate_store_quarter(df, store, quarter, gold_rule_key, min_block_scope)
            if agg:
                rows.append(agg)
    if not rows:
        return pd.DataFrame()
    base_by_key = {(row["loja"], row["trimestre"]): row for row in rows}
    final_rows = []
    for row in rows:
        consecutive = compute_consecutive_gold(base_by_key, row["loja"], row["trimestre"])
        base_value = BONUS_RULES["quarterly_manager_values"].get(row["nivel"], 0.0)
        extra = BONUS_RULES["consecutive_gold_extra"].get(min(consecutive, 4), BONUS_RULES["consecutive_gold_extra"].get(4, 0.0)) if row["nivel"] == "Ouro" else 0.0
        out = {k: v for k, v in row.items() if k != "section_scores"}
        out["ouros_consecutivos"] = consecutive if row["nivel"] == "Ouro" else 0
        out["bonus_base_gerente"] = base_value
        out["adicional_ouro_consecutivo"] = extra
        out["bonus_total_gerente"] = base_value + extra
        final_rows.append(out)
    return pd.DataFrame(final_rows)


def team_fund_simulator(level: str) -> None:
    st.markdown("### Fundo Ouro da Equipe")
    if level != "Ouro":
        st.info("O Fundo Ouro da equipe só é calculado para lojas classificadas como Ouro no trimestre.")
        return
    faturamento = st.number_input("Faturamento trimestral da loja", min_value=0.0, value=0.0, step=1000.0)
    fundo_total = faturamento * BONUS_RULES["team_fund_percent"]
    fundo_vendas = fundo_total * BONUS_RULES["team_sales_percent"]
    fundo_suporte = fundo_total * BONUS_RULES["team_support_percent"]
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Fundo Ouro", money(fundo_total), "1% do faturamento trimestral")
    with c2:
        metric_card("Equipe de vendas", money(fundo_vendas), "75% do Fundo Ouro")
    with c3:
        metric_card("Equipe suporte", money(fundo_suporte), "25% do Fundo Ouro")

    st.caption("Distribuição de vendas: valor proporcional à participação de cada vendedora no faturamento trimestral. Suporte: divisão igualitária entre elegíveis.")
    qtd_vendas = st.number_input("Quantidade de pessoas elegíveis em vendas", min_value=0, max_value=30, value=0, step=1)
    if qtd_vendas > 0:
        sales_data = pd.DataFrame({"Nome": [f"Vendedora {i+1}" for i in range(int(qtd_vendas))], "Venda trimestral": [0.0] * int(qtd_vendas)})
        edited_sales = st.data_editor(sales_data, use_container_width=True, hide_index=True, key="bonus_sales_editor")
        total_sales = float(edited_sales["Venda trimestral"].sum()) if not edited_sales.empty else 0.0
        if total_sales > 0:
            edited_sales["Participação"] = edited_sales["Venda trimestral"] / total_sales
            edited_sales["Bônus estimado"] = edited_sales["Participação"] * fundo_vendas
            st.dataframe(edited_sales, use_container_width=True, hide_index=True)
        else:
            st.warning("Informe as vendas individuais para calcular a distribuição proporcional.")

    qtd_suporte = st.number_input("Quantidade de pessoas elegíveis no suporte", min_value=0, max_value=30, value=0, step=1)
    if qtd_suporte > 0:
        st.write(f"Bônus estimado por pessoa do suporte: **{money(fundo_suporte / qtd_suporte)}**")
    st.markdown("#### Requisitos individuais")
    st.write("90 dias mínimos na loja · presença maior ou igual a 90% · sem advertência grave · nota individual maior ou igual a 8.")


def bonus_page(user: dict) -> None:
    header("Bonificação Trimestral", "Cálculo por loja, nível de bônus, consecutividade Ouro e Fundo Ouro da equipe.")
    df = evaluations_df()
    if df.empty:
        st.info("Ainda não existem avaliações salvas. Registre uma avaliação para calcular bonificação trimestral.")
        return
    if user.get("role") == ROLE_GESTORA and not GESTORA_CAN_VIEW_ALL_STORES:
        df = df[df["store"] == user.get("store")]
    df = df.copy()
    df["quarter"] = df["evaluation_date"].apply(quarter_from_date)

    st.markdown("## Regras ativas")
    c1, c2 = st.columns(2)
    with c1:
        gold_rule_key = st.selectbox(
            "Regra de Ouro",
            ["gold_strict", "gold_standard"],
            index=0 if BONUS_RULES["default_gold_rule"] == "gold_strict" else 1,
            format_func=lambda x: "Ouro rigoroso: média ≥ 8,8, resultado ≥ 9,0" if x == "gold_strict" else "Ouro padrão: média ≥ 8,5, resultado ≥ 8,8",
        )
    with c2:
        min_block_scope = st.selectbox(
            "Escopo do menor bloco",
            ["all_sections", "weighted_sections"],
            index=0 if BONUS_RULES["min_block_scope"] == "all_sections" else 1,
            format_func=lambda x: "Todas as seções avaliativas" if x == "all_sections" else "Somente blocos da média ponderada",
        )

    available_stores = sorted(df["store"].dropna().unique().tolist()) or STORES
    quarters = sorted(df["quarter"].dropna().unique().tolist(), key=quarter_index, reverse=True)
    with st.expander("Filtros", expanded=True):
        f1, f2 = st.columns(2)
        with f1:
            selected_store = st.selectbox("Loja", ["Todas"] + available_stores)
        with f2:
            selected_quarter = st.selectbox("Trimestre", quarters)

    stores_for_calc = available_stores if selected_store == "Todas" else [selected_store]
    table = build_quarter_table(df, stores_for_calc, gold_rule_key, min_block_scope)
    if table.empty:
        st.warning("Nenhum cálculo disponível para os filtros selecionados.")
        return
    current = table[table["trimestre"] == selected_quarter].copy()
    if current.empty:
        st.warning("Nenhuma avaliação encontrada para esse trimestre.")
        return

    total_bonus = float(current["bonus_total_gerente"].sum())
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Bônus gerente", money(total_bonus), "Total estimado no trimestre")
    with col2:
        metric_card("Lojas Ouro", str((current["nivel"] == "Ouro").sum()), "Com Fundo Ouro da equipe")
    with col3:
        metric_card("Média do trimestre", f"{current['media_ponderada'].mean():.2f}", "Média ponderada oficial")
    with col4:
        metric_card("Avaliações", str(int(current["avaliacoes"].sum())), "Base usada no cálculo")

    st.markdown("## Resultado trimestral por loja")
    display_cols = [
        "loja", "trimestre", "avaliacoes", "media_ponderada", "resultado", "gestao", "menor_bloco",
        "nivel", "ouros_consecutivos", "bonus_base_gerente", "adicional_ouro_consecutivo", "bonus_total_gerente", "falta_grave", "motivo"
    ]
    st.dataframe(
        current[display_cols].rename(columns={
            "loja": "Loja",
            "trimestre": "Trimestre",
            "avaliacoes": "Avaliações",
            "media_ponderada": "Média geral",
            "resultado": "Resultado",
            "gestao": "Gestão",
            "menor_bloco": "Menor bloco",
            "nivel": "Nível",
            "ouros_consecutivos": "Ouros consecutivos",
            "bonus_base_gerente": "Bônus base gerente",
            "adicional_ouro_consecutivo": "Adicional consecutivo",
            "bonus_total_gerente": "Bônus total gerente",
            "falta_grave": "Falta grave",
            "motivo": "Critério aplicado",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("## Evolução de níveis por trimestre")
    evolution = table.sort_values(["loja", "trimestre"])
    st.dataframe(
        evolution[["loja", "trimestre", "media_ponderada", "nivel", "ouros_consecutivos", "bonus_total_gerente"]].rename(columns={
            "loja": "Loja",
            "trimestre": "Trimestre",
            "media_ponderada": "Média geral",
            "nivel": "Nível",
            "ouros_consecutivos": "Ouros consecutivos",
            "bonus_total_gerente": "Bônus gerente",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("## Simulação do Fundo Ouro")
    chosen_store = st.selectbox("Loja para simular Fundo Ouro", current["loja"].tolist())
    chosen_row = current[current["loja"] == chosen_store].iloc[0]
    team_fund_simulator(chosen_row["nivel"])

    st.markdown("## Exportação")
    st.download_button(
        "Baixar cálculo de bonificação em CSV",
        data=current.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"bonificacao_{selected_quarter}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    with st.expander("Critérios documentados"):
        st.markdown(
            """
**Níveis executivos:** Ouro R$ 5.000, Prata R$ 3.700, Bronze R$ 2.000.  
**Consecutividade Ouro:** 2 trimestres +R$ 1.000; 3 trimestres +R$ 2.000; 4 ou mais trimestres +R$ 3.000.  
**Ouro rigoroso:** média geral ≥ 8,8, Resultado ≥ 9,0, Gestão ≥ 8,5, sem bloco abaixo de 8 e sem falta grave.  
**Ouro padrão:** média geral ≥ 8,5, Resultado ≥ 8,8, Gestão ≥ 8,5, sem bloco abaixo de 8 e sem falta grave.  
**Prata:** média geral ≥ 8,0, Resultado ≥ 8,3, Gestão ≥ 8,0 e nenhum bloco abaixo de 7,5.  
**Bronze:** regra configurável em `src/config.py`, padrão: média geral ≥ 7,5 e nenhum bloco abaixo de 7.  
**Equipe no Ouro:** Fundo Ouro = 1% do faturamento trimestral; 75% vendas e 25% suporte.
"""
        )
