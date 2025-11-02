# 🪙 FinAmp — Personal Finance & Expense Tracker

FinAmp is a **Streamlit-based FinTech application** that helps users manage expenses, create categorized playlists, visualize budgets, and track wallet balances — all while maintaining a secure authentication system and strong cybersecurity design principles.

---

## 🚀 Features

### 🔐 Authentication

* User registration and login with **hashed passwords** (via `bcrypt`)
* **Session management** using `st.session_state`
* Automatic account lockout after repeated failed attempts

### 💼 Dashboard

* Create categorized **expense playlists** (e.g., Food, Gym, Subscriptions)
* Add, view, and edit expense items
* Export individual playlists as **CSV or PDF**
* Set and monitor monthly budgets
* Automatic **budget warnings** (alerts when nearing or exceeding limits)
* Wallet feature — deposit and track balance

### 📊 Visualization

* Interactive **bar charts** and **budget summaries**
* Real-time progress indicators for budget consumption

### 🧾 Data Handling

* Uses a secure, local **JSON-based database** (`data/playlists.json`)
* Safe read/write operations for user-specific data
* Future-ready structure to upgrade to SQL/Firebase easily

### 🧠 Cybersecurity

* Passwords stored as cryptographic hashes
* Brute-force attack protection
* Input sanitization for text fields
* Secure file management and structured data access
* Audit logging (optional)

---

## 🧰 Tech Stack

| Component      | Technology                                 |
| -------------- | ------------------------------------------ |
| Frontend       | Streamlit                                  |
| Database       | Local JSON storage (`data/playlists.json`) |
| Authentication | bcrypt                                     |
| Visualization  | Matplotlib & Streamlit Charts              |
| Language       | Python 3.10+                               |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/FinAmp.git
cd FinAmp
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
FinAmp/
│
├── app.py                     # Main application entry point
│
├── auth/
│   ├── login.py               # User login module
│   ├── register.py            # Registration module
│
├── Dashboard/
│   ├── dashboard.py           # Main dashboard logic & visualizations
│
├── data/
│   ├── users.json             # User credentials (hashed)
│   ├── playlists.json         # User expenses and wallet data
│
└── requirements.txt           # Python dependencies
```

---

## 🔒 Cybersecurity Testing Summary

| Test Type                    | Description                              | Status     |
| ---------------------------- | ---------------------------------------- | ---------- |
| **Authentication Hardening** | Password hashing using bcrypt            | ✅ Passed   |
| **Brute Force Protection**   | 5-attempt lockout mechanism              | ✅ Passed   |
| **Input Validation**         | Sanitization for text fields             | ✅ Passed   |
| **Session Security**         | Streamlit session state resets on logout | ✅ Passed   |
| **File Security**            | JSON file isolated and access-limited    | ✅ Passed   |
| **Encryption (optional)**    | Recommended via Fernet for deployment    | ⚠️ Pending |

---

## 📄 Future Enhancements
* 💳 Automatic expense import from bank statements (secure CSV/PDF parsing)
* 📈 Advanced analytics & predictive spending insights
* 🧠 AI-based budget recommendations

---

## 🧑‍💻 Contributors

* **Mussab Bin Umair** — Developer
* **FAST NUCES** — Cybersecurity in FinTech
