import streamlit as st

st.title("📋 Booking Requests")
st.markdown("---")

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "provider":
    st.warning("⚠️ Login as **Provider**.")
    st.stop()

db = st.session_state.db
user = st.session_state.user_data
all_bookings = db.get_provider_bookings(user["id"])

if not all_bookings:
    st.info("📋 No booking requests yet!")
    st.stop()

# Stats
s1, s2, s3, s4 = st.columns(4)
s1.metric("📋 Total", len(all_bookings))
s2.metric("🟡 Pending", len([b for b in all_bookings if b["status"] == "pending"]))
s3.metric("🟢 Accepted", len([b for b in all_bookings if b["status"] == "accepted"]))
s4.metric("✅ Completed", len([b for b in all_bookings if b["status"] == "completed"]))

st.markdown("---")
tab1, tab2, tab3, tab4 = st.tabs(["🟡 Pending", "🟢 Accepted", "✅ Completed", "📋 All"])

with tab1:
    pending = [b for b in all_bookings if b["status"] == "pending"]
    for b in pending:
        st.markdown(f"### 🟡 Booking #{b['id']}")
        st.write(f"**Customer:** {b['customer_name']}")
        st.write(f"**Date:** {b['booking_date']}")
        st.write(f"**Issue:** {b['description']}")
        c1, c2, _ = st.columns([1, 1, 3])
        if c1.button("✅ Accept", key=f"a_{b['id']}"):
            db.update_booking_status(b["id"], "accepted")
            st.rerun()
        if c2.button("❌ Reject", key=f"r_{b['id']}"):
            db.update_booking_status(b["id"], "rejected")
            st.rerun()
        st.markdown("---")

with tab2:
    accepted = [b for b in all_bookings if b["status"] == "accepted"]
    for b in accepted:
        st.markdown(f"### 🟢 Booking #{b['id']}")
        st.write(f"**Customer:** {b['customer_name']}")
        st.write(f"**Issue:** {b['description']}")
        if st.button("✔️ Complete", key=f"c_{b['id']}"):
            db.update_booking_status(b["id"], "completed")
            st.rerun()
        st.markdown("---")

with tab3:
    completed = [b for b in all_bookings if b["status"] == "completed"]
    for b in completed:
        st.write(f"✅ **#{b['id']}** | {b['customer_name']} | {b['booking_date']}")

with tab4:
    for b in all_bookings:
        st.write(f"**#{b['id']}** | {b['customer_name']} | {b['status'].upper()}")