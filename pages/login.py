import streamlit as st

st.title("🔑 Login")
st.markdown("---")

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

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
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

    st.markdown("---")
    st.info(
        "**Test Accounts:**\n\n"
        "Customer: `ashan@email.com` / `pass123`\n\n"
        "Provider: `kamal@email.com` / `pass123`"
    )

    # ==========================================
    # REGISTER LINK
    # ==========================================
    st.markdown("---")
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown("**Don't have an account?**")
        if st.button("📝 Register Here", use_container_width=True):
            st.switch_page("pages/register.py")

    # ==========================================
    # ADMIN ACCESS
    # ==========================================
    st.markdown("---")
    col_a1, col_a2, col_a3 = st.columns([1, 2, 1])
    with col_a2:
        if st.button("🛡️ Admin Login", use_container_width=True):
            st.switch_page("pages/admin.py")
