import streamlit as st

st.title("👤 Customer Profile")
st.markdown("---")

# ==========================================
# CHECKS
# ==========================================
if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "customer":
    st.warning("⚠️ Please login as a **Customer** to view your profile.")
    st.stop()

db = st.session_state.db
user = st.session_state.user_data

# Refresh user data from database
fresh_user = db.get_user_by_id(user["id"])
if fresh_user:
    user = fresh_user
    st.session_state.user_data = user

# ==========================================
# PROFILE INFO & STATS
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Personal Information")
    st.write(f"**👤 Name:** {user['name']}")
    st.write(f"**📧 Email:** {user['email']}")
    st.write(f"**📞 Phone:** {user['phone']}")
    st.write(f"**📍 Address:** {user['address']}")
    st.write(f"**🔑 Role:** {user['role'].title()}")

with col2:
    st.subheader("📊 Statistics")

    # Get stats from database
    bookings = db.get_customer_bookings(user["id"])
    reviews = db.get_customer_reviews(user["id"])

    total_bookings = len(bookings)
    completed_bookings = len(
        [b for b in bookings if b["status"] == "completed"]
    )
    pending_bookings = len(
        [b for b in bookings if b["status"] == "pending"]
    )
    total_reviews = len(reviews)

    st.metric("📋 Total Bookings", total_bookings)
    st.metric("✅ Completed", completed_bookings)
    st.metric("🟡 Pending", pending_bookings)
    st.metric("⭐ Reviews Given", total_reviews)

st.markdown("---")

# ==========================================
# EDIT PROFILE
# ==========================================
st.subheader("✏️ Edit Profile")

with st.form("edit_customer_profile"):
    new_name = st.text_input("Full Name", value=user["name"])
    new_phone = st.text_input("Phone Number", value=user["phone"])
    new_address = st.text_input("Address", value=user["address"])

    submitted = st.form_submit_button(
        "💾 Save Changes", use_container_width=True
    )

    if submitted:
        # Validation
        errors = []
        if not new_name or len(new_name) < 2:
            errors.append("Name must be at least 2 characters.")
        if not new_phone or len(new_phone) < 10:
            errors.append("Enter a valid phone number (min 10 digits).")
        if not new_address or len(new_address) < 3:
            errors.append("Enter a valid address.")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            # Check if anything changed
            if (new_name == user["name"] and
                    new_phone == user["phone"] and
                    new_address == user["address"]):
                st.info("ℹ️ No changes detected.")
            else:
                result = db.update_user(
                    user["id"],
                    name=new_name,
                    phone=new_phone,
                    address=new_address
                )
                if result["success"]:
                    # Update session data
                    st.session_state.user_data["name"] = new_name
                    st.session_state.user_data["phone"] = new_phone
                    st.session_state.user_data["address"] = new_address
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")

st.markdown("---")

# ==========================================
# CHANGE PASSWORD
# ==========================================
st.subheader("🔒 Change Password")

with st.form("change_password_form"):
    old_password = st.text_input(
        "Current Password", type="password",
        key="old_pass"
    )
    new_password = st.text_input(
        "New Password", type="password",
        key="new_pass"
    )
    confirm_password = st.text_input(
        "Confirm New Password", type="password",
        key="confirm_pass"
    )

    pass_submitted = st.form_submit_button(
        "🔒 Change Password", use_container_width=True
    )

    if pass_submitted:
        if not old_password or not new_password or not confirm_password:
            st.error("❌ Please fill in all password fields!")
        elif new_password != confirm_password:
            st.error("❌ New passwords don't match!")
        elif len(new_password) < 6:
            st.error("❌ New password must be at least 6 characters!")
        elif old_password == new_password:
            st.error("❌ New password must be different from current!")
        else:
            result = db.change_password(
                user["id"], old_password, new_password
            )
            if result["success"]:
                st.success("✅ Password changed successfully!")
            else:
                st.error(f"❌ {result.get('message', 'Wrong current password!')}")

st.markdown("---")

# ==========================================
# REVIEWS I'VE GIVEN
# ==========================================
st.subheader("⭐ Reviews I've Given")

reviews = db.get_customer_reviews(user["id"])

if not reviews:
    st.info("📝 You haven't written any reviews yet. "
            "Complete a booking and leave a review!")
else:
    st.write(f"**Total reviews:** {len(reviews)}")
    st.markdown("---")

    for review in reviews:
        stars = "⭐" * review["rating"]

        with st.expander(
            f"{stars} | {review['provider_name']} | "
            f"{review['service_type'].title()} | "
            f"{review['created_at']}"
        ):
            r_col1, r_col2 = st.columns([3, 1])

            with r_col1:
                st.write(f"**🔧 Provider:** {review['provider_name']}")
                st.write(f"**📂 Service:** {review['service_type'].title()}")
                st.write(f"**⭐ Rating:** {review['rating']}/5 {stars}")
                st.write(f"**💬 Review:** \"{review['review_text']}\"")
                st.write(f"**📅 Date:** {review['created_at']}")

            with r_col2:
                st.markdown(
                    f"<div style='text-align:center; padding:15px; "
                    f"border:2px solid #ddd; border-radius:10px;'>"
                    f"<h1>{stars[:2]}</h1>"
                    f"<h3>{review['rating']}/5</h3></div>",
                    unsafe_allow_html=True
                )

st.markdown("---")

# ==========================================
# RECENT BOOKINGS SUMMARY
# ==========================================
st.subheader("📋 Recent Bookings")

bookings = db.get_customer_bookings(user["id"])

if not bookings:
    st.info("No bookings yet.")
else:
    # Show last 5 bookings
    recent = bookings[:5]

    status_icons = {
        "pending": "🟡",
        "accepted": "🟢",
        "rejected": "🔴",
        "completed": "✅",
        "cancelled": "⚫"
    }

    for b in recent:
        icon = status_icons.get(b["status"], "⚪")
        st.write(
            f"{icon} **Booking #{b['id']}** | "
            f"{b['provider_name']} | "
            f"{b['service_type'].title()} | "
            f"{b['booking_date']} | "
            f"**{b['status'].upper()}**"
        )

    if len(bookings) > 5:
        st.info(
            f"Showing 5 of {len(bookings)} bookings. "
            f"Go to 📋 My Bookings for full list."
        )