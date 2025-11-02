import re, json, bcrypt, streamlit as st 
from pathlib import Path

dbpath = Path("data/users.json")

def users_load():
    if dbpath.exists():
        return json.loads(dbpath.read_text())
    return{}

def users_save(users):
    dbpath.write_text(json.dumps(users, indent=4))


def register_page():
    st.title("Register for FinAmp")
    name = st.text_input("Full Name") 
    roll = st.text_input("FAST NUCES roll number (i.e: NUXXI-XXXX)")
    password = st.text_input("Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")
    kyc_q = st.selectbox("Select your KYC question", ["When was FinTech introduced in Fast NUCES?",
                                                    "What is the full form of FSM?",
                                                    "What is the flagship event of FAST ISB?",
                                                    "What is the name of the library?",
                                                    "What is the name of the bus service?"])
    kyc_a = st.text_input("Answer to your KYC question")
    
    if st.button("Register"):
        users = users_load()
        if not re.match(r"^NU\d{2}I-\d{4}$", roll):
            st.error("Wrong Format (i.e NU22I-0123)")
            return
        if len(password) < 8 or not re.search(r"[A-Z]", password) \
            or not re.search(r"[a-z]", password) \
            or not re.search(r"[0-9]", password) \
            or not re.search(r"[!@#$%&]", password):
                st.error("Password must have a digit, uppercase letter, lowercase letter, a symbol and atleast of 8 characters.")
                return
        if password != confirm_pass:
            st.error("Password does not match.")
            return
        if roll in users:
            st.error("User already exists.")
            return
        
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        hashed_kyc = bcrypt.hashpw(kyc_a.strip().lower().encode(), bcrypt.gensalt()).decode()
        users[roll] = {
            "name": name,
            "password": hashed_pw,
            "kyc_q": kyc_q,
            "kyc_a": hashed_kyc,
            "failed_attempts": 0,
            "locked": False}
        users_save(users)
        st.success("Registration completed! Go to the Login page.")