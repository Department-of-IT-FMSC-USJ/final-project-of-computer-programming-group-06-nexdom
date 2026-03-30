import streamlit as st
from pages.style import inject_global_css, page_banner

inject_global_css()

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

db = st.session_state.db

page_banner(
    title="Create Your Account",
    subtitle="Join NEXDOM and connect with trusted home service professionals.",
    icon="📝",
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(
        "<div style='background:white; border:1px solid #E2E8F0; border-radius:16px;"
        " padding:2rem; box-shadow:0 4px 20px rgba(0,0,0,0.08);'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align:center; color:#0F172A; margin-bottom:1rem;'>📝 Sign Up</h3>",
        unsafe_allow_html=True,
    )

    role = st.selectbox("👤 Register As", ["customer", "provider"])
    address = ""

    with st.form("register_form"):
        name     = st.text_input("Full Name *")
        email    = st.text_input("Email *")
        password = st.text_input("Password *", type="password")
        confirm  = st.text_input("Confirm Password *", type="password")
        phone    = st.text_input("Phone *")

        if role == "customer":
            address = st.text_input("Address *")

        if role == "provider":
            st.markdown(
                """
                <div style='background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px;
                            padding:0.7rem 1rem; margin:0.5rem 0; font-size:0.85rem; color:#1E40AF;'>
                  📋 Provider registrations require <strong>admin approval</strong>
                  before you can log in.
                </div>
                """,
                unsafe_allow_html=True,
            )
            service_type = st.selectbox(
                "Service *",
                ["plumbing", "carpentry", "electrical", "painting", "cleaning"]
            )
            experience  = st.number_input("Experience (years)", 0, 50, 1)
            hourly_rate = st.number_input("Rate (Rs./hr)", 100, 10000, 500)
            location    = st.text_input("Location *")
            description = st.text_area("Description *")

        if st.form_submit_button("📝 Register", use_container_width=True):
            errors = []
            if not name:
                errors.append("Name required")
            if not email or "@" not in email:
                errors.append("Valid email required")
            if len(password) < 6:
                errors.append("Password min 6 chars")
            if password != confirm:
                errors.append("Passwords don't match")
            if not phone:
                errors.append("Phone required")

            if errors:
                for e in errors:
                    st.error(f"❌ {e}")
            else:
                if role == "customer":
                    result = db.create_user(
                        name, email, password, phone, role, address
                    )
                    if result["success"]:
                        st.success("✅ Registered successfully! Please login.")
                        st.balloons()
                    else:
                        st.error(f"❌ {result['message']}")

                elif role == "provider":
                    result = db.create_provider_request(
                        name, email, password, phone,
                        service_type, experience, hourly_rate,
                        location, description
                    )
                    if result["success"]:
                        st.success(
                            "✅ Registration request submitted! "
                            "Please wait for **admin approval** before logging in."
                        )
                        st.balloons()
                    else:
                        st.error(f"❌ {result['message']}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown(
            "<p style='text-align:center; color:#64748B; font-size:0.85rem;'>"
            "Already have an account?</p>",
            unsafe_allow_html=True,
        )
        if st.button("🔑 Login Here", use_container_width=True):
            st.switch_page("pages/login.py")