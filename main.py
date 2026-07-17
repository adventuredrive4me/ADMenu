import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime

# =========================================================================
# SYSTEM CORE: PERMANENT DATABASE STATE SETUPS
# =========================================================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'active_view' not in st.session_state:
    st.session_state.active_view = "Dashboard"
if 'trips' not in st.session_state:
    st.session_state.trips = {
        "Canyon Odyssey": {
            "start": datetime(2026, 10, 26, 0, 0),
            "end": datetime(2026, 11, 2, 0, 0),
            "days": 8, "nights": 7,
            "currency": "NPR - Nepalese Rupee", "exchange_rate": 0.60,
            "stops": [
                {
                    "id": "stop_1", "day": "Day 2", "meal": "Lunch", "time": "02:00 pm", "date_str": "27 Oct",
                    "name": "Anapurna Coffee Shop & Bakery", "phone": "+9779851110571",
                    "email": "ygauchan@gmail.com", "is_live": False, "live_start_time": None,
                    "menu": [
                        {"name": "Vegetable Noodle Soup", "course": "Soup", "unit": "Plate", "ratio": 1.0, "price": 400.0, "billing": "Payable/Admin Account", "display": True, "sort": 1}
                    ]
                },
                {
                    "id": "stop_2", "day": "Day 2", "meal": "Dinner", "time": "08:00 pm", "date_str": "27 Oct",
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

st.set_page_config(page_title="ADMenu App Engine Pro", layout="centered")

# =========================================================================
# GLOBAL STYLE SHEET INJECTIONS FOR RESPONSIVE UI LAYOUTS
# =========================================================================
st.markdown("""
<style>
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    .blinking-live-tag {
        background-color: #28a745;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: bold;
        animation: blink 1.2s infinite;
        display: inline-block;
    }
    
    /* Administrative Central Control Keypad Styles */
    div.stButton > button {
        width: 100% !important;
        height: 75px !important;
        background-color: #ffffff !important;
        color: #2b3a4a !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        font-size: 1.05em !important;
    }
    div.stButton > button:hover {
        border-color: #cbd5e1 !important;
        background-color: #f8fafc !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================================
# PRODUCTION GATEKEEPER: CLEAN SECURITY GATEWAY (NO DEFAULTS)
# =========================================================================
if not st.session_state.logged_in:
    st.title("📱 ADMenu Security Gateway")
    with st.container(border=True):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Unlock Terminal Platform", type="primary"):
            if u == "admin" and p == "admin":
                st.session_state.logged_in = True
                st.rerun()
            else: 
                st.error("Invalid credentials provided.")
    st.stop()

# --- BACK ACTION RETURN LINK PIPELINES ---
if st.session_state.active_view != "Dashboard":
    if st.button("⬅️ Return to Main Control Station Dashboard"):
        st.session_state.active_view = "Dashboard"
        st.rerun()

# =========================================================================
# FRAME WORKSPACE 1: CORE SCREEN LIVE GO-DASHBOARD PORTAL PANEL
# =========================================================================
if st.session_state.active_view == "Dashboard":
    
    active_trip_name = list(st.session_state.trips.keys())[0]
    trip_ref = st.session_state.trips[active_trip_name]
    
    # Corrected Dynamic Currency Mapping Architecture
    curr_iso = trip_ref["currency"].split()[0]
    currency_symbols = {"NPR": "रू", "USD": "$", "EUR": "€", "INR": "₹"}
    curr_sym = currency_symbols.get(curr_iso, "₹")

    with st.container(border=True):
        st.markdown(f"### **{active_trip_name}**")
        st.markdown(f"<span style='color:gray;'>{trip_ref['start'].strftime('%d %b')} — {trip_ref['end'].strftime('%d %b %Y')}</span>", unsafe_allow_html=True)

    st.markdown("#### 🛜 LIVE GO-DASHBOARD")
    
    # Render Route Stops Timeline
    for s in trip_ref["stops"]:
        with st.container(border=True):
            col_l1, col_l2 = st.columns([2, 1])
            
            with col_l1:
                if s["is_live"]:
                    st.markdown(f"🍔 **{s['name']}** &nbsp; <span class='blinking-live-tag'>LIVE</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"🏨 **{s['name']}**")
                
                st.caption(f"{s.get('meal', 'Lunch')} · {s.get('day', 'Day 2')} · {s.get('date_str', '27 Oct')}, {s.get('time', '02:00 pm')}")
                
                if s["is_live"] and s["live_start_time"]:
                    elapsed = int(time.time() - s["live_start_time"])
                    m, s_sec = divmod(elapsed, 60)
                    st.markdown(f"<small style='color:#dc3545;'>⏱️ Active Duration: <b>{m}m {s_sec}s</b></small>", unsafe_allow_html=True)

            with col_l2:
                # Guaranteed Inline HTML Button Overrides for Bulletproof Styling
                if s["is_live"]:
                    if st.button("Stop Live", key=f"stop_{s['id']}", type="primary"):
                        s["is_live"] = False
                        s["live_start_time"] = None
                        st.rerun()
                else:
                    if st.button("Share Live", key=f"start_{s['id']}", type="secondary"):
                        s["is_live"] = True
                        s["live_start_time"] = time.time()
                        st.rerun()

    # --- THE CENTRAL GRID ACTION CONTROLLER KEYPAD ---
    st.markdown("#### ADMIN TOOLS")
    
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("📋\n\nTrip Setup", key="pad_setup"):
        st.session_state.active_view = "Trip Setup"
        st.rerun()
    if col_btn2.button("🍴\n\nMenu Builder", key="pad_builder"):
        st.session_state.active_view = "Menu Builder"
        st.rerun()
        
    col_btn3, col_btn4 = st.columns(2)
    if col_btn3.button("👥\n\nGuest List", key="pad_guests"):
        st.session_state.active_view = "Guest List"
        st.rerun()
    if col_btn4.button("📊\n\nConsolidation & Export", key="pad_export"):
        st.session_state.active_view = "Consolidation & Export"
        st.rerun()
        
    if st.button("💵\n\nLedger", key="pad_ledger"):
        st.session_state.active_view = "Ledger"
        st.rerun()

    # Real-Time Submissions Audit Ticker Tracker Pipeline
    st.markdown("---")
    st.markdown("##### 👥 Passenger Selection Audit List")
    for g in st.session_state.guests:
        with st.container(border=True):
            cg1, cg2, cg3 = st.columns([2, 1, 1])
            cg1.markdown(f"👤 **{g['name']}** <small style='color:gray;'>(ID: {g['id']})</small>", unsafe_allow_html=True)
            if g["submitted"]:
                cg2.markdown("<div style='margin-top:5px;'><span style='background-color:#d4edda; color:#155724; padding:4px 8px; border-radius:4px; font-size:0.85em;'>✅ Submitted</span></div>", unsafe_allow_html=True)
                if cg3.button("Reset", key=f"reset_{g['id']}"):
                    g["submitted"] = False
                    st.rerun()
            else:
                cg2.markdown("<div style='margin-top:5px;'><span style='background-color:#fff3cd; color:#856404; padding:4px 8px; border-radius:4px; font-size:0.85em;'>⏳ Pending</span></div>", unsafe_allow_html=True)
                # Corrected: Explicitly indented action execution line
                if cg3.button("🔔 Ping", key=f"png_{g['id']}"):
                    st.toast(f"Operational broadcast notification ping pushed to {g['name']}!")

# =========================================================================
# FRAME WORKSPACE 2: TRIP PROPERTY PARAMETERS CONFIGURE MODE
# =========================================================================
elif st.session_state.active_view == "Trip Setup":
    st.header("📖 Trip Setup Configuration Panel")
    active_trip_name = list(st.session_state.trips.keys())[0]
    trip_ref = st.session_state.trips[active_trip_name]
    
    with st.form("isolated_setup_form"):
        t_name = st.text_input("Trip Profile Name Designation", value=active_trip_name)
