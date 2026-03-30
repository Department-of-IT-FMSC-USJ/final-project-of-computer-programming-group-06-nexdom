import streamlit as st
from chatbot.sentiment_analyzer import SentimentAnalyzer

st.title("⭐ My Reviews")
st.markdown("---")

# ==========================================
# CHECKS
# ==========================================
if "db" not in st.session_state:
    st.warning("⚠️ Please go to 🏠 Home page first.")
    st.stop()

if not st.session_state.get("logged_in") or st.session_state.user_role != "provider":
    st.warning("⚠️ Please login as a **Service Provider**.")
    st.stop()

db = st.session_state.db
user = st.session_state.user_data
analyzer = SentimentAnalyzer()

# Get reviews from database
reviews = db.get_provider_reviews(user["id"])
avg_rating = db.get_provider_average_rating(user["id"])
distribution = db.get_provider_rating_distribution(user["id"])

# ==========================================
# REVIEW STATISTICS
# ==========================================
st.subheader("📊 Review Statistics")
stat1, stat2, stat3, stat4 = st.columns(4)
stat1.metric("⭐ Average Rating", f"{avg_rating}/5")
stat2.metric("📝 Total Reviews", len(reviews))

if reviews:
    ratings = [r["rating"] for r in reviews]
    stat3.metric("🔝 Highest Rating", f"{max(ratings)}/5")
    stat4.metric("🔻 Lowest Rating", f"{min(ratings)}/5")
else:
    stat3.metric("🔝 Highest Rating", "N/A")
    stat4.metric("🔻 Lowest Rating", "N/A")

st.markdown("---")

# ==========================================
# RATING DISTRIBUTION
# ==========================================
if reviews:
    st.subheader("📊 Rating Distribution")
    total_reviews = len(reviews)

    for star_count in [5, 4, 3, 2, 1]:
        count = distribution.get(star_count, 0)
        percentage = (count / total_reviews) * 100 if total_reviews > 0 else 0
        star_display = "⭐" * star_count

        dist_col1, dist_col2, dist_col3 = st.columns([2, 4, 1])
        with dist_col1:
            st.write(f"{star_display}")
        with dist_col2:
            st.progress(percentage / 100)
        with dist_col3:
            st.write(f"**{count}** ({percentage:.0f}%)")

    st.markdown("---")

# ==========================================
# SENTIMENT ANALYSIS OVERVIEW
# ==========================================
st.subheader("🧠 Sentiment Analysis Overview")
st.markdown(
    "*Our system analyzes the text of each review to determine "
    "customer sentiment beyond just star ratings.*"
)

positive_count = 0
neutral_count = 0
negative_count = 0
total_sentiment_score = 0
sentiment_results = []

for review in reviews:
    sentiment = analyzer.analyze_sentiment(review["review_text"])
    sentiment_results.append({
        "review": review,
        "sentiment": sentiment
    })
    total_sentiment_score += sentiment["score"]
    if sentiment["label"] == "positive":
        positive_count += 1
    elif sentiment["label"] == "negative":
        negative_count += 1
    else:
        neutral_count += 1

avg_sentiment = total_sentiment_score / len(reviews) if reviews else 0

# Sentiment Stats
sent_col1, sent_col2, sent_col3, sent_col4 = st.columns(4)
sent_col1.metric("😊 Positive", positive_count)
sent_col2.metric("😐 Neutral", neutral_count)
sent_col3.metric("😟 Negative", negative_count)
sent_col4.metric("📈 Avg Sentiment", f"{avg_sentiment:.2f}")

# Sentiment Breakdown Bar
st.markdown("**Sentiment Breakdown:**")
if reviews:
    total_reviews = len(reviews)
    pos_pct = (positive_count / total_reviews) * 100
    neu_pct = (neutral_count / total_reviews) * 100
    neg_pct = (negative_count / total_reviews) * 100

    bar_col1, bar_col2, bar_col3 = st.columns(3)
    with bar_col1:
        st.markdown(f"😊 **Positive:** {positive_count} ({pos_pct:.0f}%)")
        st.progress(pos_pct / 100)
    with bar_col2:
        st.markdown(f"😐 **Neutral:** {neutral_count} ({neu_pct:.0f}%)")
        st.progress(neu_pct / 100)
    with bar_col3:
        st.markdown(f"😟 **Negative:** {negative_count} ({neg_pct:.0f}%)")
        st.progress(neg_pct / 100)

st.markdown("---")

# ==========================================
# INDIVIDUAL REVIEW CARDS
# ==========================================
st.subheader("📝 Individual Reviews")

if not reviews:
    st.info("📝 No reviews yet. Complete jobs to receive reviews!")
else:
    for item in sentiment_results:
        review = item["review"]
        sentiment = item["sentiment"]

        stars = "⭐" * review["rating"]
        label = sentiment["label"]
        score = sentiment["score"]

        # Sentiment colour badge
        if label == "positive":
            badge = "🟢 Positive"
        elif label == "negative":
            badge = "🔴 Negative"
        else:
            badge = "🟡 Neutral"

        with st.expander(
            f"{stars} | {review['customer_name']} | "
            f"{review['service_type'].title()} | {badge} | "
            f"{review['created_at']}"
        ):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**👤 Customer:** {review['customer_name']}")
                st.write(f"**📂 Service:** {review['service_type'].title()}")
                st.write(f"**⭐ Rating:** {review['rating']}/5 {stars}")
                st.write(f"**💬 Review:** \"{review['review_text']}\"")
                st.write(f"**📅 Date:** {review['created_at']}")

                # Keyword analysis
                key_phrases = analyzer.get_key_phrases(review["review_text"])
                if key_phrases and key_phrases != ["—"]:
                    st.markdown("**🔍 Keywords Detected:**")
                    st.write("  ".join(key_phrases))
                else:
                    st.markdown("**🔍 Keywords Detected:** —")

            with col2:
                st.metric("Rating", f"{review['rating']}/5")
                st.metric("Sentiment", badge)
                st.metric("Score", f"{score:.2f}")
