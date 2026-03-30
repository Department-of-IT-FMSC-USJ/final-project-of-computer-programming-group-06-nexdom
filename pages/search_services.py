import streamlit as st
from pages.style import inject_global_css, section_header, page_banner

inject_global_css()

page_banner(
    title="Search Service Providers",
    subtitle="Find the right professional for your home service needs.",
    icon="🔍",
)

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "customer":
    st.warning("⚠️ Login as **Customer** to search.")
    st.stop()

db   = st.session_state.db
user = st.session_state.user_data

# ---- Filter Bar ----
st.markdown(
    "<div style='background:white; border:1px solid #E2E8F0; border-radius:12px;"
    " padding:1rem 1.2rem; box-shadow:0 1px 4px rgba(0,0,0,0.05); margin-bottom:1rem;'>",
    unsafe_allow_html=True,
)
f1, f2, f3 = st.columns(3)
with f1:
    service_options = ["All", "plumbing", "carpentry", "electrical", "painting", "cleaning"]
    preselected  = st.session_state.pop("selected_service", None)
    default_index = service_options.index(preselected) if preselected in service_options else 0
    service_type = st.selectbox("🔧 Service", service_options, index=default_index)

with f2:
    sort_by = st.selectbox("📊 Sort By", ["Rating ↓", "Rating ↑", "Price ↓", "Price ↑", "Experience ↓"])

with f3:
    location = st.text_input("📍 Location", placeholder="e.g., Colombo")

st.markdown("</div>", unsafe_allow_html=True)

providers = db.get_all_providers(service_type if service_type != "All" else None)

if location:
    providers = [p for p in providers if location.lower() in p["location"].lower()]

# Sorting Logic
if sort_by == "Rating ↓":    providers.sort(key=lambda p: p["average_rating"], reverse=True)
elif sort_by == "Rating ↑":  providers.sort(key=lambda p: p["average_rating"])
elif sort_by == "Price ↓":   providers.sort(key=lambda p: p["hourly_rate"], reverse=True)
elif sort_by == "Price ↑":   providers.sort(key=lambda p: p["hourly_rate"])
elif sort_by == "Experience ↓": providers.sort(key=lambda p: p["experience"], reverse=True)

if not providers:
    st.markdown(
        "<div style='text-align:center; padding:3rem; color:#94A3B8;'>"
        "<div style='font-size:3rem;'>😔</div>"
        "<div style='font-size:1.1rem; margin-top:0.5rem;'>No providers found for your search.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<div style='background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px;"
        " padding:0.6rem 1rem; font-size:0.82rem; color:#1E40AF; margin-bottom:0.5rem;'>"
        "💡 <strong>Note:</strong> Rates are approximate. Final pricing may vary depending on "
        "scope, materials required, and complexity of the task.</div>",
        unsafe_allow_html=True,
    )
    st.success(f"Found **{len(providers)}** provider(s)")

    for p in providers:
        avail_badge = (
            "<span style='background:#DCFCE7;color:#15803D;padding:2px 10px;"
            "border-radius:20px;font-size:0.75rem;font-weight:600;'>🟢 Available</span>"
            if p["is_available"] else
            "<span style='background:#FEE2E2;color:#B91C1C;padding:2px 10px;"
            "border-radius:20px;font-size:0.75rem;font-weight:600;'>🔴 Unavailable</span>"
        )
        stars = "⭐" * int(p["average_rating"])

        with st.expander(
            f"{'🟢' if p['is_available'] else '🔴'} **{p['name']}** | "
            f"{p['service_type'].title()} | {p['average_rating']}/5 {stars}"
        ):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(
                    f"""
                    <div style='background:#F8FAFC; border-radius:10px; padding:1rem;
                                border:1px solid #E2E8F0; margin-bottom:0.5rem;'>
                      <div style='display:flex; gap:1.5rem; flex-wrap:wrap;'>
                        <div><span style='color:#64748B;font-size:0.78rem;'>📍 Location</span>
                          <div style='font-weight:600;'>{p['location']}</div></div>
                        <div><span style='color:#64748B;font-size:0.78rem;'>💼 Experience</span>
                          <div style='font-weight:600;'>{p['experience']} years</div></div>
                        <div><span style='color:#64748B;font-size:0.78rem;'>💰 Rate</span>
                          <div style='font-weight:600;'>Rs.{p['hourly_rate']}/hr*</div></div>
                        <div>{avail_badge}</div>
                      </div>
                      <div style='margin-top:0.8rem; color:#475569; font-size:0.88rem;'>
                        📝 {p['description']}
                      </div>
                    </div>
                    <p style='font-size:0.78rem; color:#94A3B8; margin:0;'>
                      📞 Phone number visible after booking is accepted.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

            with c2:
                st.markdown(
                    f"""
                    <div style='background:white; border:2px solid #E2E8F0; border-radius:12px;
                                padding:1rem; text-align:center; height:100%;'>
                      <div style='font-size:0.75rem; color:#64748B; font-weight:600;
                                  text-transform:uppercase;'>Rating</div>
                      <div style='font-size:1.6rem; font-weight:800; color:#F59E0B;'>
                        {p['average_rating']}
                      </div>
                      <div style='font-size:0.8rem; color:#F59E0B;'>{'⭐' * int(p['average_rating'])}</div>
                      <div style='margin-top:0.5rem; font-size:0.75rem; color:#64748B; font-weight:600;
                                  text-transform:uppercase;'>Reviews</div>
                      <div style='font-size:1.3rem; font-weight:700; color:#1E293B;'>
                        {p['review_count']}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("---")
            st.markdown(
                "<div style='font-size:0.95rem; font-weight:700; color:#0F172A; margin-bottom:0.5rem;'>"
                "📅 Book This Provider</div>",
                unsafe_allow_html=True,
            )
            from datetime import date
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