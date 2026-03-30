import streamlit as st
from pages.style import inject_global_css, section_header, page_banner

inject_global_css()

db = st.session_state.db

# HERO BANNER

page_banner(
    title="NEXDOM — Home Service Provider Platform",
    subtitle="Find trusted professionals for plumbing, carpentry, electrical, painting & cleaning.",
    icon="🏠",
)


# OUR SERVICES

section_header("🔧 Our Services", "Browse by category — click to explore providers")

st.markdown("""
    <style>
    .service-card {
        text-align: center;
        padding: 1.4rem 0.8rem;
        border-radius: 14px;
        margin-bottom: 6px;
        font-weight: 700;
        font-size: 0.9rem;
        color: #1E293B;
        border: 2px solid transparent;
        transition: all 0.15s ease;
    }
    .service-card:hover { transform: translateY(-2px); }
    .service-card .svc-icon { font-size: 2.4rem; margin-bottom: 6px; }
    .service-card .svc-name { font-size: 0.95rem; font-weight: 700; color: #0F172A; }
    </style>
""", unsafe_allow_html=True)

services_display = [
    ("🔧", "Plumbing",   "#DBEAFE", "#1D4ED8", "plumbing"),
    ("🪚", "Carpentry",  "#FEF3C7", "#D97706", "carpentry"),
    ("⚡", "Electrical", "#FEF9C3", "#CA8A04", "electrical"),
    ("🎨", "Painting",   "#F3E8FF", "#7C3AED", "painting"),
    ("🧹", "Cleaning",   "#DCFCE7", "#15803D", "cleaning"),
]

col1, col2, col3, col4, col5 = st.columns(5)

for col, (icon, name, bg, border, key) in zip(
    [col1, col2, col3, col4, col5], services_display
):
    with col:
        st.markdown(
            f"<div class='service-card' style='background:{bg}; border-color:{border}20;'>"
            f"<div class='svc-icon'>{icon}</div>"
            f"<div class='svc-name'>{name}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        if st.button(f"Explore", key=f"svc_{key}", use_container_width=True):
            if not st.session_state.get("logged_in"):
                st.warning("⚠️ Please login first to search services!")
                st.switch_page("pages/login.py")
            elif st.session_state.get("user_role") != "customer":
                st.warning("⚠️ Only customers can search services!")
            else:
                st.session_state.selected_service = key
                st.switch_page("pages/search_services.py")

st.markdown("<br>", unsafe_allow_html=True)

# PLATFORM STATS

section_header("📊 Platform Statistics", "Live numbers from our growing community")

stats = db.get_platform_stats()

s1, s2, s3, s4 = st.columns(4)
stat_configs = [
    (s1, "🔧 Providers",  stats.get("total_providers", 0), "#1A56DB"),
    (s2, "👥 Customers",  stats.get("total_customers", 0), "#7C3AED"),
    (s3, "⭐ Reviews",    stats.get("total_reviews", 0),   "#F59E0B"),
    (s4, "📋 Bookings",   stats.get("total_bookings", 0),  "#10B981"),
]
for col, label, value, color in stat_configs:
    with col:
        st.markdown(
            f"""
            <div style='background:white; border:1px solid #E2E8F0; border-radius:14px;
                        padding:1.2rem 1rem; text-align:center;
                        box-shadow:0 1px 4px rgba(0,0,0,0.06);
                        border-top: 4px solid {color};'>
              <div style='font-size:2rem; font-weight:800; color:{color};'>{value}</div>
              <div style='font-size:0.8rem; font-weight:600; color:#64748B;
                          text-transform:uppercase; letter-spacing:0.5px; margin-top:4px;'>
                {label}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# TOP PROVIDERS

section_header("🏆 Top Rated Providers", "Our highest-rated professionals this season")

all_providers = db.get_all_providers()
sorted_providers = sorted(
    all_providers, key=lambda p: p["average_rating"], reverse=True
)

top_cols = st.columns(3)
medals    = ["🥇", "🥈", "🥉"]
medal_bg  = ["#FFFBEB", "#F8FAFC", "#FFF7ED"]
medal_br  = ["#F59E0B", "#94A3B8", "#EA580C"]

for i, col in enumerate(top_cols):
    if i < len(sorted_providers):
        p = sorted_providers[i]
        stars = "⭐" * int(p["average_rating"])
        with col:
            st.markdown(
                f"""
                <div style='background:{medal_bg[i]}; border:2px solid {medal_br[i]};
                            border-radius:16px; padding:1.5rem; text-align:center;'>
                  <div style='font-size:2.5rem;'>{medals[i]}</div>
                  <div style='font-size:1rem; font-weight:700; color:#0F172A;
                              margin-top:6px;'>{p['name']}</div>
                  <div style='font-size:0.8rem; color:#64748B; margin-top:2px;
                              background:#F1F5F9; display:inline-block;
                              padding:2px 10px; border-radius:20px; margin-top:6px;'>
                    {p['service_type'].title()}
                  </div>
                  <div style='font-size:1.4rem; font-weight:800; color:{medal_br[i]};
                              margin-top:10px;'>{p['average_rating']} ⭐</div>
                  <div style='font-size:0.78rem; color:#64748B;'>{p['review_count']} reviews</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("<br>", unsafe_allow_html=True)
            
# CHATBOT CALLOUT

st.markdown(
    """
    <div style='background:linear-gradient(135deg,#1E1B4B,#312E81);
                border-radius:14px; padding:1.5rem 2rem;
                display:flex; align-items:center; gap:1rem;'>
      <div style='font-size:2.5rem;'>🤖</div>
      <div>
        <div style='font-size:1rem; font-weight:700; color:#E0E7FF;'>
          HomeHelper AI ChatBot
        </div>
        <div style='font-size:0.85rem; color:#A5B4FC; margin-top:2px;'>
          Our AI analyzes reviews using <strong style='color:#C7D2FE;'>sentiment analysis</strong>
          to recommend the best provider for your needs.
          Login as a customer to try it!
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)