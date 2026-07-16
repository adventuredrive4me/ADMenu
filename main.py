import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime

# --- PERMANENT DATABASE & STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'active_view' not in st.session_state:
    st.session_state.active_view = "Dashboard"  # Controls bottom button view routing
if 'trips' not in st.session_state:
    st.session_state.trips = {
        "Canyon Odyssey": {
            "start": datetime(2026, 10, 26, 0, 0),
            "end": datetime(2026, 11, 2, 0, 0),
            "days": 8, "nights": 7,
            "currency": "NPR - Nepalese Rupee", "exchange_rate": 0.60,
            "stops": [
                {
                    "id": "stop_1", "day": "Day 2", "meal": "Lunch", "time": "02:00 pm",
                    "name": "Anapurna Coffee Shop & Bakery", "phone": "+9779851110571",
                    "email": "ygauchan@gmail.com", "is_live": True, "live_start_time": time.time() - 1500,
                    "menu": [
                        {"name": "Vegetable Noodle Soup", "course": "Soup", "unit": "Plate", "ratio": 1.0, "price": 400.0, "billing": "Payable/Admin Account", "display": True, "sort": 1}
                    ]
                },
                {
                    "id": "stop_2", "day": "Day 2", "meal": "Dinner", "time": "08:00 pm",
                    "name": "Hotel Grand Shambala", "phone": "+9779851187371",
                    "email": "hotelgrandshambala@gmail.com", "is_live": False, "live_start_time": None,
                    "menu": []
                }
            ]
        }
    }
if 'guests' not in st.session_state:
    st.session_state.guests = [
        {"name": "Raju", "id": "9", "submitted": True, "choices": {"Vegetable Noodle Soup": 1}},
        {"name": "Sanjay", "id": "4", "submitted": False, "choices": {}},
        {"name": "Tom", "id": "3", "submitted": False, "choices": {}},
        {"name": "Raj", "id": "2", "submitted": False, "choices": {}},
        {"name": "Tintin", "id": "8", "submitted": False, "choices": {}},
        {"name": "Doctor", "id": "10", "submitted": False, "choices": {}},
        {"name": "Sonal", "id": "6", "submitted": False, "choices": {}},
        {"name": "Ranjana Choudhury", "id": "11", "submitted": False, "choices": {}},
        {"name": "Amol", "id": "12", "submitted": False, "choices": {}},
        {"name": "Joydeb", "id": "14", "submitted": False, "choices": {}}
    ]

st.set_page_config(page_title="ADMenu App Engine", layout="centered")

# --- GLOBAL STYLING INJECTION FOR APP ALIGNMENT ---
st.markdown("""
<style>
    .stButton > button { width: 100%; border-radius: 8px; }
    div[data-testid="stExpander"] { border: 1px solid #e6e6e6; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- SECURITY GATEKEEPER ---
if not st.session_state.logged_in:
    st.title("📱 ADMenu Security Gateway")
    with st.container(border=True):
        u = st.text_input("Username", value="admin")
        p = st.text_input("Password", type="password", value="admin")
        if st.button("Unlock Terminal Platform", type="primary"):
            if u == "admin" and p == "admin":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Access denied.")
    st.stop()

# --- BACK TO DASHBOARD NAVIGATION LINK ---
if st.session_state.active_view != "Dashboard":
    if st.button("⬅️ Return to Main Live Dashboard"):
        st.session_state.active_view = "Dashboard"
        st.rerun()

# =========================================================================
# 📺 VIEW INTERFACE 1: THE LIVE GO-DASHBOARD (MAIN VIEW)
# =========================================================================
if st.session_state.active_view == "Dashboard":
    st.title("📱 ADMenu Dashboard")
    
    # Active Trip Identifier Header
    active_trip_name = list(st.session_state.trips.keys())[0]
    trip_ref = st.session_state.trips[active_trip_name]
    
    with st.container(border=True):
        st.subheader(active_trip_name)
        st.caption(f"🗓️ Calendar Parameters: {trip_ref['start'].strftime('%d %b')} → {trip_ref['end'].strftime('%d %b %Y')}")

    st.markdown("### 🛜 LIVE GO-DASHBOARD")
    
    # Render Timeline Stops with Live Toggles
    for s in trip_ref["stops"]:
        if s["is_live"]:
            # Green Live Alert Container Card
            st.markdown(f"<div style='border: 2px solid #28a745; background-color: #f8fff9; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
            col_l1, col_l2 = st.columns([3, 1])
            col_l1.markdown(f"🍔 **{s['name']}** &nbsp; <span style='background-color:#28a745; color:white; padding:2px 6px; border-radius:4px; font-size:0.8em;'>LIVE</span>", unsafe_allow_html=True)
            
            if col_l2.button("Stop Live", key=f"stop_{s['id']}"):
                s["is_live"] = False
                s["live_start_time"] = None
                st.rerun()
                
            st.caption(f"{s['meal']} · {s['day']} · {s['time']}")
            
            # Live Countdown Clock Math
            if s["live_start_time"]:
                elapsed = int(time.time() - s["live_start_time"])
                m, s_sec = divmod(elapsed, 60)
                st.markdown(f"⏱️ **Active ordering duration window:** {m}m {s_sec}s")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Standard Grey Idle Card
            with st.container(border=True):
                col_i1, col_i2 = st.columns([3, 1])
                col_i1.markdown(f"🏨 **{s['name']}**")
                col_i1.caption(f"{s['meal']} · {s['day']} · {s['time']}")
                if col_i2.button("Share as Live", key=f"start_{s['id']}", type="secondary"):
                    s["is_live"] = True
                    s["live_start_time"] = time.time()
                    st.rerun()

    # Real-Time Guest Submission Status Grid
    st.markdown("##### Tracking (1/10 submitted)")
    for g in st.session_state.guests:
        with st.container(border=True):
            cg1, cg2, cg3 = st.columns([2, 1, 1])
            cg1.markdown(f"👤 **{g['name']}**<br><span style='font-size:0.8em; color:gray;'>ID: {g['id']}</span>", unsafe_allow_html=True)
            
            if g["submitted"]:
                cg2.markdown("<span style='background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:4px; font-size:0.9em;'>✅ Submitted</span>", unsafe_allow_html=True)
                if cg3.button("Allow changes", key=f"chg_{g['id']}"):
                    g["submitted"] = False
                    st.rerun()
            else:
                cg2.markdown("<span style='background-color:#fff3cd; color:#856404; padding:6px 12px; border-radius:4px; font-size:0.9em;'>⏳ Pending</span>", unsafe_allow_html=True)
                if cg3.button("🔔 Ping", key=f"png_{g['id']}"):
                    st.toast(f"Notification alert dispatched to {g['name']}!")

    # --- THE CENTRAL GRID ACTION CONTROLLER KEYPAD ---
    st.markdown("### 🛠️ ADMIN TOOLS")
    b_col1, b_col2 = st.columns(2)
    
    if b_col1.button("📖 Trip Setup", type="secondary"):
        st.session_state.active_view = "Trip Setup"
        st.rerun()
    if b_col2.button("🍳 Menu Builder", type="secondary"):
        st.session_state.active_view = "Menu Builder"
        st.rerun()
        
    b_col3, b_col4 = st.columns(2)
    if b_col3.button("👥 Guest List", type="secondary"):
        st.session_state.active_view = "Guest List"
        st.rerun()
    if b_col4.button("📊 Consolidation & Export", type="secondary"):
        st.session_state.active_view = "Consolidation & Export"
        st.rerun()
        
    if st.button("💵 Ledger & B&L Accounts Summary", type="secondary"):
        st.session_state.active_view = "Ledger"
        st.rerun()

# =========================================================================
# 🛠️ VIEW INTERFACE 2: TRIP SETUP MODAL
# =========================================================================
elif st.session_state.active_view == "Trip Setup":
    st.header("📖 Trip Setup & Parameters")
    
    with st.form("master_setup_form"):
        t_name = st.text_input("Trip Designation Name", value="Canyon Odyssey")
        sd = st.date_input("Start Date Profile")
        st_time = st.time_input("Start Departure Time")
        ed = st.date_input("End Date Profile")
        et_time = st.time_input("End Return Time")
        
        st.markdown("##### 💱 Currency Profile Tracker")
        t_curr = st.selectbox("Operational Region Currency Alignment", ["NPR - Nepalese Rupee", "INR - Indian Rupee", "USD - US Dollar"])
        ex_rate = st.number_input("Exchange Multiplier (1 Local Unit = ? INR)", min_value=0.01, value=0.60)
        
        if st.form_submit_button("Update Trip Details"):
            st.session_state.trips[t_name] = {
                "start": datetime.combine(sd, st_time), "end": datetime.combine(ed, et_time),
                "days": 8, "nights": 7, "currency": t_curr, "exchange_rate": ex_rate,
                "stops": st.session_state.trips["Canyon Odyssey"]["stops"]
            }
            st.success("Trip properties synchronized successfully!")

# =========================================================================
# 🛠️ VIEW INTERFACE 3: MENU BUILDER MODULE
# =========================================================================
elif st.session_state.active_view == "Menu Builder":
    st.header("🍳 Menu Item Builder Architecture")
    
    trip_ref = st.session_state.trips[list(st.session_state.trips.keys())[0]]
    stop_names = [s["name"] for s in trip_ref["stops"]]
    target_stop_name = st.selectbox("Assign Food Item To Location Stop", stop_names)
    target_stop = next(s for s in trip_ref["stops"] if s["name"] == target_stop_name)
    
    with st.form("add_food_item_form", clear_on_submit=True):
