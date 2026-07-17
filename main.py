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
# ADVANCED CSS INJECTION FOR PREMIUM MATTE LOOK & BLINKING ANIMATIONS
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
    
    /* 🛠️ Admin Pad Core Action Button Styling Overrides */
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
    
    /* 🔴 Crimson Red Stop Live Button Styling */
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label="Stop Live"] {
        background-color: #dc3545 !important;
        color: white !important;
        border: 1px solid #dc3545 !important;
        height: 42px !important;
    }
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label="Stop Live"]:hover {
        background-color: #bd2130 !important;
    }
    
    /* 🟢 Solid Green Share as Live Button Styling */
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label^="Share as Live"] {
        background-color: #28a745 !important;
        color: white !important;
        border: 1px solid #28a745 !important;
        height: 42px !important;
    }
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label^="Share as Live"]:hover {
        background-color: #218838 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SYSTEM SECURITY ENTRY PROTOCOL ---
if not st.session_state.logged_in:
    st.title("📱 ADMenu Security Gateway")
    with st.container(border=True):
        u = st.text_input("Username", value="admin")
        p = st.text_input("Password", type="password", value="admin")
        if st.button("Unlock Terminal Platform", type="primary"):
            if u == "admin" and p == "admin":
                st.session_state.logged_in = True
                st.rerun()
            else: 
                st.error("Invalid administrator profile parameter entry matches.")
    st.stop()

# --- BACK ACTION RETURN FLOATING LINK ---
if st.session_state.active_view != "Dashboard":
    st.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("⬅️ Return to Main Console View"):
        st.session_state.active_view = "Dashboard"
        st.rerun()

# =========================================================================
# VIEW CONTROLLER 1: CORE SCREEN LIVE GO-DASHBOARD (YOUR IMAGE LAYOUT)
# =========================================================================
if st.session_state.active_view == "Dashboard":
    
    # Extract string key safely to eliminate dictionary indexing crashes
    active_trip_name = list(st.session_state.trips.keys())[0]
    trip_ref = st.session_state.trips[active_trip_name]
    
    # Format Currency Strings
    curr_iso = trip_ref['currency'].split(' ')[0]
    curr_sym = "रू" if curr_iso == "NPR" else ("€" if curr_iso == "EUR" else ("$" if curr_iso == "USD" else "₹"))

    # Render Header Card matching your layout view profile precisely
    with st.container(border=True):
        st.markdown(f"### **{active_trip_name}**")
        st.markdown(f"<span style='color:gray;'>{trip_ref['start'].strftime('%d %b')} — {trip_ref['end'].strftime('%d %b')}</span>", unsafe_allow_html=True)

    st.markdown("#### 🛜 LIVE GO-DASHBOARD")
    
    # Render Dynamic Multi-Stop Route Timelines
    for s in trip_ref["stops"]:
        with st.container(border=True):
            col_l1, col_l2 = st.columns([2, 1])
            
            with col_l1:
                if s["is_live"]:
                    st.markdown(f"🍔 **{s['name']}** &nbsp; <span class='blinking-live-tag'>LIVE</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"🏨 **{s['name']}**")
                st.caption(f"{s['meal']} · {s['day']} · {s['date_str']}, {s['time']}")
                
                # Active Dynamic Countdown Clock Readout
                if s["is_live"] and s["live_start_time"]:
                    elapsed = int(time.time() - s["live_start_time"])
                    m, s_sec = divmod(elapsed, 60)
                    st.markdown(f"<small style='color:#dc3545;'>⏱️ Ordering Active: <b>{m}m {s_sec}s</b></small>", unsafe_allow_html=True)

            with col_l2:
                st.markdown("<div style='padding-top:8px;'></div>", unsafe_allow_html=True)
                if s["is_live"]:
                    if st.button("Stop Live", key=f"stop_{s['id']}"):
                        s["is_live"] = False
                        s["live_start_time"] = None
                        st.rerun()
                else:
                    if st.button("Share as Live", key=f"start_{s['id']}"):
                        s["is_live"] = True
                        s["live_start_time"] = time.time()
                        st.rerun()

    # --- ADMIN TOOLS CONTROLLER PAD GENERATOR (MATCHES IMAGE SPEC) ---
    st.markdown("#### ADMIN TOOLS")
    
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("📖\n\nTrip Setup", key="pad_setup"):
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

    # Real-Time Passenger Status Monitor Summary Feed
    st.markdown("---")
    st.markdown("##### 👥 Passenger Selection Audit List")
    for g in st.session_state.guests:
        with st.container(border=True):
            cg1, cg2, cg3 = st.columns([1, 1, 1])
            cg1.markdown(f"👤 **{g['name']}** <small style='color:gray;'>(ID: {g['id']})</small>", unsafe_allow_html=True)
            if g["submitted"]:
                cg2.markdown("<span style='background-color:#d4edda; color:#155724; padding:4px 8px; border-radius:4px; font-size:0.85em;'>✅ Submitted</span>", unsafe_allow_html=True)
                if cg3.button("Reset Entry", key=f"reset_{g['id']}"):
                    g["submitted"] = False
                    st.rerun()
            else:
