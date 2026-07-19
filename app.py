# ==========================================================
# ADMENU
# Expedition Meal Management
#
# Main Application
# Version : 0.3
# ==========================================================

import streamlit as st

from config import (
    APP_NAME,
    APP_VERSION,
    COMPANY_NAME,
    LOGIN_USERNAME,
    LOGIN_PASSWORD
)

from database import initialize_database


# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🍽️",
    layout="wide"
)


# ----------------------------------------------------------
# Create Database (Runs only once)
# ----------------------------------------------------------

initialize_database()


# ----------------------------------------------------------
# Session State
# ----------------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"


# ----------------------------------------------------------
# Login Screen
# ----------------------------------------------------------

def login_screen():

    st.markdown("# 🍽️ ADMenu")
    st.markdown("### Smart Expedition Meal Management")
    st.divider()

    with st.container(border=True):

        st.subheader("Administrator Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if (
                username == LOGIN_USERNAME
                and
                password == LOGIN_PASSWORD
            ):

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("Invalid username or password.")

    st.caption(
        f"{COMPANY_NAME} • Version {APP_VERSION}"
    )


# ----------------------------------------------------------
# Dashboard
# ----------------------------------------------------------

def dashboard():

    st.title("🏠 Dashboard")

    st.success("Welcome to ADMenu")

    st.write(
        "Your Expedition Meal Management System is ready."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🧳 Trip Setup",
            use_container_width=True
        ):
            st.info("Coming in next milestone.")

        if st.button(
            "🍽 Menu Builder",
            use_container_width=True
        ):
            st.info("Coming in next milestone.")

        if st.button(
            "👥 Guest List",
            use_container_width=True
        ):
            st.info("Coming in next milestone.")

    with col2:

        if st.button(
            "📡 LIVE Ordering",
            use_container_width=True
        ):
            st.info("Coming soon.")

        if st.button(
            "📊 Review Orders",
            use_container_width=True
        ):
            st.info("Coming soon.")

        if st.button(
            "💰 Ledger",
            use_container_width=True
        ):
            st.info("Coming soon.")

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.rerun()


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

if st.session_state.logged_in:

    dashboard()

else:

    login_screen()
