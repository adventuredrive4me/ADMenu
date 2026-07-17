import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime

# --- PERMANENT DATABASE & STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
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

st.set_page_config(page_title="ADMenu App Engine Pro", layout="centered")

# --- GLOBAL STYLE INJECTION FOR RESPONSIVE MOBILE CORE UI ---
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
    .stButton > button { width: 100%; border-radius: 8px; }
    
    /* 🔴 Crimson Red Stop Live Button Styling Override */
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label="Stop Live"] {
        background-color: #dc3545 !important;
        color: white !important;
        border: 1px solid #dc3545 !important;
        font-weight: bold !important;
    }
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label="Stop Live"]:hover {
        background-color: #bd2130 !important;
    }
    
    /* 🟢 Solid Green Share as Live Button Styling Override */
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label^="Share as Live"] {
        background-color: #28a745 !important;
        color: white !important;
        border: 1px solid #28a745 !important;
        font-weight: bold !important;
    }
    div[data-testid="stHorizontalBlock"] div.stButton button[aria-label^="Share as Live"]:hover {
        background-color: #218838 !important;
    }
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
            else: 
                st.error("Access denied. Invalid system credentials.")
    st.stop()

# =========================================================================
# 📺 ALL-IN-ONE CORE LIVE CONTROL PORTAL
# =========================================================================
st.title("📱 ADMenu Master Console")

active_trip_name = list(st.session_state.trips.keys())[0]
trip_ref = st.session_state.trips[active_trip_name]

# Currency Symbol Evaluator Parser Engine
curr_iso = trip_ref['currency'].split(' ')
curr_sym = "रू" if curr_iso[0] == "NPR" else ("€" if curr_iso[0] == "EUR" else ("$" if curr_iso[0] == "USD" else "₹"))

with st.container(border=True):
    st.subheader(active_trip_name)
    st.caption(f"🗓️ Parameters: {trip_ref['start'].strftime('%d %b')} → {trip_ref['end'].strftime('%d %b %Y')}")
    col_meta1, col_meta2 = st.columns(2)
    col_meta1.metric("⏳ Duration Calculated", f"{trip_ref['days']} Days / {trip_ref['nights']} Nights")
    col_meta2.metric("💱 Operational FX Conversion", f"1 {curr_iso[0]} = ₹{trip_ref['exchange_rate']:.4f}")

# -------------------------------------------------------------------------
# MODULE 1: LIVE ITINERARY GO-DASHBOARD
# -------------------------------------------------------------------------
st.markdown("### 🛜 LIVE GO-DASHBOARD")
for s in trip_ref["stops"]:
    if s["is_live"]:
        with st.container(border=True):
            col_l1, col_l2 = st.columns(2)
            col_l1.markdown(f"🍔 **{s['name']}** &nbsp; <span class='blinking-live-tag'>LIVE</span>", unsafe_allow_html=True)
            col_l1.caption(f"{s['meal']} · {s['day']} · {s['time']}")
            if s["live_start_time"]:
                elapsed = int(time.time() - s["live_start_time"])
                m, s_sec = divmod(elapsed, 60)
                col_l1.markdown(f"⏱️ **Ordering Window Active:** {m}m {s_sec}s")
            if col_l2.button("Stop Live", key=f"stop_{s['id']}"):
                s["is_live"] = False
                s["live_start_time"] = None
                st.rerun()
    else:
        with st.container(border=True):
            col_i1, col_i2 = st.columns(2)
            col_i1.markdown(f"🏨 **{s['name']}**")
            col_i1.caption(f"{s['meal']} · {s['day']} · {s['time']}")
            if col_i2.button(f"Share as Live", key=f"start_{s['id']}"):
                s["is_live"] = True
                s["live_start_time"] = time.time()
                st.rerun()

# -------------------------------------------------------------------------
# MODULE 2: GUEST SUBMISSION STATUS LIST
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 👥 GUEST SELECTION WAVE MONITOR")
audit_cat = st.selectbox("Select Operational Category Window to Audit", ["Breakfast", "Lunch", "Snacks-Break", "Dinner", "Beverages"])

active_audit_stops = [s for s in trip_ref["stops"] if s["meal"] == audit_cat]

if active_audit_stops:
    for s_target in active_audit_stops:
        st.markdown(f"**Venue Stop Monitor: {s_target['name']}**")
        for g in st.session_state.guests:
            with st.container(border=True):
                cg1, cg2, cg3 = st.columns(3)
                cg1.markdown(f"👤 **{g['name']}**<br><span style='font-size:0.8em; color:gray;'>ID: {g['id']}</span>", unsafe_allow_html=True)
                if g["submitted"]:
                    cg2.markdown("<div style='padding-top:10px;'><span style='background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:4px; font-size:0.9em;'>✅ Submitted</span></div>", unsafe_allow_html=True)
                    if cg3.button("Allow changes", key=f"chg_{g['id']}_{s_target['id']}"):
                        g["submitted"] = False
                        st.rerun()
                else:
                    cg2.markdown("<div style='padding-top:10px;'><span style='background-color:#fff3cd; color:#856404; padding:6px 12px; border-radius:4px; font-size:0.9em;'>⏳ Pending</span></div>", unsafe_allow_html=True)
                    if cg3.button("🔔 Ping", key=f"png_{g['id']}_{s_target['id']}"):
                        st.toast(f"Notification ping dispatched to {g['name']}!")
else:
    st.caption(f"No active itinerary route stops assigned under the {audit_cat} wave parameter.")

# -------------------------------------------------------------------------
# MODULE 3: GUEST INTERFACE FEED SIMULATOR
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 📱 SMARTPHONE GUEST APPLICATION INTERFACE")
simulated_guest = st.selectbox("Select Passenger Profile Identity", [g["name"] for g in st.session_state.guests])
g_ref = next(g for g in st.session_state.guests if g["name"] == simulated_guest)

live_stops = [s for s in trip_ref["stops"] if s["is_live"]]

if live_stops:
    global_pricing_toggle = st.checkbox("Reveal prices in local currency to guests for Admin packages", value=False)
    for ls in live_stops:
        st.markdown(f"##### Active Digital Menu Card: {ls['name']}")
        if ls["menu"]:
            std_items = [i for i in ls["menu"] if i["billing"] != "Chargeable Food" and i["display"]]
            charge_items = [i for i in ls["menu"] if i["billing"] == "Chargeable Food" and i["display"]]
            
            with st.form(f"guest_order_form_{ls['id']}"):
                if std_items:
                    st.markdown("**🍲 Included Package Selections**")
                    for idx, item in enumerate(std_items):
