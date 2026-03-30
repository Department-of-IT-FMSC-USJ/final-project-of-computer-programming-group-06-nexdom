import streamlit as st

st.title("📊 My Earnings & Performance")
st.markdown("---")

# CHECKS

if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "provider":
    st.warning("⚠️ Please login as a **Service Provider**.")
    st.stop()

db = st.session_state.db
user = st.session_state.user_data

# Get data from database
profile = db.get_provider_profile(user["id"])
all_bookings = db.get_provider_bookings(user["id"])
reviews = db.get_provider_reviews(user["id"])
earnings = db.get_provider_earnings(user["id"])
avg_rating = db.get_provider_average_rating(user["id"])

# Categorize bookings by status
completed = [b for b in all_bookings if b["status"] == "completed"]
accepted = [b for b in all_bookings if b["status"] == "accepted"]
pending = [b for b in all_bookings if b["status"] == "pending"]
rejected = [b for b in all_bookings if b["status"] == "rejected"]
cancelled = [b for b in all_bookings if b["status"] == "cancelled"]


# EARNINGS OVERVIEW

st.subheader("💰 Earnings Overview")

earn_col1, earn_col2, earn_col3, earn_col4 = st.columns(4)

earn_col1.metric(
    "💰 Total Earnings",
    f"Rs.{earnings:,.2f}"
)
earn_col2.metric(
    "✅ Jobs Completed",
    len(completed)
)
earn_col3.metric(
    "📋 Total Requests",
    len(all_bookings)
)

# Completion rate
if len(all_bookings) > 0:
    completion_rate = (len(completed) / len(all_bookings)) * 100
    earn_col4.metric(
        "📊 Completion Rate",
        f"{completion_rate:.0f}%"
    )
else:
    earn_col4.metric("📊 Completion Rate", "N/A")

st.markdown("---")


# RATE INFORMATION

if profile:
    st.subheader("💵 Rate Information")

    rate_col1, rate_col2, rate_col3, rate_col4 = st.columns(4)

    hourly = profile["hourly_rate"]

    rate_col1.metric(
        "⏰ Hourly Rate",
        f"Rs.{hourly:,.2f}"
    )
    rate_col2.metric(
        "📅 Daily (8hrs)",
        f"Rs.{hourly * 8:,.2f}"
    )
    rate_col3.metric(
        "📆 Weekly (5 days)",
        f"Rs.{hourly * 8 * 5:,.2f}"
    )
    rate_col4.metric(
        "🗓️ Monthly (22 days)",
        f"Rs.{hourly * 8 * 22:,.2f}"
    )

    st.markdown("---")

# BOOKING STATISTICS

st.subheader("📊 Booking Statistics")

book_col1, book_col2, book_col3, book_col4, book_col5 = st.columns(5)

book_col1.metric("📋 Total", len(all_bookings))
book_col2.metric("🟡 Pending", len(pending))
book_col3.metric("🟢 Active", len(accepted))
book_col4.metric("✅ Completed", len(completed))
book_col5.metric("❌ Rejected/Cancelled", len(rejected) + len(cancelled))

# Booking status breakdown visual
if all_bookings:
    st.markdown("**Booking Status Breakdown:**")

    statuses = {
        "Completed": len(completed),
        "Accepted": len(accepted),
        "Pending": len(pending),
        "Rejected": len(rejected),
        "Cancelled": len(cancelled)
    }

    status_colors = {
        "Completed": "#C8E6C9",
        "Accepted": "#B3E5FC",
        "Pending": "#FFF9C4",
        "Rejected": "#FFCDD2",
        "Cancelled": "#E0E0E0"
    }

    status_icons = {
        "Completed": "✅",
        "Accepted": "🟢",
        "Pending": "🟡",
        "Rejected": "🔴",
        "Cancelled": "⚫"
    }

    total = len(all_bookings)

    for status_name, count in statuses.items():
        if count > 0:
            percentage = (count / total) * 100
            color = status_colors[status_name]
            icon = status_icons[status_name]
            bar = "█" * int(percentage / 5)  # Scale bar

            st.markdown(
                f"{icon} **{status_name}:** {bar} "
                f"**{count}** ({percentage:.0f}%)"
            )

st.markdown("---")


# PERFORMANCE METRICS

st.subheader("🏆 Performance Metrics")

perf_col1, perf_col2, perf_col3 = st.columns(3)

with perf_col1:
    st.markdown(
        f"""
        <div style='text-align:center; padding:20px;
        background-color:#E3F2FD; border-radius:10px;
        border: 2px solid #1976D2;'>
        <h2>⭐</h2>
        <h3>{avg_rating}/5</h3>
        <p>Average Rating</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with perf_col2:
    # Acceptance rate
    total_decided = len(completed) + len(accepted) + len(rejected)
    if total_decided > 0:
        acceptance_rate = (
            (len(completed) + len(accepted)) / total_decided
        ) * 100
    else:
        acceptance_rate = 0

    if acceptance_rate >= 80:
        acc_color = "#E8F5E9"
        acc_border = "#4CAF50"
    elif acceptance_rate >= 50:
        acc_color = "#FFF9C4"
        acc_border = "#FFC107"
    else:
        acc_color = "#FFEBEE"
        acc_border = "#F44336"

    st.markdown(
        f"""
        <div style='text-align:center; padding:20px;
        background-color:{acc_color}; border-radius:10px;
        border: 2px solid {acc_border};'>
        <h2>📊</h2>
        <h3>{acceptance_rate:.0f}%</h3>
        <p>Acceptance Rate</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with perf_col3:
    st.markdown(
        f"""
        <div style='text-align:center; padding:20px;
        background-color:#F3E5F5; border-radius:10px;
        border: 2px solid #9C27B0;'>
        <h2>📝</h2>
        <h3>{len(reviews)}</h3>
        <p>Total Reviews</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# JOB HISTORY TABS

st.subheader("📋 Job History")

tab1, tab2, tab3, tab4 = st.tabs([
    "✅ Completed Jobs",
    "🟢 Active Jobs",
    "📊 Full Summary",
    "💰 Earnings Breakdown"
])

with tab1:
    if not completed:
        st.info("No completed jobs yet. Accept and complete bookings to earn!")
    else:
        st.success(f"🎉 You've completed **{len(completed)}** job(s)!")
        st.markdown("---")

        for i, booking in enumerate(completed, 1):
            with st.container():
                job_col1, job_col2 = st.columns([4, 1])

                with job_col1:
                    st.markdown(
                        f"**{i}. ✅ Booking #{booking['id']}**"
                    )
                    st.write(
                        f"👤 **Customer:** {booking['customer_name']}"
                    )
                    st.write(
                        f"📅 **Date:** {booking['booking_date']}"
                    )
                    st.write(
                        f"📝 **Issue:** {booking['description']}"
                    )
                    st.write(
                        f"📂 **Service:** {booking['service_type'].title()}"
                    )

                with job_col2:
                    if profile:
                        st.metric(
                            "💰 Earned",
                            f"Rs.{profile['hourly_rate']}"
                        )

                st.markdown("---")

with tab2:
    if not accepted:
        st.info("No active jobs at the moment.")
    else:
        st.warning(f"⚠️ You have **{len(accepted)}** active job(s)")
        st.markdown("---")

        for booking in accepted:
            st.markdown(f"### 🟢 Booking #{booking['id']}")
            st.write(f"👤 **Customer:** {booking['customer_name']}")
            st.write(f"📅 **Date:** {booking['booking_date']}")
            st.write(f"📝 **Issue:** {booking['description']}")

            if st.button(
                "✔️ Mark as Completed",
                key=f"earn_complete_{booking['id']}",
                use_container_width=True
            ):
                db.update_booking_status(booking["id"], "completed")
                st.success(
                    f"✅ Job completed! "
                    f"Earned Rs.{profile['hourly_rate'] if profile else 0}"
                )
                st.rerun()

            st.markdown("---")

with tab3:
    st.markdown("### 📊 Complete Performance Summary")
    st.markdown("---")

    summary_data = {
        "📋 Total Requests Received": len(all_bookings),
        "✅ Jobs Completed": len(completed),
        "🟢 Jobs In Progress": len(accepted),
        "🟡 Pending Requests": len(pending),
        "❌ Jobs Rejected": len(rejected),
        "⚫ Jobs Cancelled": len(cancelled),
        "💰 Total Earnings": f"Rs.{earnings:,.2f}",
        "⭐ Average Rating": f"{avg_rating}/5",
        "📝 Total Reviews": len(reviews),
    }

    if len(all_bookings) > 0:
        summary_data["📊 Completion Rate"] = (
            f"{(len(completed) / len(all_bookings)) * 100:.0f}%"
        )

    if profile:
        summary_data["⏰ Hourly Rate"] = f"Rs.{profile['hourly_rate']}"
        summary_data["💼 Experience"] = f"{profile['experience']} years"
        summary_data["📍 Location"] = profile["location"]

    for label, value in summary_data.items():
        sum_col1, sum_col2 = st.columns([2, 3])
        with sum_col1:
            st.write(f"**{label}:**")
        with sum_col2:
            st.write(f"{value}")

with tab4:
    st.markdown("### 💰 Earnings Breakdown")
    st.markdown("---")

    if not completed:
        st.info("No earnings yet. Complete jobs to start earning!")
    else:
        if profile:
            rate = profile["hourly_rate"]

            st.write(f"**Your hourly rate:** Rs.{rate}")
            st.write(f"**Jobs completed:** {len(completed)}")
            st.write(
                f"**Total earned:** Rs.{rate} × {len(completed)} = "
                f"**Rs.{earnings:,.2f}**"
            )

            st.markdown("---")
            st.markdown("**Earnings per job:**")

            for i, booking in enumerate(completed, 1):
                st.write(
                    f"💰 **Job #{booking['id']}** | "
                    f"{booking['customer_name']} | "
                    f"{booking['booking_date']} | "
                    f"Rs.{rate}"
                )

            st.markdown("---")

            # Projected earnings
            st.markdown("### 📈 Projected Earnings")

            proj_col1, proj_col2, proj_col3 = st.columns(3)

            # Average jobs per month (simple calculation)
            if len(completed) > 0:
                avg_monthly_jobs = max(len(completed), 1)
            else:
                avg_monthly_jobs = 0

            proj_col1.metric(
                "📅 Projected Monthly",
                f"Rs.{rate * avg_monthly_jobs * 4:,.0f}",
                help="Based on current job rate × 4 weeks"
            )
            proj_col2.metric(
                "📆 Projected Quarterly",
                f"Rs.{rate * avg_monthly_jobs * 4 * 3:,.0f}",
                help="Monthly projection × 3 months"
            )
            proj_col3.metric(
                "🗓️ Projected Yearly",
                f"Rs.{rate * avg_monthly_jobs * 4 * 12:,.0f}",
                help="Monthly projection × 12 months"
            )

st.markdown("---")

# TIPS FOR IMPROVEMENT

st.subheader("💡 Tips to Improve")

if avg_rating >= 4.5:
    st.success(
        "🌟 **Outstanding!** You're one of the top-rated providers! "
        "Keep up the excellent work!"
    )
elif avg_rating >= 4.0:
    st.info(
        "👍 **Great job!** Your ratings are good. "
        "Focus on punctuality and communication to reach 5 stars!"
    )
elif avg_rating >= 3.0:
    st.warning(
        "📈 **Room for improvement.** Read your reviews carefully "
        "and address any recurring concerns from customers."
    )
elif avg_rating > 0:
    st.error(
        "⚠️ **Needs attention.** Consider improving your service quality, "
        "punctuality, and professionalism. "
        "Respond to customer feedback!"
    )
else:
    st.info(
        "📝 No ratings yet. Complete jobs and encourage "
        "customers to leave reviews!"
    )

# Quick tips
tips = [
    "⏰ Always be punctual - arrive on time or early",
    "💬 Communicate clearly with customers about the work",
    "🧹 Leave the work area clean after completing the job",
    "💰 Be transparent about pricing - no hidden charges",
    "📱 Respond to booking requests quickly",
    "🔧 Use quality tools and materials",
    "😊 Be friendly and professional",
    "📸 Take before/after photos of your work"
]

with st.expander("📋 Tips for Getting Better Reviews"):
    for tip in tips:
        st.write(f"• {tip}")