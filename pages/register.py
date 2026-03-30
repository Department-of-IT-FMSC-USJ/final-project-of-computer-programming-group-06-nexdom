import streamlit as st

st.title("📝 Register")
st.markdown("---")

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

db = st.session_state.db

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    role = st.selectbox("👤 Register As", ["customer", "provider"])
    address = ""  # default value for customers

    with st.form("register_form"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        password = st.text_input("Password *", type="password")
        confirm = st.text_input("Confirm Password *", type="password")
        phone = st.text_input("Phone *")

        if role == "customer":
            address = st.text_input("Address *")

        if role == "provider":
            service_type = st.selectbox(
                "Service *",
                ["plumbing", "carpentry", "electrical", "painting", "cleaning"]
            )
            experience = st.number_input("Experience (years)", 0, 50, 1)
            hourly_rate = st.number_input("Rate (Rs./hr)", 100, 10000, 500)
            location = st.text_input("Location *")
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
                # Create user in database
                result = db.create_user(
                    name, email, password, phone, role,
                    address if role == "customer" else ""
                )

                if result["success"]:
                    # Create provider profile if provider
                    if role == "provider":
                        db.create_provider_profile(
                            result["user_id"], service_type,
                            experience, hourly_rate,
                            location, description
                        )
                    st.success("✅ Registered! Please login.")
                    st.balloons()
                else:
                    st.error(f"❌ {result['message']}")