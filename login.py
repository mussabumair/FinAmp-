import json, bcrypt, streamlit as st
from pathlib import Path
st.write("Using rerun function:", hasattr(st, "rerun"))

dbpath = Path("data/users.json")

def users_load():
    if dbpath.exists():
        return json.loads(dbpath.read_text())
    return{}

def users_save(users):
    dbpath.write_text(json.dumps(users, indent=4))
    
def login_page():
    st.title("Login - FinAmp")
    roll = st.text_input("Roll Number")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        users = users_load()
        if roll not in users:
            st.error("User was not found")
            return
        
        user = users[roll]
        if user.get("locked"):
            st.error("User is locked due to repeated attempts.")
            return
        
        if bcrypt.checkpw(password.encode(), user["password"].encode()):
            st.session_state["user"] = roll
            st.session_state["name"] = user["name"]
            user["failed_attempts"] = 0 
            users_save(users)   
            st.success("Login successful")
            st.rerun()
        else:
            user["failed_attempts"] += 1
            if user["failed_attempts"] >= 5:
                user["locked"] = True
                st.error("Account in cooling period after 5 failed attempts")
            else:
                st.error(f"Incorrect password. Attempts: {5 - user['failed_attempts']}")
                
            users_save(users)