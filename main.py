import streamlit as st
import pandas as pd
import io
import time

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'trips' not in st.session_state:
    st.session_state.trips = {}
if 'categories' not in st.session_state:
    st.session_state.categories = [
        {"name": "Breakfast", "sort_order": 1},
        {"name": "Lunch", "sort_order": 2},
        {"name": "Snacks-Break", "sort_order": 3},
        {"name": "Dinner", "sort_order": 4},
        {"name": "Beverages", "sort_order": 5}
    ]
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = {}
if 'guests' not in st.session_state:
    st.session_state.guests = ["Amit Sharma", "Priya Patel", "Rohan Das", "Sneha Reddy"]
if 'guest_submissions' not in st.session_state:
    st.session_state.guest_submissions = {}
if 'trip_status' not in st.session_state:
    st.session_state.trip_status = {}

st.set_page_config(page_title="ADMenu Mobile", layout="centered")

# --- 1. ADMIN LOG IN ---
st.title("📱 ADMenu Logistics Portal")

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

# --- 2. ADD A TRIP & LOGISTICS ---
st.sidebar.header("🗺️ Plan Trip & Logistics")
with st.sidebar.form("trip_form", clear_on_submit=True):
    t_name = st.text_input("Trip Name*", placeholder="e.g., Goa 2026")
    s_date = st.date_input("Start Date")
    s_time = st.time_input("Start Time")
    e_date = st.date_input("End Date")
    e_time = st.time_input("End Time")
    rest_name = st.text_input("Restaurant Name")
    rest_addr = st.text_area("Address / Location")
    rest_phone = st.text_input("WhatsApp Contact No. (+91)")
    rest_email = st.text_input("Vendor Email Address")
    arr_dt = st.date_input("Expected Arrival Date")
    arr_tm = st.time_input("Expected Arrival Time")
    
    if st.form_submit_button("Initialize Trip Network") and t_name:
        st.session_state.trips[t_name] = {
            "start": f"{s_date} {s_time}", "end": f"{e_date} {e_time}",
            "restaurant": rest_name, "address": rest_addr, "phone": rest_phone,
            "email": rest_email, "arrival": f"{arr_dt} {arr_tm}"
        }
        st.sidebar.success(f"Trip '{t_name}' initialized!")

if not st.session_state.trips:
    st.info("💡 Please create a Trip using the Left Sidebar Logistics form to begin.")
    st.stop()

selected_trip = st.selectbox("🎯 Select Active Trip Environment", list(st.session_state.trips.keys()))
trip_data = st.session_state.trips[selected_trip]

if selected_trip not in st.session_state.menu_items: st.session_state.menu_items[selected_trip] = []
if selected_trip not in st.session_state.guest_submissions: st.session_state.guest_submissions[selected_trip] = {}
if selected_trip not in st.session_state.trip_status: st.session_state.trip_status[selected_trip] = {"sent": False, "sent_time": None}

# --- 3. MENU BUILDER ---
st.header("🍳 Menu Builder")
global_show_prices = st.checkbox("👁️ Allow guests to view prices for Admin-Paid items", value=False)

with st.expander("➕ Add Food Items Smoothly", expanded=True):
    with st.form("bulk_menu_form", clear_on_submit=True):
        f_cat = st.selectbox("Category Group", [c["name"] for c in sorted(st.session_state.categories, key=lambda x: x["sort_order"])])
        f_name = st.text_input("Food Item Name*")
        f_course = st.selectbox("Course Assignment", ["Starter", "Main Course", "Dessert", "Beverages", "Sides"])
        f_unit = st.text_input("Unit of Measure", placeholder="e.g., 1 plate, portion, bottle")
        f_ratio = st.number_input("Target Ratio per Person", min_value=0.0, value=1.0)
        f_price = st.number_input("Price per Unit (Rs.)*", min_value=0.0, value=100.0)
        f_sort = st.number_input("Item Sort Order Priority", min_value=1, value=10)
        f_display = st.checkbox("Display to Guests on App Feed", value=True)
        f_billing = st.selectbox("Billing Class", ["Payable/Admin Account", "Complimentary", "Chargeable Food"])
        
        if st.form_submit_button("⚡ Inject Item Into Live Manifest") and f_name:
            st.session_state.menu_items[selected_trip].append({
                "category": f_cat, "name": f_name, "course": f_course, "unit": f_unit,
                "ratio": f_ratio, "price": f_price, "sort_order": f_sort, "display": f_display, "billing": f_billing
            })
            st.success(f"Added '{f_name}'!")

if st.session_state.menu_items[selected_trip]:
    df_menu = pd.DataFrame(st.session_state.menu_items[selected_trip])
    st.dataframe(df_menu.sort_values(by=["category", "sort_order"]), use_container_width=True)

# --- 4. ONE-BUTTON DISPATCH & COUNTDOWN ---
st.markdown("---")
st.header("🔔 Live Guest Dispatch Network")
is_sent = st.session_state.trip_status[selected_trip]["sent"]

if not is_sent:
    if st.button("📢 Broadcast Menu App Link Live to Guests", type="primary", use_container_width=True):
        st.session_state.trip_status[selected_trip] = {"sent": True, "sent_time": time.time()}
        st.balloons()
        st.rerun()
else:
    st.success("🚀 Menu is currently LIVE. Configuration edits are locked.")
    elapsed = int(time.time() - st.session_state.trip_status[selected_trip]["sent_time"])
    mins, secs = divmod(elapsed, 60)
    st.metric("⏱️ Ordering Window Active Time", f"{mins:02d}m : {secs:02d}s")
    if st.button("🔄 Refresh Countdown"): st.rerun()

# --- 5. MOBILE GUEST SIMULATOR ---
if is_sent:
    st.markdown("---")
    st.header("📱 Guest Mobile Interface Screen")
    active_guest = st.selectbox("Select Mock Identity", st.session_state.guests)
    guest_selections = {}
    visible_items = [i for i in st.session_state.menu_items[selected_trip] if i["display"]]
    
    if visible_items:
        normal_items = [i for i in visible_items if i["billing"] != "Chargeable Food"]
        chargeable_items = [i for i in visible_items if i["billing"] == "Chargeable Food"]
        
        if normal_items:
            st.subheader("🍽️ Included Food Items")
            for idx, item in enumerate(normal_items):
                price_lbl = "(Complimentary)" if item["billing"] == "Complimentary" else (f"Rs. {item['price']}" if global_show_prices else "")
                label_text = f"{item['category']} - {item['name']} {price_lbl}"
                is_chk = st.checkbox(label_text, key=f"g_n_{idx}_{active_guest}")
                qty_val = st.selectbox("Qty", list(range(1, 11)), key=f"g_nq_{idx}_{active_guest}")
                if is_chk: guest_selections[item["name"]] = {"qty": qty_val, "price": item["price"], "billing": item["billing"], "unit": item["unit"]}

        if chargeable_items:
            st.error("⚠️ Chargeable Food (Pay at Counter)")
            for idx, item in enumerate(chargeable_items):
                label_text = f"🔥 [COUNTER PAYABLE] {item['category']} - {item['name']} - Rs. {item['price']}"
                is_chk = st.checkbox(label_text, key=f"g_c_{idx}_{active_guest}")
                qty_val = st.selectbox("Qty", list(range(1, 11)), key=f"g_cq_{idx}_{active_guest}")
                if is_chk: guest_selections[item["name"]] = {"qty": qty_val, "price": item["price"], "billing": item["billing"], "unit": item["unit"]}

        if st.button("🗳️ Finalize and Submit Choices", use_container_width=True):
            st.session_state.guest_submissions[selected_trip][active_guest] = guest_selections
            st.success("Order synchronized securely!")
            st.rerun()

# --- 6. ADMIN TRACKING ---
st.markdown("---")
st.header("📊 Admin Tracking Workspace")
audit_cat = st.selectbox("Select Category Window to Audit", [c["name"] for c in st.session_state.categories])
submissions_this_trip = st.session_state.guest_submissions[selected_trip]

audit_rows = []
for g in st.session_state.guests:
    has_sub = g in submissions_this_trip
    status_indicator = "✅ Order Received" if has_sub else "⏳ Pending"
    ordered_items_string = "None"
    if has_sub:
        item_details = []
        for f_name, details in submissions_this_trip[g].items():
            orig = next((i for i in st.session_state.menu_items[selected_trip] if i["name"] == f_name), None)
            if orig and orig["category"] == audit_cat: item_details.append(f"{f_name} ({details['qty']})")
        if item_details: ordered_items_string = ", ".join(item_details)
    audit_rows.append({"Guest Name": g, "Status": status_indicator, f"Choices ({audit_cat})": ordered_items_string})
st.dataframe(pd.DataFrame(audit_rows), use_container_width=True)

# --- 7. FINANCIAL LEDGER & ACCOUNTING ---
st.subheader("📈 Global Aggregator & Financial Audit Report")
totals, admin_payable_cost, admin_complimentary_cost, counter_chargeable_cost, chargeable_ledger = {}, 0.0, 0.0, 0.0, []

for guest, items in submissions_this_trip.items():
    guest_counter_debt = 0.0
    for f_name, d in items.items():
        if f_name not in totals: totals[f_name] = {"Quantity": 0, "Unit": d["unit"], "Billing": d["billing"], "Cost": 0.0}
        totals[f_name]["Quantity"] += d["qty"]
        line_cost = d["qty"] * d["price"]
        totals[f_name]["Cost"] += line_cost
        
        if d["billing"] == "Payable/Admin Account": admin_payable_cost += line_cost
        elif d["billing"] == "Complimentary": admin_complimentary_cost += line_cost
        elif d["billing"] == "Chargeable Food":
            counter_chargeable_cost += line_cost
            guest_counter_debt += line_cost
