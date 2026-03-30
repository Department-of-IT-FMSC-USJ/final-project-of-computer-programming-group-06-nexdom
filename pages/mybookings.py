import streamlit as st

st.set_page_config(page_title="My Bookings", page_icon="📋")
st.title("📋 My Bookings")
st.markdown("---")

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "customer":
    st.warning("⚠️ Login as a **Customer**.")
    st.stop()

db = st.session_state.db
user = st.session_state.user_data
bookings = db.get_customer_bookings(user["id"])

if not bookings:
    st.info("📋 No bookings yet!")
    st.stop()

# Dashboard
s1, s2, s3, s4, s5 = st.columns(5)
s1.metric("📋 Total", len(bookings))
s2.metric("🟡 Pending", len([b for b in bookings if b["status"] == "pending"]))
s3.metric("🟢 Accepted", len([b for b in bookings if b["status"] == "accepted"]))
s4.metric("✅ Completed", len([b for b in bookings if b["status"] == "completed"]))
s5.metric("❌ Cancelled", len([b for b in bookings if b["status"] in ["cancelled", "rejected"]]))

def show_booking(b, tab_prefix):
    icons = {"pending": "🟡", "accepted": "🟢", "completed": "✅", "rejected": "🔴", "cancelled": "⚫"}
    icon = icons.get(b["status"], "⚪")
    
    with st.container(border=True):
        st.markdown(f"### {icon} Booking #{b['id']}")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Provider:** {b['provider_name']}")
            st.write(f"**Service:** {b['service_type'].title()}")
        with col2:
            st.write(f"**Date:** {b['booking_date']}")
            st.write(f"**Status:** `{b['status'].upper()}`")
        
        st.write(f"**Issue:** {b['description']}")

        # --- UPDATED CONTACT DETAILS LOGIC ---
        # Changed from [ "accepted", "completed" ] to ONLY [ "accepted" ]
# Inside your show_booking(b, tab_prefix) function:

# --- CONTACT DETAILS (ONLY FOR ACCEPTED) ---
# --- CONTACT DETAILS (ONLY FOR ACCEPTED) ---
        if b["status"] == "accepted":
            st.markdown("---")
            st.success("✅ **Booking Accepted!**")
            
            # Retrieve the phone number from the dict
            phone_number = b.get("provider_phone", "No phone number found")
            
            # Using a single markdown line to remove the gap
            st.markdown(f"### 📞 Contact Provider: **{phone_number}**")
            
            st.caption("Call the provider to coordinate the service time.")

        # --- Cancel Logic ---
        if b["status"] == "pending":
            st.markdown("---")
            if st.button("❌ Cancel Booking", key=f"{tab_prefix}_can_{b['id']}"):
                db.update_booking_status(b["id"], "cancelled")
                st.rerun()

        # --- Review Logic ---
        if b["status"] == "completed":
            st.markdown("---")
            existing_reviews = db.get_customer_reviews(user["id"])
            already_reviewed = any(r["booking_id"] == b["id"] for r in existing_reviews)
            
            if already_reviewed:
                st.info("✅ Service Finished & Reviewed")
            else:
                with st.expander("📝 Leave a Review for this Service"):
                    with st.form(f"rev_{b['id']}"):
                        rating = st.slider("Rating", 1, 5, 5)
                        text = st.text_area("How was the experience?")
                        if st.form_submit_button("Submit Review"):
                            if text.strip():
                                db.create_review(b["id"], user["id"], b["provider_id"], rating, text, b["service_type"])
                                st.rerun()
                            else:
                                st.error("Please add a comment.")

st.markdown("---")
t1, t2, t3, t4, t5 = st.tabs(["📋 All", "🟡 Pending", "🟢 Accepted", "✅ Completed", "❌ Cancelled"])

with t1: 
    for b in bookings: show_booking(b, "all")
with t2: 
    pending = [b for b in bookings if b["status"] == "pending"]
    if not pending: st.info("No pending requests.")
    for b in pending: show_booking(b, "pen")
with t3: 
    accepted = [b for b in bookings if b["status"] == "accepted"]
    if not accepted: st.info("No accepted bookings. Contact info will appear here once accepted.")
    for b in accepted: show_booking(b, "acc")
with t4: 
    completed = [b for b in bookings if b["status"] == "completed"]
    if not completed: st.info("No completed bookings.")
    for b in completed: show_booking(b, "com")
with t5: 
    cancelled = [b for b in bookings if b["status"] in ["cancelled", "rejected"]]
    if not cancelled: st.info("No cancelled bookings.")
    for b in cancelled: show_booking(b, "can")