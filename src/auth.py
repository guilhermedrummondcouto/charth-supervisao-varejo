from __future__ import annotations
import hashlib
import streamlit as st
from .config import ROLE_ADMIN, ROLE_SUPERVISORA
from .db import get_user_by_username


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def login_box() -> bool:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">CHARTH</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Supervisão de Varejo</div>', unsafe_allow_html=True)
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    clicked = st.button("Entrar", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if clicked:
        user = get_user_by_username(username.strip())
        if user and verify_password(password, user["password_hash"]):
            st.session_state.user = {
                "username": user["username"],
                "role": user["role"],
                "store": user.get("store"),
                "name": user.get("name") or user["username"],
            }
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    return False


def require_login(_conn=None) -> dict:
    if "user" not in st.session_state:
        login_box()
        st.stop()
    return st.session_state.user


def can_edit(user: dict) -> bool:
    return user.get("role") in {ROLE_ADMIN, ROLE_SUPERVISORA}


def can_admin(user: dict) -> bool:
    return user.get("role") == ROLE_ADMIN


def logout_button() -> None:
    if st.sidebar.button("Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()
