import streamlit as st

st.title("🔧 Provider Profile")
st.markdown("---")

# ==========================================
# CHECKS
# ==========================================
if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "provider":
    st.warning("⚠️ Please login as a **Service Provider** to view your profile.")
    st.stop()

db = st.session_state.db
user = st.session_state.user_data

# Refresh user data from database
fresh_user = db.get_user_by_id(user["id"])
if fresh_user:
    user = fresh_user
    st.session_state.user_data = user

# Get profile from database
profile = db.get_provider_profile(user["id"])

# ==========================================
# PROFILE DISPLAY
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Personal Information")
    st.write(f"**👤 Name:** {user['name']}")
    st.write(f"**📧 Email:** {user['email']}")
    st.write(f"**📞 Phone:** {user['phone']}")
    st.write(f"**🔑 Role:** Service Provider")

    if profile:
        st.markdown("---")
        st.subheader("🔧 Service Details")
        st.write(f"**📂 Service Type:** {profile['service_type'].title()}")
        st.write(f"**💼 Experience:** {profile['experience']} years")
        st.write(f"**💰 Hourly Rate:** Rs.{profile['hourly_rate']}")
        st.write(f"**📍 Location:** {profile['location']}")
        st.write(f"**📝 Description:** {profile['description']}")

        availability = "🟢 Available" if profile["is_available"] else "🔴 Unavailable"
        st.write(f"**📊 Status:** {availability}")

with col2:
    st.subheader("📊 Statistics")

    # Get stats from database
    avg_rating = db.get_provider_average_rating(user["id"])
    reviews = db.get_provider_reviews(user["id"])
    all_bookings = db.get_provider_bookings(user["id"])
    earnings = db.get_provider_earnings(user["id"])

    completed_count = len(
        [b for b in all_bookings if b["status"] == "completed"]
    )
    pending_count = len(
        [b for b in all_bookings if b["status"] == "pending"]
    )

    st.metric("⭐ Average Rating", f"{avg_rating}/5")
    st.metric("📝 Total Reviews", len(reviews))
    st.metric("📋 Total Bookings", len(all_bookings))
    st.metric("✅ Completed Jobs", completed_count)
    st.metric("🟡 Pending Requests", pending_count)
    st.metric("💰 Total Earnings", f"Rs.{earnings}")

st.markdown("---")

# ==========================================
# EDIT PROFILE
# ==========================================
if profile:
    st.subheader("✏️ Edit Profile")

    with st.form("edit_provider_profile"):
        st.markdown("**👤 Personal Details**")
        new_name = st.text_input("Name", value=user["name"])
        new_phone = st.text_input("Phone", value=user["phone"])

        st.markdown("---")
        st.markdown("**🔧 Service Details**")

        service_options = [
            "plumbing", "carpentry", "electrical", "painting", "cleaning"
        ]

        # Get current service index
        current_service = profile["service_type"]
        if current_service in service_options:
            current_index = service_options.index(current_service)
        else:
            current_index = 0

        new_service = st.selectbox(
            "Service Type",
            service_options,
            index=current_index
        )
        new_experience = st.number_input(
            "Experience (years)",
            min_value=0,
            max_value=50,
            value=profile["experience"]
        )
        new_rate = st.number_input(
            "Hourly Rate (Rs.)",
            min_value=100,
            max_value=10000,
            value=int(profile["hourly_rate"])
        )
        new_location = st.text_input(
            "Location",
            value=profile["location"]
        )
        new_description = st.text_area(
            "Description",
            value=profile["description"]
        )
        new_availability = st.checkbox(
            "✅ Available for bookings",
            value=profile["is_available"]
        )

        submitted = st.form_submit_button(
            "💾 Save All Changes", use_container_width=True
        )

        if submitted:
            errors = []
            if not new_name or len(new_name) < 2:
                errors.append("Name must be at least 2 characters.")
            if not new_phone or len(new_phone) < 10:
                errors.append("Enter a valid phone number.")
            if not new_location:
                errors.append("Location is required.")
            if not new_description:
                errors.append("Description is required.")

            if errors:
                for e in errors:
                    st.error(f"❌ {e}")
            else:
                # Update personal info
                db.update_user(
                    user["id"],
                    name=new_name,
                    phone=new_phone
                )

                # Update session data
                st.session_state.user_data["name"] = new_name
                st.session_state.user_data["phone"] = new_phone

                # Update provider profile
                result = db.update_provider_profile(
                    user["id"],
                    service_type=new_service,
                    experience=new_experience,
                    hourly_rate=float(new_rate),
                    location=new_location,
                    description=new_description,
                    is_available=new_availability
                )

                if result["success"]:
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")

else:
    # No profile exists - create one
    st.subheader("⚠️ Create Your Profile")
    st.warning("You don't have a service profile yet. Create one below!")

    with st.form("create_profile_form"):
        service_type = st.selectbox(
            "Service Type *",
            ["plumbing", "carpentry", "electrical", "painting", "cleaning"]
        )
        experience = st.number_input(
            "Experience (years) *",
            min_value=0,
            max_value=50,
            value=1
        )
        hourly_rate = st.number_input(
            "Hourly Rate (Rs.) *",
            min_value=100,
            max_value=10000,
            value=500
        )
        location = st.text_input("Service Location *")
        description = st.text_area(
            "Describe Your Service *",
            placeholder="Tell customers about your skills..."
        )

        if st.form_submit_button(
            "🔧 Create Profile", use_container_width=True
        ):
            if not location or not description:
                st.error("❌ Please fill all required fields!")
            else:
                result = db.create_provider_profile(
                    user["id"],
                    service_type,
                    experience,
                    float(hourly_rate),
                    location,
                    description
                )
                if result["success"]:
                    st.success("✅ Profile created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")

st.markdown("---")

# ==========================================
# CHANGE PASSWORD
# ==========================================
st.subheader("🔒 Change Password")

with st.form("provider_change_password"):
    old_pass = st.text_input(
        "Current Password", type="password",
        key="prov_old"
    )
    new_pass = st.text_input(
        "New Password", type="password",
        key="prov_new"
    )
    confirm_pass = st.text_input(
        "Confirm New Password", type="password",
        key="prov_confirm"
    )

    if st.form_submit_button(
        "🔒 Change Password", use_container_width=True
    ):
        if not old_pass or not new_pass or not confirm_pass:
            st.error("❌ Please fill all fields!")
        elif new_pass != confirm_pass:
            st.error("❌ New passwords don't match!")
        elif len(new_pass) < 6:
            st.error("❌ Password must be at least 6 characters!")
        elif old_pass == new_pass:
            st.error("❌ New password must be different!")
        else:
            result = db.change_password(user["id"], old_pass, new_pass)
            if result["success"]:
                st.success("✅ Password changed successfully!")
            else:
                st.error(
                    f"❌ {result.get('message', 'Wrong current password!')}"
                )

st.markdown("---")

# ==========================================
# QUICK REVIEW SUMMARY
# ==========================================
st.subheader("⭐ Recent Reviews")

reviews = db.get_provider_reviews(user["id"])

if not reviews:
    st.info("📝 No reviews yet. Complete jobs to receive reviews!")
else:
    # Show last 5 reviews
    recent_reviews = reviews[:5]

    for r in recent_reviews:
        stars = "⭐" * r["rating"]
        st.write(
            f"{stars} | **{r['customer_name']}** | "
            f"*\"{r['review_text'][:60]}...\"* | "
            f"{r['created_at']}"
        )

    if len(reviews) > 5:
        st.info(
            f"Showing 5 of {len(reviews)} reviews. "
            f"Go to ⭐ Provider Reviews for full list."
        )