import streamlit as st
from pages.style import inject_global_css, section_header, page_banner

inject_global_css()

# Remove the conflicting set_page_config call — home.py owns it
# st.set_page_config(page_title="My Bookings", page_icon="📋")

page_banner(
    title="My Bookings",
    subtitle="Track all your service bookings and leave reviews.",
    icon="📋",
)

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "customer":
    st.warning("⚠️ Login as a **Customer**.")
    st.stop()

db   = st.session_state.db
user = st.session_state.user_data
bookings = db.get_customer_bookings(user["id"])

if not bookings:
    st.markdown(
        "<div style='text-align:center; padding:3rem; color:#94A3B8;'>"
        "<div style='font-size:3rem;'>📋</div>"
        "<div style='font-size:1.1rem; margin-top:0.5rem;'>No bookings yet!</div>"
        "<div style='font-size:0.85rem; margin-top:0.3rem;'>Search for a service provider to get started.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

# ---- Status Summary ----
section_header("📊 Booking Summary")

s1, s2, s3, s4, s5 = st.columns(5)
summary_items = [
    (s1, "Total",      len(bookings),                                                  "#1A56DB"),
    (s2, "Pending",    len([b for b in bookings if b["status"] == "pending"]),          "#F59E0B"),
    (s3, "Accepted",   len([b for b in bookings if b["status"] == "accepted"]),         "#10B981"),
    (s4, "Completed",  len([b for b in bookings if b["status"] == "completed"]),        "#7C3AED"),
    (s5, "Cancelled",  len([b for b in bookings if b["status"] in ["cancelled","rejected"]]), "#EF4444"),
]
for col, label, val, color in summary_items:
    with col:
        st.markdown(
            f"""
            <div style='background:white; border:1px solid #E2E8F0; border-radius:12px;
                        padding:0.9rem 0.5rem; text-align:center;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05); border-top:4px solid {color};'>
              <div style='font-size:1.5rem; font-weight:800; color:{color};'>{val}</div>
              <div style='font-size:0.72rem; font-weight:600; color:#64748B;
                          text-transform:uppercase; letter-spacing:0.4px;'>{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

STATUS_COLORS = {
    "pending":   ("#FEF9C3", "#CA8A04", "🟡"),
    "accepted":  ("#DCFCE7", "#15803D", "🟢"),
    "completed": ("#EFF6FF", "#1D4ED8", "✅"),
    "rejected":  ("#FEE2E2", "#B91C1C", "🔴"),
    "cancelled": ("#F1F5F9", "#475569", "⚫"),
}

def show_booking(b, tab_prefix):
    bg, border, icon = STATUS_COLORS.get(b["status"], ("#F8FAFC", "#94A3B8", "⚪"))

    with st.container(border=True):
        # Header row
        st.markdown(
            f"""
            <div style='background:{bg}; border-left:4px solid {border}; border-radius:8px;
                        padding:0.6rem 0.8rem; margin-bottom:0.6rem;
                        display:flex; align-items:center; gap:0.5rem;'>
              <span style='font-size:1.1rem;'>{icon}</span>
              <span style='font-weight:700; color:#0F172A; font-size:1rem;'>
                Booking #{b['id']}
              </span>
              <span style='margin-left:auto; background:{border}22; color:{border};
                           font-size:0.72rem; font-weight:700; padding:2px 10px;
                           border-radius:20px; text-transform:uppercase;'>
                {b['status']}
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<div style='font-size:0.85rem; color:#64748B;'>Provider</div>"
                f"<div style='font-weight:600; color:#0F172A;'>{b['provider_name']}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='font-size:0.85rem; color:#64748B; margin-top:0.4rem;'>Service</div>"
                f"<div style='font-weight:600; color:#0F172A;'>{b['service_type'].title()}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"<div style='font-size:0.85rem; color:#64748B;'>Date</div>"
                f"<div style='font-weight:600; color:#0F172A;'>{b['booking_date']}</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"<div style='font-size:0.85rem; color:#64748B; margin-top:0.4rem;'>Issue</div>"
            f"<div style='color:#1E293B; font-size:0.9rem;'>{b['description']}</div>",
            unsafe_allow_html=True,
        )

        # Accepted — show contact
        if b["status"] == "accepted":
            phone_number = b.get("provider_phone", "No phone number found")
            st.markdown(
                f"""
                <div style='background:#DCFCE7; border:1px solid #86EFAC; border-radius:10px;
                            padding:0.8rem 1rem; margin-top:0.6rem;'>
                  <div style='font-weight:700; color:#14532D; font-size:0.9rem;'>
                    ✅ Booking Accepted!
                  </div>
                  <div style='font-size:1.05rem; font-weight:700; color:#15803D; margin-top:4px;'>
                    📞 Contact Provider: {phone_number}
                  </div>
                  <div style='font-size:0.78rem; color:#16A34A; margin-top:2px;'>
                    Call the provider to coordinate the service time.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Pending — cancel button
        if b["status"] == "pending":
            st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
            if st.button("❌ Cancel Booking", key=f"{tab_prefix}_can_{b['id']}"):
                db.update_booking_status(b["id"], "cancelled")
                st.rerun()

        # Completed — review form
        if b["status"] == "completed":
            st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
            existing_reviews = db.get_customer_reviews(user["id"])
            already_reviewed = any(r["booking_id"] == b["id"] for r in existing_reviews)

            if already_reviewed:
                st.markdown(
                    "<div style='background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px;"
                    " padding:0.5rem 0.8rem; font-size:0.85rem; color:#1E40AF;'>"
                    "✅ Service Finished & Reviewed</div>",
                    unsafe_allow_html=True,
                )
            else:
                with st.expander("📝 Leave a Review for this Service"):
                    with st.form(f"rev_{b['id']}"):
                        rating = st.slider("Rating", 1, 5, 5)
                        text   = st.text_area("How was the experience?")
                        if st.form_submit_button("Submit Review"):
                            if text.strip():
                                db.create_review(b["id"], user["id"], b["provider_id"], rating, text, b["service_type"])
                                st.rerun()
                            else:
                                st.error("Please add a comment.")

st.markdown("<br>", unsafe_allow_html=True)

# ---- Tabbed view ----
t1, t2, t3, t4, t5 = st.tabs(["📋 All", "🟡 Pending", "🟢 Accepted", "✅ Completed", "❌ Cancelled"])

with t1:
    for b in bookings: show_booking(b, "all")
with t2:
    pending = [b for b in bookings if b["status"] == "pending"]
    if not pending:
        st.info("No pending requests.")
    for b in pending: show_booking(b, "pen")
with t3:
    accepted = [b for b in bookings if b["status"] == "accepted"]
    if not accepted:
        st.info("No accepted bookings. Contact info will appear here once accepted.")
    for b in accepted: show_booking(b, "acc")
with t4:
    completed = [b for b in bookings if b["status"] == "completed"]
    if not completed:
        st.info("No completed bookings.")
    for b in completed: show_booking(b, "com")
with t5:
    cancelled = [b for b in bookings if b["status"] in ["cancelled", "rejected"]]
    if not cancelled:
        st.info("No cancelled bookings.")
    for b in cancelled: show_booking(b, "can")