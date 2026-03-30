import streamlit as st
from datetime import date

st.title("🔍 Search Service Providers")
st.markdown("---")

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "customer":
    st.warning("⚠️ Login as **Customer** to search.")
    st.stop()

db = st.session_state.db
user = st.session_state.user_data

# Filters
f1, f2, f3 = st.columns(3)
with f1:
    service_options = ["All", "plumbing", "carpentry", "electrical", "painting", "cleaning"]
    preselected = st.session_state.pop("selected_service", None)
    default_index = service_options.index(preselected) if preselected in service_options else 0
    service_type = st.selectbox("Service", service_options, index=default_index)

with f2:
    sort_by = st.selectbox("Sort By", ["Rating ↓", "Rating ↑", "Price ↓", "Price ↑", "Experience ↓"])

with f3:
    location = st.text_input("Location", placeholder="e.g., Colombo")

st.markdown("---")

providers = db.get_all_providers(service_type if service_type != "All" else None)

if location:
    providers = [p for p in providers if location.lower() in p["location"].lower()]

# Sorting Logic
if sort_by == "Rating ↓": providers.sort(key=lambda p: p["average_rating"], reverse=True)
elif sort_by == "Rating ↑": providers.sort(key=lambda p: p["average_rating"])
elif sort_by == "Price ↓": providers.sort(key=lambda p: p["hourly_rate"], reverse=True)
elif sort_by == "Price ↑": providers.sort(key=lambda p: p["hourly_rate"])
elif sort_by == "Experience ↓": providers.sort(key=lambda p: p["experience"], reverse=True)

if not providers:
    st.warning("😔 No providers found.")
else:
    st.info("💡 **Note:** Rates are approximate. Final pricing may vary depend on the scope, materials required, and complexity of the task.")
    st.success(f"Found **{len(providers)}** provider(s)")

    for p in providers:
        stars = "⭐" * int(p["average_rating"])
        with st.expander(f"{'🟢' if p['is_available'] else '🔴'} **{p['name']}** | {p['service_type'].title()} | {p['average_rating']}/5 {stars}"):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"📍 **Location:** {p['location']}")
                st.write(f"💼 **Experience:** {p['experience']} years")
                st.write(f"💰 **Rate:** Rs.{p['hourly_rate']}/hr*")
                st.write(f"📝 **About:** {p['description']}")
                st.caption("📞 *Phone number visible after booking is accepted.*")

            with c2:
                st.metric("Rating", f"{p['average_rating']}/5 ⭐")
                st.metric("Reviews", p["review_count"])

            st.markdown("---")
            st.markdown("### 📅 Book This Provider")
            with st.form(f"book_{p['id']}"):
                date_selected = st.date_input("Select Date", min_value=date.today(), key=f"d_{p['id']}")
                desc = st.text_area("Issue", placeholder="Describe your issue...", key=f"desc_{p['id']}")

                if st.form_submit_button("📅 Confirm Booking"):
                    if not desc:
                        st.error("❌ Describe your issue!")
                    else:
                        result = db.create_booking(
                            customer_id=user["id"],
                            provider_id=p["id"],
                            service_type=p["service_type"],
                            booking_date=str(date_selected),
                            description=desc
                        )
                        if result["success"]:
                            st.success(f"✅ Booking created! Wait for provider to accept.")
                            st.balloons()
                        else:
                            st.error(f"❌ {result['message']}")