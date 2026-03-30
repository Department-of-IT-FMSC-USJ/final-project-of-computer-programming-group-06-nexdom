import streamlit as st
from database.db_operations import DatabaseManager
from pages.style import inject_global_css, NEXDOM_CSS

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
# INJECT GLOBAL STYLES
# ==========================================
st.markdown(NEXDOM_CSS, unsafe_allow_html=True)

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
st.sidebar.markdown(
    """
    <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
      <div style='font-size:2.2rem;'>🏠</div>
      <div style='font-size:1.4rem; font-weight:800; color:#F8FAFC;
                  letter-spacing:-0.5px; margin-top:4px;'>NEXDOM</div>
      <div style='font-size:0.72rem; color:#94A3B8; text-transform:uppercase;
                  letter-spacing:1.5px; margin-top:2px;'>Home Services</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<hr style='border-top:1px solid #334155; margin:0.5rem 0;'>",
    unsafe_allow_html=True,
)

if logged_in and st.session_state.user_data:
    role_icons = {"customer": "👤", "provider": "🔧", "admin": "🛡️"}
    role_icon = role_icons.get(st.session_state.user_role, "👤")
    st.sidebar.markdown(
        f"""
        <div style='background:#1E3A5F; border:1px solid #1D4ED8; border-radius:10px;
                    padding:0.8rem 1rem; margin-bottom:0.8rem;'>
          <div style='font-size:1.3rem;'>{role_icon}</div>
          <div style='font-weight:700; color:#E2E8F0; font-size:0.95rem; margin-top:2px;'>
            {st.session_state.user_data['name']}
          </div>
          <div style='font-size:0.72rem; color:#93C5FD; margin-top:2px;
                      text-transform:uppercase; letter-spacing:0.5px;'>
            {st.session_state.user_role}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.user_role = None
        st.session_state.chat_history = []
        st.rerun()
else:
    st.sidebar.markdown(
        """
        <div style='background:#1E3A5F; border:1px solid #334155; border-radius:10px;
                    padding:0.8rem 1rem; margin-bottom:0.8rem; text-align:center;'>
          <div style='font-size:1.5rem;'>🔒</div>
          <div style='font-size:0.82rem; color:#94A3B8; margin-top:4px;'>
            Please login to access<br>all features.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# RUN NAVIGATION
# ==========================================
pg = st.navigation(pages, position="sidebar")
pg.run()
