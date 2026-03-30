import streamlit as st
from pages.style import inject_global_css, section_header, page_banner

inject_global_css()

page_banner(
    title="Customer Profile",
    subtitle="Manage your personal information and track activity.",
    icon="👤",
)

# CHECKS

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "customer":
    st.warning("⚠️ Please login as a **Customer** to view your profile.")
    st.stop()

db   = st.session_state.db
user = st.session_state.user_data

# Refresh user data from database
fresh_user = db.get_user_by_id(user["id"])
if fresh_user:
    user = fresh_user
    st.session_state.user_data = user

# PROFILE INFO & STATS

section_header("👤 Profile Overview")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        f"""
        <div style='background:white; border:1px solid #E2E8F0; border-radius:14px;
                    padding:1.5rem; box-shadow:0 1px 6px rgba(0,0,0,0.06);'>
          <div style='display:flex; align-items:center; gap:1rem; margin-bottom:1rem;'>
            <div style='background:linear-gradient(135deg,#1A56DB,#60A5FA); width:56px; height:56px;
                        border-radius:50%; display:flex; align-items:center; justify-content:center;
                        font-size:1.5rem; color:white; font-weight:700; flex-shrink:0;'>
              {user['name'][0].upper()}
            </div>
            <div>
              <div style='font-size:1.1rem; font-weight:700; color:#0F172A;'>{user['name']}</div>
              <div style='font-size:0.8rem; color:#64748B;'>{user['email']}</div>
            </div>
          </div>
          <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.8rem;'>
            <div style='background:#F8FAFC; border-radius:8px; padding:0.6rem 0.8rem;'>
              <div style='font-size:0.72rem; color:#64748B; font-weight:600;
                          text-transform:uppercase;'>📞 Phone</div>
              <div style='font-weight:600; color:#0F172A; margin-top:2px;'>{user['phone']}</div>
            </div>
            <div style='background:#F8FAFC; border-radius:8px; padding:0.6rem 0.8rem;'>
              <div style='font-size:0.72rem; color:#64748B; font-weight:600;
                          text-transform:uppercase;'>📍 Address</div>
              <div style='font-weight:600; color:#0F172A; margin-top:2px;'>{user['address'] or "—"}</div>
            </div>
            <div style='background:#EFF6FF; border-radius:8px; padding:0.6rem 0.8rem;
                        border:1px solid #BFDBFE;'>
              <div style='font-size:0.72rem; color:#1D4ED8; font-weight:600;
                          text-transform:uppercase;'>🔑 Role</div>
              <div style='font-weight:700; color:#1D4ED8; margin-top:2px;'>
                {user['role'].title()}
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    bookings = db.get_customer_bookings(user["id"])
    reviews  = db.get_customer_reviews(user["id"])

    total_bookings     = len(bookings)
    completed_bookings = len([b for b in bookings if b["status"] == "completed"])
    pending_bookings   = len([b for b in bookings if b["status"] == "pending"])
    total_reviews      = len(reviews)

    stat_data = [
        ("📋 Total Bookings", total_bookings,     "#1A56DB"),
        ("✅ Completed",       completed_bookings, "#10B981"),
        ("🟡 Pending",         pending_bookings,   "#F59E0B"),
        ("⭐ Reviews Given",   total_reviews,      "#7C3AED"),
    ]
    for label, val, color in stat_data:
        st.markdown(
            f"""
            <div style='background:white; border:1px solid #E2E8F0; border-radius:10px;
                        padding:0.7rem 0.9rem; margin-bottom:0.5rem;
                        box-shadow:0 1px 3px rgba(0,0,0,0.05);
                        border-left:4px solid {color};
                        display:flex; align-items:center; justify-content:space-between;'>
              <span style='font-size:0.78rem; font-weight:600; color:#64748B;'>{label}</span>
              <span style='font-size:1.2rem; font-weight:800; color:{color};'>{val}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# EDIT PROFILE

section_header("✏️ Edit Profile", "Update your personal information")

with st.form("edit_customer_profile"):
    new_name    = st.text_input("Full Name", value=user["name"])
    new_phone   = st.text_input("Phone Number", value=user["phone"])
    new_address = st.text_input("Address", value=user["address"])

    submitted = st.form_submit_button(
        "💾 Save Changes", use_container_width=True
    )

    if submitted:
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
                    st.session_state.user_data["name"]    = new_name
                    st.session_state.user_data["phone"]   = new_phone
                    st.session_state.user_data["address"] = new_address
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")

st.markdown("<br>", unsafe_allow_html=True)

# CHANGE PASSWORD

section_header("🔒 Change Password", "Keep your account secure")

with st.form("change_password_form"):
    old_password     = st.text_input("Current Password",    type="password", key="old_pass")
    new_password     = st.text_input("New Password",        type="password", key="new_pass")
    confirm_password = st.text_input("Confirm New Password",type="password", key="confirm_pass")

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

st.markdown("<br>", unsafe_allow_html=True)

# REVIEWS I'VE GIVEN

section_header("⭐ Reviews I've Given", "Your past service feedback")

reviews = db.get_customer_reviews(user["id"])

if not reviews:
    st.info("📝 You haven't written any reviews yet. Complete a booking and leave a review!")
else:
    st.markdown(
        f"<p style='color:#64748B; font-size:0.85rem;'><strong>{len(reviews)}</strong> review(s) written</p>",
        unsafe_allow_html=True,
    )

    for review in reviews:
        stars       = "⭐" * review["rating"]
        label_color = "#15803D" if review["rating"] >= 4 else ("#CA8A04" if review["rating"] == 3 else "#B91C1C")

        with st.expander(
            f"{stars} | {review['provider_name']} | "
            f"{review['service_type'].title()} | {review['created_at']}"
        ):
            r_col1, r_col2 = st.columns([3, 1])

            with r_col1:
                st.markdown(
                    f"""
                    <div style='background:#F8FAFC; border-radius:10px; padding:0.9rem;
                                border:1px solid #E2E8F0;'>
                      <div><span style='color:#64748B;font-size:0.78rem;'>🔧 Provider</span>
                        <div style='font-weight:600;'>{review['provider_name']}</div></div>
                      <div style='margin-top:0.5rem;'>
                        <span style='color:#64748B;font-size:0.78rem;'>📂 Service</span>
                        <div style='font-weight:600;'>{review['service_type'].title()}</div></div>
                      <div style='margin-top:0.5rem;'>
                        <span style='color:#64748B;font-size:0.78rem;'>📅 Date</span>
                        <div style='font-weight:600;'>{review['created_at']}</div></div>
                      <div style='margin-top:0.8rem; font-style:italic; color:#475569;'>
                        "{review['review_text']}"
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with r_col2:
                st.markdown(
                    f"""
                    <div style='text-align:center; background:white; border:2px solid {label_color};
                                border-radius:12px; padding:1rem;'>
                      <div style='font-size:1.8rem;'>{stars[:2]}</div>
                      <div style='font-size:1.4rem; font-weight:800; color:{label_color};'>
                        {review['rating']}/5
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

st.markdown("<br>", unsafe_allow_html=True)

# RECENT BOOKINGS SUMMARY

section_header("📋 Recent Bookings", "Your 5 most recent service bookings")

bookings = db.get_customer_bookings(user["id"])

if not bookings:
    st.info("No bookings yet.")
else:
    recent = bookings[:5]

    STATUS_STYLE = {
        "pending":   ("#FEF9C3", "#CA8A04",  "🟡"),
        "accepted":  ("#DCFCE7", "#15803D",  "🟢"),
        "rejected":  ("#FEE2E2", "#B91C1C",  "🔴"),
        "completed": ("#EFF6FF", "#1D4ED8",  "✅"),
        "cancelled": ("#F1F5F9", "#475569",  "⚫"),
    }

    for b in recent:
        bg, color, icon = STATUS_STYLE.get(b["status"], ("#F8FAFC", "#94A3B8", "⚪"))
        st.markdown(
            f"""
            <div style='background:{bg}; border-left:4px solid {color}; border-radius:8px;
                        padding:0.6rem 0.9rem; margin-bottom:0.5rem;
                        display:flex; align-items:center; justify-content:space-between;'>
              <div>
                <span style='font-weight:700; color:#0F172A;'>{icon} #{b['id']}</span>
                <span style='margin-left:0.5rem; color:#475569;'>
                  {b['provider_name']} · {b['service_type'].title()} · {b['booking_date']}
                </span>
              </div>
              <span style='font-size:0.72rem; font-weight:700; color:{color};
                           text-transform:uppercase; background:{color}22;
                           padding:2px 8px; border-radius:20px;'>
                {b['status']}
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if len(bookings) > 5:
        st.info(
            f"Showing 5 of {len(bookings)} bookings. "
            f"Go to 📋 My Bookings for full list."
        )