import streamlit as st
from database.db_operations import DatabaseManager

# ==========================================
# PAGE CONFIG — only here, nowhere else
# ==========================================
st.set_page_config(
    page_title="NEXDOM",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# INITIALIZE DATABASE & SESSION STATE
# ==========================================
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()
    seeded = st.session_state.db.seed_sample_data()
    if seeded:
        print("✅ Sample data loaded!")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None
    st.session_state.user_role = None
    st.session_state.chat_history = []

# ==========================================
# ROLE-BASED NAVIGATION
# ==========================================
role = st.session_state.get("user_role")
logged_in = st.session_state.get("logged_in", False)

# Pages visible to everyone (not logged in)
public_pages = [
    st.Page("pages/landing.py",  title="Home",     icon="🏠", default=True),
    st.Page("pages/login.py",    title="Login",    icon="🔑"),
    st.Page("pages/register.py", title="Register", icon="📝"),
    st.Page("pages/admin.py",    title="Admin",    icon="🛡️"),
]


# Customer pages
customer_pages = [
    st.Page("pages/landing.py",         title="Home",            icon="🏠", default=True),
    st.Page("pages/search_services.py", title="Search Services", icon="🔍"),
    st.Page("pages/mybookings.py",       title="My Bookings",     icon="📋"),
    st.Page("pages/chatbot.py",          title="ChatBot",         icon="🤖"),
    st.Page("pages/customer_profile.py", title="My Profile",      icon="👤"),
]

# Provider pages
provider_pages = [
    st.Page("pages/landing.py",           title="Home",              icon="🏠", default=True),
    st.Page("pages/bookings_request.py",  title="Booking Requests",  icon="📋"),
    st.Page("pages/provider_profile.py",  title="My Profile",        icon="🔧"),
    st.Page("pages/provider_reviews.py",  title="My Reviews",        icon="⭐"),
    st.Page("pages/provider_earnings.py", title="My Earnings",       icon="📊"),
]

# Admin pages
admin_pages = [
    st.Page("pages/landing.py", title="🏠 Home",            icon="🏠", default=True),
    st.Page("pages/admin.py",   title="🛡️ Admin Dashboard", icon="🛡️"),
]

# Pick which pages to show
if not logged_in:
    pages = public_pages
elif role == "customer":
    pages = customer_pages
elif role == "provider":
    pages = provider_pages
else:
    pages = public_pages

# ==========================================
# SIDEBAR — user info + logout
# ==========================================
st.sidebar.title("🏠 NEXDOM")
st.sidebar.markdown("---")

if logged_in and st.session_state.user_data:
    st.sidebar.success(
        f"👤 **{st.session_state.user_data['name']}**\n\n"
        f"Role: {st.session_state.user_role.upper()}"
    )
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.user_role = None
        st.session_state.chat_history = []
        st.rerun()
else:
    st.sidebar.info("Please login to access all features.")


# ==========================================
# RUN NAVIGATION
# ==========================================
pg = st.navigation(pages, position="sidebar")
pg.run()
