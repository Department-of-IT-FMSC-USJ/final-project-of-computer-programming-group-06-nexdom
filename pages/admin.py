import streamlit as st
import pandas as pd
from pages.style import inject_global_css, section_header, page_banner

inject_global_css()

page_banner(
    title="Admin Dashboard",
    subtitle="Manage providers, bookings, and platform statistics.",
    icon="🛡️",
)

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

# SIMPLE ADMIN PASSWORD GATE

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown(
        "<h3 style='text-align:center; margin-bottom:1rem; color:#0F172A;'>🔒 Admin Login</h3>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<div style='background:white; border:1px solid #E2E8F0; border-radius:14px;"
            " padding:1.8rem; box-shadow:0 4px 16px rgba(0,0,0,0.07);'>",
            unsafe_allow_html=True,
        )
        with st.form("admin_login"):
            admin_pass = st.text_input("Admin Password", type="password")
            if st.form_submit_button("🔑 Login", use_container_width=True):
                if admin_pass == "admin123":
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Wrong password!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

db = st.session_state.db

# Logout button
if st.button("🚪 Exit Admin"):
    st.session_state.admin_authenticated = False
    st.rerun()

# PLATFORM STATISTICS

section_header("📊 Platform Overview", "Live snapshot of all platform activity")

stats = db.get_platform_stats()

c1, c2, c3, c4, c5 = st.columns(5)
stat_items = [
    (c1, "Providers",   stats.get("total_providers", 0),   "🔧", "#1A56DB"),
    (c2, "Customers",   stats.get("total_customers", 0),   "👥", "#7C3AED"),
    (c3, "Bookings",    stats.get("total_bookings", 0),    "📋", "#F59E0B"),
    (c4, "Completed",   stats.get("completed_bookings", 0),"✅", "#10B981"),
    (c5, "Reviews",     stats.get("total_reviews", 0),     "⭐", "#EF4444"),
]
for col, label, val, icon, color in stat_items:
    with col:
        st.markdown(
            f"""
            <div style='background:white; border:1px solid #E2E8F0; border-radius:12px;
                        padding:1rem 0.8rem; text-align:center;
                        box-shadow:0 1px 4px rgba(0,0,0,0.06);
                        border-top:4px solid {color};'>
              <div style='font-size:1.5rem;'>{icon}</div>
              <div style='font-size:1.7rem; font-weight:800; color:{color};
                          margin-top:4px;'>{val}</div>
              <div style='font-size:0.72rem; font-weight:600; color:#64748B;
                          text-transform:uppercase; letter-spacing:0.5px;'>{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Completion rate
total    = stats.get("total_bookings", 0)
complete = stats.get("completed_bookings", 0)
rate     = (complete / total * 100) if total > 0 else 0
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style='background:linear-gradient(135deg,#ECFDF5,#D1FAE5);
                border:1px solid #6EE7B7; border-radius:10px;
                padding:0.9rem 1.2rem; color:#065F46; font-size:0.92rem;'>
      📈 <strong>Platform Completion Rate: {rate:.0f}%</strong>
      — {complete} out of {total} bookings completed
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# PROVIDER REGISTRATION REQUESTS

section_header("📬 Provider Registration Requests", "Review and approve pending provider applications")

pending_requests = db.get_all_provider_requests(status="pending")
all_requests     = db.get_all_provider_requests()

req_tab1, req_tab2 = st.tabs([
    f"🟡 Pending ({len(pending_requests)})",
    f"📋 All Requests ({len(all_requests)})"
])

with req_tab1:
    if not pending_requests:
        st.markdown(
            "<div style='text-align:center; padding:2rem; color:#64748B;'>"
            "✅ No pending requests.</div>",
            unsafe_allow_html=True,
        )
    for req in pending_requests:
        with st.expander(
            f"🟡 **{req['name']}** | {req['service_type'].title()} | "
            f"{req['location']} | Rs.{req['hourly_rate']}/hr | {req['created_at']}"
        ):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(
                    f"""
                    <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;
                                background:#F8FAFC; border-radius:10px; padding:1rem;'>
                      <div><span style='color:#64748B;font-size:0.8rem;'>👤 Name</span><br>
                        <strong>{req['name']}</strong></div>
                      <div><span style='color:#64748B;font-size:0.8rem;'>📧 Email</span><br>
                        <strong>{req['email']}</strong></div>
                      <div><span style='color:#64748B;font-size:0.8rem;'>📞 Phone</span><br>
                        <strong>{req['phone']}</strong></div>
                      <div><span style='color:#64748B;font-size:0.8rem;'>🔧 Service</span><br>
                        <strong>{req['service_type'].title()}</strong></div>
                      <div><span style='color:#64748B;font-size:0.8rem;'>💼 Experience</span><br>
                        <strong>{req['experience']} years</strong></div>
                      <div><span style='color:#64748B;font-size:0.8rem;'>💰 Rate</span><br>
                        <strong>Rs.{req['hourly_rate']}/hr</strong></div>
                      <div style='grid-column:1/-1;'>
                        <span style='color:#64748B;font-size:0.8rem;'>📍 Location</span><br>
                        <strong>{req['location']}</strong></div>
                      <div style='grid-column:1/-1;'>
                        <span style='color:#64748B;font-size:0.8rem;'>📝 Description</span><br>
                        {req['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c2:
                if st.button("✅ Approve", key=f"approve_{req['id']}", use_container_width=True):
                    result = db.process_provider_request(req["id"], "approved")
                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])

                st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
                if st.button("❌ Reject", key=f"reject_{req['id']}", use_container_width=True):
                    result = db.process_provider_request(req["id"], "rejected")
                    if result["success"]:
                        st.warning(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])

with req_tab2:
    if not all_requests:
        st.info("No requests yet.")
    else:
        import pandas as pd
        df_req = pd.DataFrame(all_requests)
        df_req_display = df_req[[
            "name", "email", "service_type",
            "location", "hourly_rate", "status", "created_at"
        ]].copy()
        df_req_display.columns = [
            "Name", "Email", "Service",
            "Location", "Rate (Rs./hr)", "Status", "Submitted"
        ]
        st.dataframe(df_req_display, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# ALL PROVIDERS TABLE

section_header("🔧 All Service Providers", "Registered providers on the platform")

providers = db.get_all_providers()

if providers:
    df_providers = pd.DataFrame(providers)

    df_display = df_providers[[
        "name", "service_type", "experience",
        "hourly_rate", "location",
        "average_rating", "review_count", "is_available"
    ]].copy()

    df_display.columns = [
        "Name", "Service", "Experience (yrs)",
        "Rate (Rs./hr)", "Location",
        "Avg Rating", "Reviews", "Available"
    ]

    df_display["Available"] = df_display["Available"].apply(
        lambda x: "✅ Yes" if x else "❌ No"
    )

    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.info("No providers found.")

st.markdown("<br>", unsafe_allow_html=True)

# CHARTS

section_header("📊 Analytics", "Visual breakdown of platform data")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown(
        "<div style='background:white; border:1px solid #E2E8F0; border-radius:12px;"
        " padding:1rem; box-shadow:0 1px 4px rgba(0,0,0,0.05);'>",
        unsafe_allow_html=True,
    )
    st.markdown("**🔧 Providers by Service Type**")
    if providers:
        df_p = pd.DataFrame(providers)
        service_counts = df_p["service_type"].value_counts().reset_index()
        service_counts.columns = ["Service", "Count"]
        service_counts = service_counts.set_index("Service")
        st.bar_chart(service_counts)
    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:
    st.markdown(
        "<div style='background:white; border:1px solid #E2E8F0; border-radius:12px;"
        " padding:1rem; box-shadow:0 1px 4px rgba(0,0,0,0.05);'>",
        unsafe_allow_html=True,
    )
    st.markdown("**⭐ Average Rating by Service Type**")
    if providers:
        df_p = pd.DataFrame(providers)
        avg_ratings = df_p.groupby("service_type")["average_rating"].mean().reset_index()
        avg_ratings.columns = ["Service", "Avg Rating"]
        avg_ratings = avg_ratings.set_index("Service")
        st.bar_chart(avg_ratings)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ALL BOOKINGS TABLE

section_header("📋 All Bookings", "Platform-wide booking history")

all_bookings = []
for p in providers:
    bookings = db.get_provider_bookings(p["id"])
    for b in bookings:
        b["provider_name"] = p["name"]
        all_bookings.append(b)

if all_bookings:
    df_bookings = pd.DataFrame(all_bookings)

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "pending", "accepted", "completed", "rejected", "cancelled"]
    )

    if status_filter != "All":
        df_bookings = df_bookings[df_bookings["status"] == status_filter]

    df_b_display = df_bookings[[
        "id", "customer_name", "provider_name",
        "service_type", "booking_date", "status"
    ]].copy()

    df_b_display.columns = [
        "ID", "Customer", "Provider",
        "Service", "Date", "Status"
    ]

    st.dataframe(df_b_display, use_container_width=True, hide_index=True)
    st.markdown(
        f"<p style='font-size:0.83rem; color:#64748B;'>Showing <strong>{len(df_b_display)}</strong> booking(s)</p>",
        unsafe_allow_html=True,
    )
else:
    st.info("No bookings found.")

st.markdown("<br>", unsafe_allow_html=True)

# ALL REVIEWS TABLE

section_header("⭐ All Reviews", "Customer reviews submitted across all providers")

all_reviews = []
for p in providers:
    reviews = db.get_provider_reviews(p["id"])
    for r in reviews:
        r["provider_name"] = p["name"]
    all_reviews.extend(reviews)


if all_reviews:
    df_reviews = pd.DataFrame(all_reviews)

    df_r_display = df_reviews[[
        "customer_name", "provider_name",
        "service_type", "rating", "review_text", "created_at"
    ]].copy()

    df_r_display.columns = [
        "Customer", "Provider",
        "Service", "Rating", "Review", "Date"
    ]

    st.dataframe(df_r_display, use_container_width=True, hide_index=True)
    st.markdown(
        f"<p style='font-size:0.83rem; color:#64748B;'>Total <strong>{len(df_r_display)}</strong> review(s)</p>",
        unsafe_allow_html=True,
    )
else:
    st.info("No reviews found.")
