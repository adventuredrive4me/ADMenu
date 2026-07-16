import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'trips' not in st.session_state:
    st.session_state.trips = {}
if 'guests' not in st.session_state:
    st.session_state.guests = ["Amit Sharma", "Priya Patel", "Rohan Das", "Sneha Reddy"]
if 'guest_submissions' not in st.session_state:
    st.session_state.guest_submissions = {} # trip_name -> stop_id -> guest_name -> choices
if 'trip_status' not in st.session_state:
    st.session_state.trip_status = {}  # trip_name -> stop_id -> {"sent": Bool, "sent_time": float}

st.set_page_config(page_title="ADMenu Premium Mobile", layout="centered")

# --- 1. ADMIN LOG IN ---
st.title("📱 ADMenu Logistics Portal Pro")

if not st.session_state.logged_in:
    st.subheader("🔑 Administrator Access")
    username = st.text_input("Admin Username", value="admin")
    password = st.text_input("Admin Password", type="password", value="admin")
    if st.button("Access Dashboard", use_container_width=True):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

if st.sidebar.button("🔒 Secure Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- 2. ADVANCED TRIP LOGISTICS & SIDEBAR ---
st.sidebar.header("🗺️ Plan Trip & Logistics")
with st.sidebar.form("trip_form", clear_on_submit=True):
    t_name = st.text_input("Trip Name*", placeholder="e.g., Canyon Odyssey")
    
    st.markdown("##### 📅 Schedule Parameters")
    s_date = st.date_input("Start Date")
    s_time = st.time_input("Start Time")
    e_date = st.date_input("End Date")
    e_time = st.time_input("End Time")
    
    st.markdown("##### 💵 Currency Control Settings")
    t_curr = st.selectbox("Trip Local Currency", ["NPR - Nepalese Rupee", "EUR - Euro", "USD - US Dollar", "INR - Indian Rupee"])
    ex_rate = st.number_input("Exchange Rate (1 Local Unit = ? INR)", min_value=0.001, value=0.60, format="%.4f")
    
    if st.form_submit_button("Initialize Trip Network") and t_name:
        # Calculate Days and Nights
        dt_start = datetime.combine(s_date, s_time)
        dt_end = datetime.combine(e_date, e_time)
        delta = dt_end - dt_start
        days = max(1, delta.days + 1)
        nights = max(0, days - 1)
        
        st.session_state.trips[t_name] = {
            "start": dt_start,
            "end": dt_end,
            "days": days,
            "nights": nights,
            "currency": t_curr,
            "exchange_rate": ex_rate,
            "stops": [] # List of dictionaries for eateries
        }
        st.sidebar.success(f"Trip '{t_name}' initialized!")

if not st.session_state.trips:
    st.info("💡 Please establish a Trip environment in the Left Sidebar to begin.")
    st.stop()

selected_trip = st.selectbox("🎯 Select Active Trip Environment", list(st.session_state.trips.keys()))
trip_data = st.session_state.trips[selected_trip]

# --- DISPLAY CALCULATORS METRICS ---
st.markdown(f"### 🗓️ Overview: {selected_trip}")
c_days, c_curr = st.columns(2)
c_days.metric("⏳ Trip Duration Calculated", f"{trip_data['days']} Days / {trip_data['nights']} Nights")
c_curr.metric("💱 Operational FX Conversion", f"1 {trip_data['currency'].split(' ')[0]} = ₹{trip_data['exchange_rate']}")

# --- 3. MULTI-STOP ITINERARY TIMELINE ---
st.markdown("---")
st.header("📍 Multi-Stop Itinerary Timeline")

with st.expander("➕ Add Stop/Eatery to Trip Timeline", expanded=False):
    with st.form("stop_form", clear_on_submit=True):
        stop_day = st.selectbox("Timeline Day Assignment", [f"Day {i}" for i in range(1, trip_data['days'] + 1)])
        stop_meal = st.selectbox("Stop Category/Meal Window", ["Breakfast", "Lunch", "Snacks-Break", "Dinner", "Beverages"])
        r_name = st.text_input("Restaurant / Venue Name*")
        r_addr = st.text_area("Address / Location")
        r_phone = st.text_input("WhatsApp Contact (+91 / International)")
        r_email = st.text_input("Vendor Email")
        arr_time = st.time_input("Expected Arrival Time")
        
        if st.form_submit_button("🔗 Link Eatery Stop to Itinerary") and r_name:
            stop_id = f"{stop_day}_{stop_meal}_{r_name.replace(' ', '_')}"
            trip_data["stops"].append({
                "id": stop_id, "day": stop_day, "meal": stop_meal, "name": r_name,
                "address": r_addr, "phone": r_phone, "email": r_email, "arrival": str(arr_time),
                "menu": [] # Food items mapped explicitly to this stop
            })
            st.success(f"Linked {r_name} to timeline!")

# Render Linked Stops
if not trip_data["stops"]:
    st.warning("⚠️ No eateries or food stops linked to this itinerary yet.")
    st.stop()

st.markdown("##### 📌 Current Operational Route Matrix")
stop_options = {f"{s['day']} - {s['meal']} at {s['name']}": s for s in trip_data["stops"]}
active_stop_lbl = st.selectbox("Select Restaurant Stop to Manage & Build Menu", list(stop_options.keys()))
active_stop = stop_options[active_stop_lbl]

# --- 4. ITEM LEVEL MENU BUILDER ---
st.markdown("---")
st.header(f"🍳 Menu Builder for {active_stop['name']}")
global_show_prices = st.checkbox("👁️ Allow guests to view local currency prices for Admin-Paid items", value=False)

with st.expander("➕ Add Food Items to This Specific Stop", expanded=True):
    with st.form("food_item_form", clear_on_submit=True):
        f_name = st.text_input("Food Item Name*")
        f_course = st.selectbox("Course Assignment", ["Starter", "Main Course", "Dessert", "Beverages", "Sides"])
        f_unit = st.text_input("Unit of Measure", value="1 portion")
        f_ratio = st.number_input("Target Ratio per Person", min_value=0.0, value=1.0)
        f_price = st.number_input(f"Price per Unit ({trip_data['currency'].split(' ')[0]})*", min_value=0.0, value=100.0)
        f_sort = st.number_input("Item Sort Priority Order", min_value=1, value=10)
        f_display = st.checkbox("Display to Guests on App Feed", value=True)
        f_billing = st.selectbox("Billing Class", ["Payable/Admin Account", "Complimentary", "Chargeable Food"])
        
        if st.form_submit_button("⚡ Inject Item Into Stop Manifest") and f_name:
            active_stop["menu"].append({
                "name": f_name, "course": f_course, "unit": f_unit, "ratio": f_ratio,
                "price": f_price, "sort_order": f_sort, "display": f_display, "billing": f_billing
            })
            st.success(f"Added '{f_name}' to {active_stop['name']} menu!")

if active_stop["menu"]:
    st.dataframe(pd.DataFrame(active_stop["menu"]).sort_values(by="sort_order"), use_container_width=True)

# --- 5. ONE-BUTTON DISPATCH & TIMER ---
st.markdown("---")
st.header("🔔 Live Guest Dispatch Network")
if selected_trip not in st.session_state.trip_status: st.session_state.trip_status[selected_trip] = {}
if active_stop["id"] not in st.session_state.trip_status[selected_trip]:
    st.session_state.trip_status[selected_trip][active_stop["id"]] = {"sent": False, "sent_time": None}

status_block = st.session_state.trip_status[selected_trip][active_stop["id"]]

if not status_block["sent"]:
    if st.button(f"📢 Broadcast Menu & Open Live Orders for {active_stop['name']}", type="primary", use_container_width=True):
        st.session_state.trip_status[selected_trip][active_stop["id"]] = {"sent": True, "sent_time": time.time()}
        st.balloons()
        st.rerun()
else:
    st.success(f"🚀 Ordering matrix for {active_stop['name']} is currently LIVE.")
    elapsed = int(time.time() - status_block["sent_time"])
    mins, secs = divmod(elapsed, 60)
    st.metric("⏱️ Active Selection Countdown Window", f"{mins:02d}m : {secs:02d}s")
    if st.button("🔄 Refresh Timer State"): st.rerun()

# --- 6. GUEST INTERFACE SIMULATOR ---
if status_block["sent"]:
    st.markdown("---")
    st.header("📱 Guest Mobile Form Simulator")
    active_guest = st.selectbox("Select Mock Identity", st.session_state.guests)
    
    if selected_trip not in st.session_state.guest_submissions: st.session_state.guest_submissions[selected_trip] = {}
    if active_stop["id"] not in st.session_state.guest_submissions[selected_trip]: st.session_state.guest_submissions[selected_trip][active_stop["id"]] = {}
    
    guest_selections = {}
    visible_items = [i for i in active_stop["menu"] if i["display"]]
    
    if visible_items:
        normal_items = [i for i in visible_items if i["billing"] != "Chargeable Food"]
        chargeable_items = [i for i in visible_items if i["billing"] == "Chargeable Food"]
        
        if normal_items:
            st.subheader("🍽️ Package Selections")
            for idx, item in enumerate(normal_items):
                lbl_p = "(Complimentary)" if item["billing"] == "Complimentary" else (f"{item['price']} {trip_data['currency'].split(' ')[0]}" if global_show_prices else "")
                is_chk = st.checkbox(f"{item['course']} - {item['name']} {lbl_p}", key=f"g_n_{idx}_{active_guest}")
                qty_val = st.selectbox("Qty", list(range(1, 11)), key=f"g_nq_{idx}_{active_guest}")
                if is_chk: guest_selections[item["name"]] = {"qty": qty_val, "price": item["price"], "billing": item["billing"], "unit": item["unit"]}

        if chargeable_items:
            st.error("⚠️ Chargeable Food (Pay Direct to Counter)")
            for idx, item in enumerate(chargeable_items):
                is_chk = st.checkbox(f"🔥 [COUNTER Owed] {item['name']} - {item['price']} {trip_data['currency'].split(' ')[0]}", key=f"g_c_{idx}_{active_guest}")
                qty_val = st.selectbox("Qty", list(range(1, 11)), key=f"g_cq_{idx}_{active_guest}")
                if is_chk: guest_selections[item["name"]] = {"qty": qty_val, "price": item["price"], "billing": item["billing"], "unit": item["unit"]}
