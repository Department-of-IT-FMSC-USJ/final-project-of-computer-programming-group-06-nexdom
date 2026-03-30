```markdown
# 🏠 NEXDOM — Home Service Provider Platform

A full-stack web application built with Python and Streamlit that connects 
customers with trusted home service providers in Sri Lanka.

---

## 📋 Project Overview

NEXDOM is a multi-role service booking platform developed as a group 
assignment for ITC 2370. It allows customers to search and book home 
service providers, while providers can manage their bookings and track 
their performance. An AI-powered chatbot helps customers find the best 
providers using RAG (Retrieval-Augmented Generation) architecture.

---

## ✨ Features

### 👥 Customer
- Register and login securely
- Search service providers by type, location, and rating
- Book a provider with date and issue description
- View and manage bookings (cancel pending bookings)
- Submit star ratings and reviews for completed jobs
- Use AI ChatBot to get intelligent provider recommendations
- View and edit personal profile

### 🔧 Service Provider
- Submit registration request (requires admin approval)
- Manage booking requests (accept / reject / complete)
- View earnings and performance statistics
- View and analyse customer reviews with sentiment analysis
- Edit service profile and availability

### 🛡️ Admin
- Secure password-protected admin dashboard
- Approve or reject provider registration requests
- View platform-wide statistics
- View all providers, bookings, and reviews in data tables
- Visual analytics charts (providers by service, avg ratings)

### 🤖 AI ChatBot (RAG Architecture)
- Powered by Google Gemini AI
- Answers questions using REAL data from the database
- Quick service category buttons for instant recommendations
- Natural language queries about providers, pricing, and availability

---

## 🗂️ Project Structure

```
NEXDOM/
├── home.py                  # Main entry point + navigation controller
├── reset_db.py              # Database reset utility
├── chatbot/
│   ├── __init__.py
│   ├── rag_chatbot.py       # RAG chatbot with Gemini AI
│   ├── data_analyzer.py     # Database context retriever
│   └── sentiment_analyzer.py # Keyword-based sentiment analysis
├── database/
│   ├── __init__.py
│   ├── db_config.py         # SQLAlchemy engine + session config
│   ├── db_models.py         # ORM table definitions
│   └── db_operations.py     # All CRUD operations (DatabaseManager class)
├── models/
│   ├── __init__.py
│   ├── user.py              # Base User OOP class
│   ├── customer.py          # Customer inherits User
│   ├── service_provider.py  # ServiceProvider inherits User
│   ├── booking.py           # Booking OOP class
│   └── review.py            # Review OOP class
└── pages/
    ├── landing.py           # Home page content
    ├── login.py             # Login page
    ├── register.py          # Registration (customers direct, providers via request)
    ├── search_services.py   # Search + filter + book providers
    ├── mybookings.py        # Customer booking management + reviews
    ├── chatbot.py           # AI ChatBot interface
    ├── customer_profile.py  # Customer profile management
    ├── bookings_request.py  # Provider booking management
    ├── provider_profile.py  # Provider profile management
    ├── provider_reviews.py  # Provider review analytics
    ├── provider_earnings.py # Provider earnings dashboard
    └── admin.py             # Admin dashboard
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend + Backend | Python + Streamlit 1.55.0 |
| Database ORM | SQLAlchemy |
| Database | SQLite (`service_app.db`) |
| AI / Chatbot | Google Gemini API (RAG Architecture) |
| Data Analysis | Pandas |
| OOP Models | Python Classes with Inheritance |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9 or above
- pip

### Steps

**1. Clone or extract the project folder**

**2. Install required libraries**
```bash
pip install streamlit sqlalchemy google-genai
```

**3. Reset the database (first time only)**
```bash
python reset_db.py
```

**4. Run the application**
```bash
streamlit run home.py
```

**5. Open your browser at:**
```
http://localhost:8501
```

---

## 🔑 Test Accounts

| Role | Email | Password |
|---|---|---|
| Customer | ashan@email.com | pass123 |
| Customer | dilini@email.com | pass123 |
| Provider | kamal@email.com | pass123 |
| Provider | saman@email.com | pass123 |
| Admin | *(login page → Admin Login button)* | admin123 |

---

## 🗄️ Database Schema

| Table | Purpose |
|---|---|
| `users` | Stores both customers and providers |
| `provider_profiles` | Extended service details for providers |
| `bookings` | Service booking records |
| `reviews` | Customer ratings and review text |
| `provider_requests` | Pending provider registration requests |

---

## 🤖 AI ChatBot — How It Works

The ChatBot uses **RAG (Retrieval-Augmented Generation)** architecture:

1. Customer submits a query (e.g. *"Best plumber in Colombo"*)
2. `DataAnalyzer` fetches relevant provider data from the database
3. Real data is injected as context into the prompt
4. Google Gemini AI generates a response based ONLY on real data
5. Customer receives an accurate, data-grounded recommendation

---

## 📌 Notes

- Provider registrations require **admin approval** before login is possible
- The AI ChatBot is accessible to **customers only**
- Sample data is automatically seeded on first run
- Admin dashboard is accessible via the **Admin Login** button on the Login page (password: `admin123`)
```

***

