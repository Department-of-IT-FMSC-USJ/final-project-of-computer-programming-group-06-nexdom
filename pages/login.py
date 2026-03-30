import streamlit as st
from pages.style import inject_global_css, page_banner

inject_global_css()

st.markdown(
    """
    <style>
    /* centre the login card */
    .login-wrap { max-width: 440px; margin: 0 auto; }
    .login-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 2rem 2rem 1.5rem 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

db = st.session_state.db

if st.session_state.get("logged_in"):
    st.success(f"✅ Logged in as **{st.session_state.user_data['name']}**")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.user_role = None
        st.rerun()
    st.stop()

# Banner
page_banner(
    title="Welcome Back",
    subtitle="Sign in to your NEXDOM account to continue.",
    icon="🔑",
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='text-align:center; color:#0F172A; margin-bottom:1.2rem;'>🔑 Sign In</h3>",
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        email    = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        role     = st.selectbox("👤 Login As", ["customer", "provider"])

        if st.form_submit_button("🔑 Login", use_container_width=True):
            if not email or not password:
                st.error("❌ Fill all fields!")
            else:
                result = db.authenticate_user(email, password, role)
                if result["success"]:
                    st.session_state.logged_in = True
                    st.session_state.user_data = result["user"]
                    st.session_state.user_role = role
                    st.success(f"✅ Welcome, {result['user']['name']}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Test credentials hint
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px;
                    padding:0.9rem 1rem; font-size:0.83rem; color:#475569;'>
          <div style='font-weight:700; margin-bottom:6px; color:#0F172A;'>🔑 Test Accounts</div>
          <div>Customer: <code>ashan@email.com</code> / <code>pass123</code></div>
          <div style='margin-top:4px;'>Provider: <code>kamal@email.com</code> / <code>pass123</code></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Register link
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown(
            "<p style='text-align:center; color:#64748B; font-size:0.85rem;'>"
            "Don't have an account?</p>",
            unsafe_allow_html=True,
        )
        if st.button("📝 Register Here", use_container_width=True):
            st.switch_page("pages/register.py")

    # Admin link
    col_a1, col_a2, col_a3 = st.columns([1, 2, 1])
    with col_a2:
        st.markdown(
            "<p style='text-align:center; color:#64748B; font-size:0.85rem; margin-top:0.5rem;'>"
            "Admin access?</p>",
            unsafe_allow_html=True,
        )
        if st.button("🛡️ Admin Login", use_container_width=True):
            st.switch_page("pages/admin.py")
