from __future__ import annotations
from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st
from .calculations import result_meta_reference, status_from_weighted
from .config import BONUS_CONFIG, FORM_SECTIONS, GESTORA_CAN_VIEW_ALL_STORES, ROLE_ADMIN, ROLE_GESTORA, STORES
from .db import action_plans_df, delete_evaluation, evaluations_df, export_flattened_evaluations
from .ui import header, metric_card


SECTION_LABELS = [section["name"] for section in FORM_SECTIONS]
OBSERVATION_LABELS = {
    "observacoes_equipe_atendimento": "Equipe e Atendimento",
    "observacoes_vm": "Visual Merchandising",
    "observacoes_estoque_produto": "Estoque e Produto",
    "observacoes_resultados": "Resultados e Indicadores",
    "observacoes_experiencia_cliente_premium": "Experiência da Cliente e Padrão Premium",
    "observacoes_whatsapp": "WhatsApp e Vendas Digitais",
    "observacoes_gestao_gerente": "Gestão da Gerente",
    "observacoes_estrutura_loja": "Estrutura da Loja",

    # Compatibilidade com avaliações antigas, caso existam no banco:
    "observacoes_experiencia_cliente": "Experiência da Cliente",
    "observacoes_experiencia_premium": "Experiência Premium",
}
STRATEGIC_LABELS = {
    "maior_risco": "Maior risco da loja hoje",
    "maior_oportunidade": "Maior oportunidade de crescimento imediato",
    "virar_ouro": "O que precisa acontecer para virar Ouro",
    "dna_charth": "A loja representa o DNA da Charth?",
}

STATUS_COLOR_MAP = {
    "Excelência CHARTH": "#C9A0A0",       # Rosê CHARTH
    "Loja Forte": "#C8A24A",             # Dourado
    "Loja em Atenção": "#A66A3F",        # Bronze
    "Plano de Ação Imediato": "#7F3438", # Crítico
}
BONUS_COLOR_MAP = {
    "Ouro": "#C8A24A",
    "Prata": "#B8B8B8",
    "Bronze": "#A66A3F",
    "Sem bônus": "#6D6E71",
}
SECTION_COLOR_SCALE = [[0, "#9E3F45"], [0.55, "#B8875D"], [0.72, "#A66A3F"], [0.85, "#B8B8B8"], [1, "#C8A24A"]]
STORE_SEQUENCE = ["#1F1F1F", "#C9A0A0", "#6D6E71", "#B8B8B8", "#C8A24A", "#A66A3F"]


def filter_df_for_user(df: pd.DataFrame, user: dict) -> pd.DataFrame:
    if df.empty:
        return df
    if user.get("role") == ROLE_GESTORA and not GESTORA_CAN_VIEW_ALL_STORES:
        return df[df["store"] == user.get("store")]
    return df


def _score_badge(score: float) -> str:
    if score >= 9:
        label, bg = "Excelência Charth", "#C8A24A"
    elif score >= 8:
        label, bg = "Forte", "#B8B8B8"
    elif score >= 7:
        label, bg = "Regular", "#A66A3F"
    elif score >= 5:
        label, bg = "Atenção", "#B8875D"
    else:
        label, bg = "Crítico", "#9E3F45"
    return f"""
    <span style="
        display:inline-block;
        padding:5px 10px;
        border-radius:999px;
        background:{bg};
        color:white;
        font-size:12px;
        font-weight:700;
        letter-spacing:.03em;
        white-space:nowrap;">
        {label} · {score:.2f}
    </span>
    """


def _empty_text(value) -> bool:
    return value is None or str(value).strip() == ""


def _safe_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _render_text_card(title: str, content: str, accent: str = "#C9A0A0") -> None:
    if _empty_text(content):
        content = "Sem observação registrada."
    st.markdown(
        f"""
        <div class="charth-history-card" style="border-left:4px solid {accent};">
            <div class="charth-history-card-title">{title}</div>
            <div class="charth-history-card-body">{str(content).replace(chr(10), '<br>')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_history_css() -> None:
    st.markdown(
        """
        <style>
        .charth-history-card {
            background: #ffffff;
            border: 1px solid rgba(109,110,113,.18);
            border-radius: 16px;
            padding: 16px 18px;
            margin-bottom: 12px;
            box-shadow: 0 10px 24px rgba(31,31,31,.035);
        }
        .charth-history-card-title {
            font-family: SIMPLO, "Inter", "Segoe UI", sans-serif;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
            color: #1f1f1f;
            margin-bottom: 8px;
        }
        .charth-history-card-body {
            font-family: SIMPLO, "Inter", "Segoe UI", sans-serif;
            font-size: 15px;
            line-height: 1.65;
            color: #343434;
            white-space: normal;
        }
        .charth-section-row {
            display:flex;
            justify-content:space-between;
            gap:16px;
            align-items:center;
            background:#fff;
            border:1px solid rgba(109,110,113,.16);
            border-radius:14px;
            padding:12px 14px;
            margin-bottom:8px;
        }
        .charth-section-name {
            font-weight:700;
            color:#1f1f1f;
        }
        .charth-kicker {
            color:#6D6E71;
            font-size:12px;
            letter-spacing:.08em;
            text-transform:uppercase;
            font-weight:700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def dashboard_page(user: dict) -> None:
    header("Dashboard Executivo", "Visão gerencial de performance das lojas CHARTH, sem plano de ação e sem bonificação.")
    df = filter_df_for_user(evaluations_df(), user)
    if df.empty:
        st.info("Ainda não existem avaliações salvas. Use o menu Nova Avaliação para registrar a primeira avaliação.")
        return

    df = df.copy()
    df["status_operacional"] = df["weighted_score"].apply(status_from_weighted)
    df["mes_referencia"] = df["evaluation_date"].dt.to_period("M").astype(str)

    st.markdown(
        """
        <style>
        .charth-dashboard-note {
            background:linear-gradient(135deg, #FFFDFC 0%, #F3E8E6 100%);
            border:1px solid rgba(201,160,160,.34);
            border-radius:20px;
            padding:18px 20px;
            margin:6px 0 18px 0;
            color:#343434;
            line-height:1.55;
            box-shadow:0 12px 28px rgba(31,31,31,.035);
        }
        .charth-chart-title {
            color:#1F1F1F;
            font-size:18px;
            font-weight:850;
            letter-spacing:.02em;
            margin:4px 0 10px 0;
        }
        .charth-insight-card {
            background:#fff;
            border:1px solid rgba(109,110,113,.16);
            border-radius:18px;
            padding:16px 18px;
            margin-bottom:12px;
            box-shadow:0 12px 28px rgba(31,31,31,.035);
        }
        .charth-insight-title {
            font-family:SIMPLO, "Inter", "Segoe UI", sans-serif;
            color:#1f1f1f;
            font-weight:850;
            font-size:15px;
            margin-bottom:6px;
        }
        .charth-insight-meta {
            color:#6D6E71;
            font-size:12px;
            letter-spacing:.06em;
            text-transform:uppercase;
            font-weight:800;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Filtros", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        available_stores = sorted(df["store"].dropna().unique().tolist()) or STORES
        available_months = sorted(df["mes_referencia"].dropna().unique().tolist())
        with c1:
            stores = st.multiselect("Loja", available_stores, default=available_stores)
        with c2:
            months = st.multiselect("Mês", available_months, default=available_months)
        with c3:
            min_date = df["evaluation_date"].min().date() if pd.notna(df["evaluation_date"].min()) else date.today()
            start = st.date_input("Data inicial", value=min_date)
        with c4:
            end = st.date_input("Data final", value=date.today())

    filtered = df[
        (df["store"].isin(stores))
        & (df["mes_referencia"].isin(months))
        & (df["evaluation_date"].dt.date >= start)
        & (df["evaluation_date"].dt.date <= end)
    ].copy()
    if filtered.empty:
        st.warning("Nenhuma avaliação encontrada para os filtros selecionados.")
        return

    latest = filtered.sort_values(["evaluation_date", "id"], ascending=[False, False]).drop_duplicates("store")
    critical_count = int((latest["status_operacional"] == "Plano de Ação Imediato").sum())
    attention_count = int((latest["status_operacional"] == "Loja em Atenção").sum())
    best_store = filtered.groupby("store")["weighted_score"].mean().idxmax()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Média geral", f"{filtered['weighted_score'].mean():.2f}", "Média ponderada oficial")
    with c2:
        metric_card("Avaliações", str(len(filtered)), "Total no período")
    with c3:
        metric_card("Melhor loja", best_store, "Maior média no recorte")
    with c4:
        metric_card("Lojas em atenção", str(attention_count + critical_count), "Atenção ou plano imediato")

    st.markdown(
        """
        <div class="charth-dashboard-note">
            <strong>Regra de status operacional:</strong>
            Excelência CHARTH ≥ 9, Loja Forte ≥ 8, Loja em Atenção ≥ 7 e Plano de Ação Imediato abaixo de 7.
            A bonificação foi removida deste painel e fica concentrada no menu <strong>Bonificação</strong>.
            As pendências ficam concentradas no menu <strong>Planos de Ação</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Visão geral", "Lojas", "Seções", "Evolução"])

    with tab1:
        left, right = st.columns([1.25, 1])
        with left:
            st.markdown("### Ranking de lojas")
            rank = filtered.groupby("store", as_index=False)["weighted_score"].mean().sort_values("weighted_score", ascending=False)
            rank["status_operacional"] = rank["weighted_score"].apply(status_from_weighted)
            fig = px.bar(rank, x="store", y="weighted_score", color="status_operacional", text="weighted_score", range_y=[0, 10], color_discrete_map=STATUS_COLOR_MAP)
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig.update_layout(template="plotly_white", xaxis_title="Loja", yaxis_title="Média ponderada", height=390, margin=dict(l=20,r=20,t=20,b=20), legend_title_text="Status")
            st.plotly_chart(fig, use_container_width=True)
        with right:
            st.markdown("### Status operacional")
            status_order = ["Excelência CHARTH", "Loja Forte", "Loja em Atenção", "Plano de Ação Imediato"]
            status_df = latest["status_operacional"].value_counts().reindex(status_order, fill_value=0).reset_index()
            status_df.columns = ["Status", "Quantidade"]
            fig_status = px.pie(status_df, names="Status", values="Quantidade", hole=.58, color="Status", color_discrete_map=STATUS_COLOR_MAP)
            fig_status.update_traces(textposition="inside", textinfo="percent+label")
            fig_status.update_layout(template="plotly_white", height=390, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
            st.plotly_chart(fig_status, use_container_width=True)

        st.markdown("### Última fotografia por loja")
        latest_table = latest[["store", "evaluation_date", "manager", "weighted_score", "status_operacional"]].copy()
        latest_table["evaluation_date"] = latest_table["evaluation_date"].dt.strftime("%d/%m/%Y")
        latest_table = latest_table.rename(columns={
            "store": "Loja",
            "evaluation_date": "Última avaliação",
            "manager": "Gerente",
            "weighted_score": "Média geral",
            "status_operacional": "Status operacional",
        }).sort_values("Média geral", ascending=False)
        st.dataframe(latest_table, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### Comparativo por loja")
        store_summary = filtered.groupby("store", as_index=False).agg(
            media_geral=("weighted_score", "mean"),
            avaliacoes=("id", "count"),
            ultima_avaliacao=("evaluation_date", "max"),
        )
        store_summary["status_medio"] = store_summary["media_geral"].apply(status_from_weighted)
        store_summary["ultima_avaliacao"] = store_summary["ultima_avaliacao"].dt.strftime("%d/%m/%Y")
        fig_store = px.scatter(
            store_summary,
            x="avaliacoes",
            y="media_geral",
            size="avaliacoes",
            color="status_medio",
            text="store",
            range_y=[0,10],
            labels={"avaliacoes":"Quantidade de avaliações", "media_geral":"Média geral", "status_medio":"Status"},
            color_discrete_map=STATUS_COLOR_MAP,
        )
        fig_store.update_traces(textposition="top center")
        fig_store.update_layout(template="plotly_white", height=430, margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_store, use_container_width=True)

        store_table = store_summary.rename(columns={
            "store": "Loja",
            "media_geral": "Média geral",
            "avaliacoes": "Avaliações",
            "ultima_avaliacao": "Última avaliação",
            "status_medio": "Status médio",
        }).sort_values("Média geral", ascending=False)
        st.dataframe(store_table, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("### Médias por seção")
        rows = []
        for _, row in filtered.iterrows():
            scores = row.get("section_scores_json") if isinstance(row.get("section_scores_json"), dict) else {}
            for section in SECTION_LABELS:
                if section in scores:
                    rows.append({"Loja": row["store"], "Seção": section, "Média": float(scores.get(section) or 0)})
        section_long = pd.DataFrame(rows)
        if section_long.empty:
            st.caption("Sem médias por seção para exibir.")
        else:
            sec_overall = section_long.groupby("Seção", as_index=False)["Média"].mean().sort_values("Média", ascending=True)
            sec_overall["Status"] = sec_overall["Média"].apply(status_from_weighted)
            fig_sec = px.bar(sec_overall, x="Média", y="Seção", orientation="h", color="Status", text="Média", range_x=[0, 10], color_discrete_map=STATUS_COLOR_MAP)
            fig_sec.update_traces(texttemplate="%{text:.2f}")
            fig_sec.update_layout(template="plotly_white", height=520, yaxis_title="", xaxis_title="Média", margin=dict(l=20,r=20,t=20,b=20))
            st.plotly_chart(fig_sec, use_container_width=True)

            st.markdown("### Mapa de calor · loja x seção")
            heat = section_long.groupby(["Loja", "Seção"], as_index=False)["Média"].mean()
            pivot = heat.pivot(index="Loja", columns="Seção", values="Média").reindex(columns=SECTION_LABELS)
            fig_heat = px.imshow(
                pivot,
                text_auto=".1f",
                aspect="auto",
                zmin=0,
                zmax=10,
                color_continuous_scale=SECTION_COLOR_SCALE,
            )
            fig_heat.update_layout(template="plotly_white", height=420, xaxis_title="Seção", yaxis_title="Loja", margin=dict(l=20,r=20,t=20,b=20))
            st.plotly_chart(fig_heat, use_container_width=True)

            st.markdown("### Pontos de atenção executivos")
            worst = section_long.groupby(["Loja", "Seção"], as_index=False)["Média"].mean().sort_values("Média", ascending=True).head(6)
            cols = st.columns(3)
            for i, item in worst.iterrows():
                with cols[i % 3]:
                    st.markdown(
                        f"""
                        <div class="charth-insight-card">
                            <div class="charth-insight-meta">{item['Loja']}</div>
                            <div class="charth-insight-title">{item['Seção']}</div>
                            <div>{_score_badge(float(item['Média']))}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with tab4:
        st.markdown("### Evolução da média ponderada")
        line_df = filtered.sort_values("evaluation_date")
        fig_line = px.line(line_df, x="evaluation_date", y="weighted_score", color="store", markers=True, color_discrete_sequence=STORE_SEQUENCE)
        fig_line.add_hline(y=9, line_dash="dot", line_color="#C9A0A0", annotation_text="Excelência CHARTH")
        fig_line.add_hline(y=8, line_dash="dot", line_color="#6D6E71", annotation_text="Loja Forte")
        fig_line.add_hline(y=7, line_dash="dot", line_color="#B8875D", annotation_text="Loja em Atenção")
        fig_line.update_layout(template="plotly_white", yaxis_range=[0, 10], xaxis_title="Data", yaxis_title="Média ponderada", height=430, margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("### Evolução mensal por loja")
        monthly = filtered.groupby(["mes_referencia", "store"], as_index=False)["weighted_score"].mean()
        fig_month = px.bar(monthly, x="mes_referencia", y="weighted_score", color="store", barmode="group", text="weighted_score", range_y=[0,10], color_discrete_sequence=STORE_SEQUENCE)
        fig_month.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_month.update_layout(template="plotly_white", xaxis_title="Mês", yaxis_title="Média", height=420, margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("## Exportação")
    flat = export_flattened_evaluations(filtered)
    st.download_button(
        "Baixar avaliações filtradas em CSV",
        data=flat.to_csv(index=False).encode("utf-8-sig"),
        file_name="avaliacoes_charth_dashboard.csv",
        mime="text/csv",
        use_container_width=True,
    )

def history_page(user: dict) -> None:
    _render_history_css()
    header("Histórico de Avaliações", "Consulta executiva das avaliações salvas, com médias, pontos estratégicos e observações.")
    df = filter_df_for_user(evaluations_df(), user)
    if df.empty:
        st.info("Ainda não existem avaliações salvas.")
        return

    c1, c2 = st.columns([2, 1])
    with c1:
        store = st.selectbox("Loja", ["Todas"] + sorted(df["store"].unique().tolist()))
    with c2:
        ordenar = st.selectbox("Ordenar por", ["Mais recentes", "Melhor média", "Menor média"])

    if store != "Todas":
        df = df[df["store"] == store]
    if ordenar == "Melhor média":
        df = df.sort_values("weighted_score", ascending=False)
    elif ordenar == "Menor média":
        df = df.sort_values("weighted_score", ascending=True)
    else:
        df = df.sort_values(["evaluation_date", "id"], ascending=[False, False])

    st.markdown("### Resumo das avaliações")
    summary = df[["id", "evaluation_date", "store", "supervisor", "manager", "weighted_score", "overall_status", "bonus_level", "manager_bonus"]].rename(
        columns={
            "id": "ID",
            "evaluation_date": "Data",
            "store": "Loja",
            "supervisor": "Supervisora",
            "manager": "Gerente",
            "weighted_score": "Média",
            "overall_status": "Status",
            "bonus_level": "Bônus",
            "manager_bonus": "Valor gerente",
        }
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)

    selected = st.selectbox("Abrir avaliação", df["id"].tolist(), format_func=lambda x: f"Avaliação #{x}")
    row = df[df["id"] == selected].iloc[0]

    st.markdown(f"## Avaliação #{selected} · {row['store']}")
    date_text = row["evaluation_date"].date().strftime("%d/%m/%Y") if pd.notna(row["evaluation_date"]) else "Sem data"
    st.markdown(
        f"""
        <div class="charth-history-card" style="border-left:4px solid #1F1F1F;">
            <div class="charth-kicker">Identificação</div>
            <div class="charth-history-card-body">
                <strong>Data:</strong> {date_text} &nbsp; | &nbsp;
                <strong>Gerente:</strong> {row['manager']} &nbsp; | &nbsp;
                <strong>Supervisora:</strong> {row['supervisor']}<br>
                <strong>Média ponderada:</strong> {row['weighted_score']:.2f} &nbsp; | &nbsp;
                <strong>Status:</strong> {row['overall_status']} &nbsp; | &nbsp;
                <strong>Bônus:</strong> {row['bonus_level']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_scores = _safe_dict(row["section_scores_json"])
    strategic = _safe_dict(row["strategic_json"])
    observations = _safe_dict(row["observations_json"])

    tab1, tab2, tab3 = st.tabs(["Médias por seção", "Perguntas estratégicas", "Observações"])

    with tab1:
        st.markdown("### Médias por seção")
        if section_scores:
            for section_name in SECTION_LABELS:
                if section_name in section_scores:
                    score = float(section_scores.get(section_name) or 0)
                    st.markdown(
                        f"""
                        <div class="charth-section-row">
                            <div class="charth-section-name">{section_name}</div>
                            <div>{_score_badge(score)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.caption("Sem médias por seção registradas.")

    with tab2:
        st.markdown("### Perguntas estratégicas")
        for key, label in STRATEGIC_LABELS.items():
            _render_text_card(label, strategic.get(key, ""), accent="#C9A0A0")

    with tab3:
        st.markdown("### Observações por bloco")
        for key, label in OBSERVATION_LABELS.items():
            _render_text_card(label, observations.get(key, ""), accent="#9FA0A3")

    if user.get("role") == ROLE_ADMIN:
        st.markdown("---")
        with st.expander("Área Admin · Excluir avaliação", expanded=False):
            st.warning("Esta ação remove a avaliação selecionada e todos os planos de ação vinculados a ela. Use apenas para corrigir lançamentos indevidos.")
            confirmar = st.checkbox(f"Confirmo que desejo excluir a avaliação #{selected}", key=f"confirm_delete_eval_{selected}")
            if st.button("Excluir avaliação selecionada", type="secondary", use_container_width=True, disabled=not confirmar, key=f"delete_eval_{selected}"):
                delete_evaluation(int(selected))
                st.success(f"Avaliação #{selected} excluída com sucesso.")
                st.rerun()


def _format_date_br(value) -> str:
    if pd.isna(value):
        return "Sem prazo"
    try:
        return value.date().strftime("%d/%m/%Y")
    except AttributeError:
        try:
            return pd.to_datetime(value).date().strftime("%d/%m/%Y")
        except Exception:
            return str(value)


def _priority_badge(priority: str) -> str:
    mapping = {
        "Alta": ("Alta", "#9E3F45"),
        "Média": ("Média", "#B8875D"),
        "Baixa": ("Baixa", "#B8A76A"),
        "Monitoramento": ("Monitoramento", "#6D6E71"),
    }
    label, color = mapping.get(str(priority), (str(priority), "#6D6E71"))
    return f"""
    <span style="display:inline-block;padding:5px 10px;border-radius:999px;background:{color};color:#fff;font-size:12px;font-weight:800;letter-spacing:.04em;">
        {label}
    </span>
    """


def _status_badge(status: str) -> str:
    color = {
        "Aberto": "#9E3F45",
        "Em andamento": "#B8875D",
        "Concluído": "#6D6E71",
        "Cancelado": "#9FA0A3",
    }.get(str(status), "#6D6E71")
    return f"""
    <span style="display:inline-block;padding:5px 10px;border-radius:999px;background:{color};color:#fff;font-size:12px;font-weight:800;letter-spacing:.04em;">
        {status}
    </span>
    """


def _render_action_css() -> None:
    st.markdown(
        """
        <style>
        .charth-action-card {
            background:#fff;
            border:1px solid rgba(109,110,113,.16);
            border-radius:18px;
            padding:18px 20px;
            margin-bottom:14px;
            box-shadow:0 12px 28px rgba(31,31,31,.035);
        }
        .charth-action-top {
            display:flex;
            justify-content:space-between;
            gap:16px;
            align-items:flex-start;
            margin-bottom:12px;
        }
        .charth-action-title {
            font-family:SIMPLO, "Inter", "Segoe UI", sans-serif;
            font-size:16px;
            font-weight:850;
            color:#1f1f1f;
            margin-bottom:4px;
        }
        .charth-action-subtitle {
            font-size:12px;
            color:#6D6E71;
            letter-spacing:.08em;
            text-transform:uppercase;
            font-weight:800;
        }
        .charth-action-question {
            font-size:15px;
            line-height:1.55;
            color:#2d2d2d;
            margin:10px 0 12px 0;
        }
        .charth-action-meta {
            display:grid;
            grid-template-columns:repeat(4, minmax(0,1fr));
            gap:10px;
            margin-top:12px;
        }
        .charth-action-meta div {
            background:#F7F4F2;
            border-radius:12px;
            padding:10px 12px;
            font-size:13px;
            color:#1f1f1f;
        }
        .charth-action-meta span {
            display:block;
            color:#6D6E71;
            font-size:11px;
            letter-spacing:.08em;
            text-transform:uppercase;
            font-weight:800;
            margin-bottom:3px;
        }
        .charth-rule-card {
            background:linear-gradient(135deg, #F7F4F2 0%, #FFF 100%);
            border:1px solid rgba(201,160,160,.35);
            border-radius:18px;
            padding:16px 18px;
            margin-bottom:16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_action_card(row: pd.Series) -> None:
    score = float(row.get("score") or 0)
    deadline = row.get("deadline")
    overdue = pd.notna(deadline) and deadline.date() < date.today() and row.get("status") != "Concluído"
    overdue_text = " · Vencido" if overdue else ""
    overdue_color = "#9E3F45" if overdue else "#6D6E71"
    st.markdown(
        f"""
        <div class="charth-action-card">
            <div class="charth-action-top">
                <div>
                    <div class="charth-action-subtitle">Plano #{int(row['id'])} · {row.get('store','')}</div>
                    <div class="charth-action-title">{row.get('section','')}</div>
                </div>
                <div>{_priority_badge(row.get('priority',''))} &nbsp; {_status_badge(row.get('status',''))}</div>
            </div>
            <div class="charth-action-question"><strong>Ponto a corrigir:</strong> {row.get('question_label','')}</div>
            <div>{_score_badge(score)}</div>
            <div class="charth-action-meta">
                <div><span>Responsável</span>{row.get('responsible') or 'Não definido'}</div>
                <div><span>Prazo</span><span style="display:inline;color:{overdue_color};font-size:13px;text-transform:none;letter-spacing:0;font-weight:700;">{_format_date_br(deadline)}{overdue_text}</span></div>
                <div><span>Prioridade</span>{row.get('priority','')}</div>
                <div><span>Status</span>{row.get('status','')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def action_plans_page(user: dict) -> None:
    from .db import update_action_plan

    _render_history_css()
    _render_action_css()
    header("Planos de Ação", "Acompanhamento executivo das pendências geradas por notas abaixo do padrão.")

    st.markdown(
        """
        <div class="charth-rule-card">
            <div class="charth-kicker">Regra de status operacional da loja</div>
            <div class="charth-history-card-body">
                <strong>Excelência CHARTH</strong>: média geral ≥ 9 &nbsp; | &nbsp;
                <strong>Loja Forte</strong>: média geral ≥ 8 &nbsp; | &nbsp;
                <strong>Loja em Atenção</strong>: média geral ≥ 7 &nbsp; | &nbsp;
                <strong>Plano de Ação Imediato</strong>: média geral abaixo de 7.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    evaluations = filter_df_for_user(evaluations_df(), user)
    if not evaluations.empty:
        latest = evaluations.sort_values(["evaluation_date", "id"], ascending=[False, False]).drop_duplicates("store")
        latest = latest[["store", "evaluation_date", "weighted_score"]].copy()
        latest["status_operacional"] = latest["weighted_score"].apply(status_from_weighted)
        latest["evaluation_date"] = latest["evaluation_date"].dt.strftime("%d/%m/%Y")
        st.markdown("### Status operacional mais recente por loja")
        st.dataframe(
            latest.rename(columns={
                "store": "Loja",
                "evaluation_date": "Última avaliação",
                "weighted_score": "Média geral",
                "status_operacional": "Status operacional",
            }),
            use_container_width=True,
            hide_index=True,
        )

    plans = action_plans_df()
    if plans.empty:
        st.info("Nenhum plano de ação gerado até o momento.")
        return
    if user.get("role") == ROLE_GESTORA and not GESTORA_CAN_VIEW_ALL_STORES:
        plans = plans[plans["store"] == user.get("store")]
    if plans.empty:
        st.info("Não há planos de ação para o seu perfil de acesso.")
        return

    with st.expander("Filtros", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            stores = st.multiselect("Loja", sorted(plans["store"].dropna().unique().tolist()), default=sorted(plans["store"].dropna().unique().tolist()))
        with c2:
            statuses = st.multiselect("Status", ["Aberto", "Em andamento", "Concluído", "Cancelado"], default=["Aberto", "Em andamento"])
        with c3:
            priorities = st.multiselect("Prioridade", ["Alta", "Média", "Baixa", "Monitoramento"], default=["Alta", "Média", "Baixa", "Monitoramento"])

    filtered = plans[plans["store"].isin(stores) & plans["status"].isin(statuses) & plans["priority"].isin(priorities)].copy()
    if filtered.empty:
        st.warning("Nenhum plano encontrado para os filtros selecionados.")
        return

    today = pd.Timestamp(date.today())
    open_mask = filtered["status"] != "Concluído"
    overdue_mask = open_mask & filtered["deadline"].notna() & (filtered["deadline"] < today)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Planos filtrados", str(len(filtered)), "Total no recorte")
    with c2:
        metric_card("Em aberto", str(int(open_mask.sum())), "Aberto ou em andamento")
    with c3:
        metric_card("Prioridade alta", str(int((filtered["priority"] == "Alta").sum())), "Demandas críticas")
    with c4:
        metric_card("Vencidos", str(int(overdue_mask.sum())), "Prazo anterior a hoje")

    st.markdown("### Planos de ação")
    sort_order = {"Alta": 0, "Média": 1, "Baixa": 2, "Monitoramento": 3}
    filtered["_priority_order"] = filtered["priority"].map(sort_order).fillna(9)
    filtered = filtered.sort_values(["_priority_order", "deadline", "id"], ascending=[True, True, False])
    for _, row in filtered.iterrows():
        _render_action_card(row)

    st.markdown("### Tabela para exportação")
    table = filtered[["id", "store", "section", "question_label", "score", "priority", "responsible", "deadline", "status", "notes"]].copy()
    table["deadline"] = table["deadline"].apply(_format_date_br)
    table = table.rename(columns={
        "id": "ID",
        "store": "Loja",
        "section": "Seção",
        "question_label": "Ponto de atenção",
        "score": "Nota",
        "priority": "Prioridade",
        "responsible": "Responsável",
        "deadline": "Prazo",
        "status": "Status",
        "notes": "Observações",
    })
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button(
        "Baixar planos filtrados em CSV",
        data=table.to_csv(index=False).encode("utf-8-sig"),
        file_name="planos_de_acao_charth.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if user.get("role") == ROLE_GESTORA:
        st.caption("Gestoras visualizam os planos, mas não alteram status nesta versão.")
        return

    st.markdown("### Atualizar plano")
    plan_id = st.selectbox(
        "Plano de ação",
        filtered["id"].tolist(),
        format_func=lambda x: f"Plano #{x} · {filtered[filtered['id'] == x].iloc[0]['store']} · {filtered[filtered['id'] == x].iloc[0]['section']}",
    )
    selected = filtered[filtered["id"] == plan_id].iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        status_options = ["Aberto", "Em andamento", "Concluído", "Cancelado"]
        status = st.selectbox("Status", status_options, index=status_options.index(selected["status"]) if selected["status"] in status_options else 0)
    with c2:
        responsible = st.text_input("Responsável", value=selected.get("responsible") or "")
    with c3:
        deadline = st.date_input("Prazo", value=selected["deadline"].date() if pd.notna(selected["deadline"]) else date.today())
    notes = st.text_area("Observações do plano", value=selected.get("notes") or "")
    if st.button("Salvar atualização do plano", use_container_width=True):
        update_action_plan(int(plan_id), status, responsible, deadline.isoformat(), notes)
        st.success("Plano atualizado com sucesso.")
        st.rerun()
