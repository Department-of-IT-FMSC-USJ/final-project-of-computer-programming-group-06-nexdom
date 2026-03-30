import streamlit as st
import pandas as pd

st.title("🛡️ Admin Dashboard")
st.markdown("---")

# ==========================================
# CHECKS
# ==========================================
if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

# ==========================================
# SIMPLE ADMIN PASSWORD GATE
# ==========================================
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.subheader("🔒 Admin Login")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("admin_login"):
            admin_pass = st.text_input("Admin Password", type="password")
            if st.form_submit_button("🔑 Login", use_container_width=True):
                if admin_pass == "admin123":
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Wrong password!")
    st.stop()

db = st.session_state.db

# Logout button
if st.button("🚪 Exit Admin"):
    st.session_state.admin_authenticated = False
    st.rerun()

# ==========================================
# PLATFORM STATISTICS
# ==========================================
st.subheader("📊 Platform Overview")

stats = db.get_platform_stats()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🔧 Providers",    stats.get("total_providers", 0))
c2.metric("👥 Customers",    stats.get("total_customers", 0))
c3.metric("📋 Bookings",     stats.get("total_bookings", 0))
c4.metric("✅ Completed",    stats.get("completed_bookings", 0))
c5.metric("⭐ Reviews",      stats.get("total_reviews", 0))

# Completion rate
total    = stats.get("total_bookings", 0)
complete = stats.get("completed_bookings", 0)
rate     = (complete / total * 100) if total > 0 else 0
st.info(f"📈 **Platform Completion Rate: {rate:.0f}%** — {complete} out of {total} bookings completed")

st.markdown("---")

# ==========================================
# ALL PROVIDERS TABLE
# ==========================================
st.subheader("🔧 All Service Providers")

providers = db.get_all_providers()

if providers:
    df_providers = pd.DataFrame(providers)

    # Select and rename columns for clean display
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

st.markdown("---")

# ==========================================
# CHARTS
# ==========================================
st.subheader("📊 Analytics")

chart_col1, chart_col2 = st.columns(2)

# --- Chart 1: Providers by Service Type ---
with chart_col1:
    st.markdown("**🔧 Providers by Service Type**")
    if providers:
        df_p = pd.DataFrame(providers)
        service_counts = df_p["service_type"].value_counts().reset_index()
        service_counts.columns = ["Service", "Count"]
        service_counts = service_counts.set_index("Service")
        st.bar_chart(service_counts)

# --- Chart 2: Average Rating by Service Type ---
with chart_col2:
    st.markdown("**⭐ Average Rating by Service Type**")
    if providers:
        df_p = pd.DataFrame(providers)
        avg_ratings = df_p.groupby("service_type")["average_rating"].mean().reset_index()
        avg_ratings.columns = ["Service", "Avg Rating"]
        avg_ratings = avg_ratings.set_index("Service")
        st.bar_chart(avg_ratings)

st.markdown("---")

# ==========================================
# ALL BOOKINGS TABLE
# ==========================================
st.subheader("📋 All Bookings")

# Collect all bookings across all providers
all_bookings = []
for p in providers:
    bookings = db.get_provider_bookings(p["id"])
    for b in bookings:
        b["provider_name"] = p["name"]
        all_bookings.append(b)

if all_bookings:
    df_bookings = pd.DataFrame(all_bookings)

    # Status filter
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
    st.info(f"Showing **{len(df_b_display)}** booking(s)")
else:
    st.info("No bookings found.")

st.markdown("---")

# ==========================================
# ALL REVIEWS TABLE
# ==========================================
st.subheader("⭐ All Reviews")

all_reviews = []
for p in providers:
    reviews = db.get_provider_reviews(p["id"])
    for r in reviews:
        r["provider_name"] = p["name"]  # add provider name manually
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
    st.info(f"Total **{len(df_r_display)}** review(s)")
else:
    st.info("No reviews found.")
