from __future__ import annotations
import streamlit as st
from src.auth import can_admin, can_edit, logout_button, require_login
from src.config import APP_NAME
from src.dashboard import action_plans_page, dashboard_page, history_page
from src.db import backup_database, init_db, list_users_df, update_user_password, database_mode_label
from src.forms import render_evaluation_form
from src.ui import apply_brand_css
from src.bonus import bonus_page

st.set_page_config(page_title=APP_NAME, page_icon="◆", layout="wide")
apply_brand_css()
init_db()
user = require_login()

st.sidebar.markdown("# CHARTH")
st.sidebar.caption(f"Usuário: {user['name']} · Perfil: {user['role']}")
st.sidebar.caption(f"Banco: {database_mode_label()}")
logout_button()

if can_edit(user):
    pages = ["Dashboard", "Nova Avaliação", "Histórico", "Planos de Ação", "Bonificação", "Configurações"]
else:
    pages = ["Dashboard", "Histórico", "Planos de Ação", "Bonificação"]

page = st.sidebar.radio("Menu", pages)

if page == "Dashboard":
    dashboard_page(user)
elif page == "Nova Avaliação":
    render_evaluation_form(user)
elif page == "Histórico":
    history_page(user)
elif page == "Planos de Ação":
    action_plans_page(user)
elif page == "Bonificação":
    bonus_page(user)
elif page == "Configurações":
    st.markdown("# Configurações")
    st.info("As principais regras configuráveis estão no arquivo `src/config.py`: pesos, bonificação, lojas, perfis e permissão das gestoras.")

    st.markdown("## Segurança e senhas")
    st.caption("Use esta área para trocar sua própria senha. Administradores também conseguem redefinir a senha das gestoras e demais usuários.")

    with st.container(border=True):
        st.markdown("### Alterar minha senha")
        nova_senha = st.text_input("Nova senha", type="password", key="own_new_password")
        confirmar_senha = st.text_input("Confirmar nova senha", type="password", key="own_confirm_password")
        if st.button("Salvar minha nova senha", use_container_width=True):
            if not nova_senha or not confirmar_senha:
                st.warning("Preencha e confirme a nova senha.")
            elif nova_senha != confirmar_senha:
                st.error("As senhas não conferem.")
            else:
                try:
                    update_user_password(user["username"], nova_senha)
                    st.success("Senha alterada com sucesso. No próximo acesso, use a nova senha.")
                except ValueError as exc:
                    st.error(str(exc))

    if can_admin(user):
        st.markdown("## Gerenciar senhas das lojas")
        usuarios_df = list_users_df()
        if usuarios_df.empty:
            st.warning("Nenhum usuário cadastrado.")
        else:
            st.dataframe(usuarios_df[["username", "name", "role", "store", "active"]], use_container_width=True, hide_index=True)
            opcoes = usuarios_df["username"].tolist()
            usuario_escolhido = st.selectbox("Usuário para redefinir senha", opcoes)
            usuario_info = usuarios_df[usuarios_df["username"] == usuario_escolhido].iloc[0].to_dict()
            st.caption(f"Perfil: {usuario_info.get('role', '')} · Loja: {usuario_info.get('store') or 'Todas'}")
            senha_usuario = st.text_input("Nova senha do usuário selecionado", type="password", key="managed_new_password")
            confirmar_usuario = st.text_input("Confirmar senha do usuário selecionado", type="password", key="managed_confirm_password")
            if st.button("Redefinir senha do usuário", use_container_width=True):
                if not senha_usuario or not confirmar_usuario:
                    st.warning("Preencha e confirme a nova senha do usuário.")
                elif senha_usuario != confirmar_usuario:
                    st.error("As senhas não conferem.")
                else:
                    try:
                        update_user_password(usuario_escolhido, senha_usuario)
                        st.success(f"Senha de {usuario_escolhido} alterada com sucesso.")
                    except ValueError as exc:
                        st.error(str(exc))
    else:
        st.caption("Somente o perfil Admin pode redefinir senhas de outras usuárias.")

    st.markdown("## Backup")
    if st.button("Gerar backup local do banco", use_container_width=True):
        path = backup_database()
        if path:
            st.success(f"Backup criado em: {path}")
        else:
            st.warning("Backup local só se aplica ao SQLite. No Supabase, use o backup/exportação do próprio Supabase ou exporte CSV pelo dashboard.")

    st.markdown("## Pontos importantes")
    st.write("Gestoras não conseguem criar avaliações. Elas acessam Dashboard, Histórico, Planos de Ação e Bonificação.")
    st.write("Se `DATABASE_URL` estiver configurado em secrets, o app usa Supabase/PostgreSQL. Sem `DATABASE_URL`, usa SQLite local.")
