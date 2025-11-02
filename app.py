import streamlit as st 
from auth.login import login_page
from auth.register import register_page
from Dashboard.dashboard import dashboard_page


st.set_page_config(page_title="FinAmp", page_icon=":bar_chart:", layout="wide")
        
if "user" not in st.session_state:
    menu = st.sidebar.selectbox("Menu",["Login", "Register"])
    if menu == "Register":
        register_page()
    else:
        login_page()
else:
    st.sidebar.success(f"Welcome aboard {st.session_state['user']}")
    st.title("FinAmp Dashboard")
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
        st.rerun()
        

if "user" in st.session_state:
    dashboard_page(st.session_state["user"])
else:
    # your login / register tabs here
    ...
