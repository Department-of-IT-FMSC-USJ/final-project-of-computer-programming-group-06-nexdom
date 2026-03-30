import streamlit as st

db = st.session_state.db

st.title("🏠 NEXDOM — Home Service Provider Platform")
st.markdown("### Find Trusted Providers for Your Household Needs!")
st.markdown("---")

# Services
st.subheader("🔧 Our Services")

st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        padding: 20px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        border: 1px solid #ddd;
        background-color: #5B9BD5;
        color: white;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #4178B0;
        color: white;
        border: 1px solid #4178B0;
    }
    </style>
""", unsafe_allow_html=True)

services_display = [
    ("🔧", "Plumbing",   "#E3F2FD", "plumbing"),
    ("🪚", "Carpentry",  "#FFF3E0", "carpentry"),
    ("⚡", "Electrical", "#FFF9C4", "electrical"),
    ("🎨", "Painting",   "#F3E5F5", "painting"),
    ("🧹", "Cleaning",   "#E8F5E9", "cleaning"),
]

col1, col2, col3, col4, col5 = st.columns(5)

for col, (icon, name, color, key) in zip(
    [col1, col2, col3, col4, col5], services_display
):
    with col:
        st.markdown(
            f"<div style='text-align:center; padding:15px; "
            f"background-color:{color}; border-radius:10px; margin-bottom:5px;'>"
            f"<h2>{icon}</h2><h4>{name}</h4></div>",
            unsafe_allow_html=True
        )
        if st.button(f"View", key=f"svc_{key}", use_container_width=True):
            if not st.session_state.get("logged_in"):
                st.warning("⚠️ Please login first to search services!")
                st.switch_page("pages/login.py")
            elif st.session_state.get("user_role") != "customer":
                st.warning("⚠️ Only customers can search services!")
            else:
                st.session_state.selected_service = key
                st.switch_page("pages/search_services.py")


# Platform stats
stats = db.get_platform_stats()
st.subheader("📊 Platform Statistics")
s1, s2, s3, s4 = st.columns(4)
s1.metric("🔧 Providers", stats.get("total_providers", 0))
s2.metric("👥 Customers", stats.get("total_customers", 0))
s3.metric("⭐ Reviews",   stats.get("total_reviews", 0))
s4.metric("📋 Bookings",  stats.get("total_bookings", 0))

st.markdown("---")

# Top providers
st.subheader("🏆 Top Rated Providers")
all_providers = db.get_all_providers()
sorted_providers = sorted(
    all_providers, key=lambda p: p["average_rating"], reverse=True
)

top_cols = st.columns(3)
medals = ["🥇", "🥈", "🥉"]

for i, col in enumerate(top_cols):
    if i < len(sorted_providers):
        p = sorted_providers[i]
        with col:
            st.markdown(
                f"<div style='text-align:center; padding:15px; "
                f"border:2px solid #ddd; border-radius:10px;'>"
                f"<h2>{medals[i]}</h2>"
                f"<h4>{p['name']}</h4>"
                f"<p>{p['service_type'].title()}</p>"
                f"<h3>{p['average_rating']} ⭐</h3>"
                f"<p>{p['review_count']} reviews</p></div>",
                unsafe_allow_html=True
            )

st.markdown("---")
st.info(
    "🤖 Our ChatBot analyzes reviews using **sentiment analysis** "
    "to recommend the best provider! Login as a customer to try it."
)