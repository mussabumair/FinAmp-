import streamlit as st
import json
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

DATA_PATH = Path("data/playlists.json")

def load_playlists():
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text())
    return {}

def save_playlists(playlists):
    DATA_PATH.write_text(json.dumps(playlists, indent=4))

def dashboard_page(user):
    st.title(f"Start Your FinAmp Journey")
    st.subheader(f"Welcome aboard, {st.session_state['name']}!")
    
    st.markdown("Your Wallet")
    playlists = load_playlists()
    wallet_data = playlists.get("wallets", {})
    wallet_balance = wallet_data.get(user, 0)
    deposit = st.number_input("Add Funds (PKR)", min_value = 0.0, step= 500.0)
    
    if st.button("Add to the wallet"):
        wallet_balance += deposit
        wallet_data[user] = wallet_balance
        playlists["wallets"] = wallet_data
        save_playlists(playlists)
        st.success(f"Added PKR {deposit: .2f} to your wallet.")
        
    st.write(f"Current Wallet Balance: PKR{wallet_balance: .2f}")
    st.divider()
    
    
        
    playlists = load_playlists()
    user_playlists = playlists.get(user, {})
    st.sidebar.header("Playlist Actions")
    option = st.sidebar.radio("Select Action:", ["Create Playlist", "View Playlists","Budget Summary"])


    if option == "Create Playlist":
        st.write("### Create a New Expense Playlist")
        playlist_name = st.text_input("Playlist Name (e.g., Gym, Food, Subscriptions)")

        if st.button("Create Playlist"):
            if playlist_name in user_playlists:
                st.warning("Playlist already exists!")
            else:
                user_playlists[playlist_name] = {"items": [], "budget": 0}
                playlists[user] = user_playlists
                save_playlists(playlists)
                st.success(f"Playlist '{playlist_name}' created!")


    elif option == "View Playlists":
        if not user_playlists:
            st.info("No playlists found. Create one to get started.")
            return

        selected = st.selectbox("Select a Playlist", list(user_playlists.keys()))
        playlist = user_playlists[selected]

        st.write(f"### 💼 {selected} Playlist")

        with st.expander("➕ Add Expense Item"):
            item_name = st.text_input("Expense Name")
            amount = st.number_input("Amount (PKR)", min_value=0.0, step=100.0)
            if st.button("Add Item"):
                playlist["items"].append({"name": item_name, "amount": amount})
                playlists[user] = user_playlists
                save_playlists(playlists)
                st.success("Item added!")

        if playlist["items"]:
            df = pd.DataFrame(playlist["items"])
            st.dataframe(df)
            total = sum(item["amount"] for item in playlist["items"])
            st.write(f"**Total Spent:** PKR {total:.2f}")
            
            playlist["budget"] = st.number_input("Set Monthly Budget (PKR)", min_value=0.0, value=float(playlist["budget"]))
            save_playlists(playlists)
            if playlist["budget"] > 0:
                st.progress(min(total / playlist["budget"], 1.0))
                st.write(f"Budget Used: {total/playlist['budget']*100:.1f}%")
                if total >= playlist["budget"]:
                    st.error("You have exceeded your budget!")
                elif total >= 0.8 * playlist["budget"]:
                    st.error("You are close to exceeding your budget!")

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{selected}_playlist.csv",
                mime="text/csv"
            )
            
            if st.button("📄 Export as PDF"):
                buffer = BytesIO()
                pdf = canvas.Canvas(buffer, pagesize=letter)
                pdf.setTitle(f"{selected} Playlist Report")

                pdf.drawString(100, 750, f"Playlist Report: {selected}")
                pdf.drawString(100, 730, f"User: {user}")
                pdf.drawString(100, 710, "----------------------------------")

                y = 690
                for item in playlist["items"]:
                    pdf.drawString(100, y, f"{item['name']}: PKR {item['amount']:.2f}")
                    y -= 20
                    if y < 100:
                        pdf.showPage()
                        y = 750
                total = sum(item["amount"] for item in playlist["items"])
                pdf.drawString(100, y - 20, f"Total Spent: PKR {total:.2f}")
                pdf.save()

                buffer.seek(0)
                st.download_button(
                    label="📄 Download PDF",
                    data=buffer,
                    file_name=f"{selected}_playlist.pdf",
                    mime="application/pdf"
                )        
                

        else:
            st.info("No items added yet.")
    elif option == "Budget Summary":
        if not user_playlists:
            st.info("No playlists found.")
            return 
        st.subheader("Overall Budget and Expenses Summarization")
        summary_data = []
        for pname, pdata in user_playlists.items():
            total = sum(item["amount"] for item in pdata["items"])
            summary_data.append({"Playlist": pname,
                                "Budget": pdata.get("budget", 0.0),
                                "Spent": total,
                                "Remaining": max(pdata.get("budget", 0) - total, 0)})
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary)
        
        total_budget = df_summary["Budget"].sum()
        total_spent = df_summary["Spent"].sum()
        st.write(f"### Total Spent: PKR{total_spent:.2f} / Budget: PKR{total_budget:.2f}")
        
        if total_budget > 0:
            overall_progress = total_spent / total_budget
            st.progress(min(overall_progress, 1.0))
            if overall_progress >= 1:
                st.error("You have exceeded your budget!")
            elif overall_progress >= 0.8:
                st.error("You are close to exceeding your budget!")
                
        if not df_summary.empty:
            st.subheader("Spending Distribution by Playlist")

            # Bar chart for total spent
            st.write("### Total Spending by Playlist")
            st.bar_chart(df_summary.set_index("Playlist")["Spent"])

            # Bar chart for remaining budget
            st.write("### Remaining Budget by Playlist")
            st.bar_chart(df_summary.set_index("Playlist")["Remaining"])

            # Combined comparison chart
            st.write("### Budget vs Spending Comparison")
            comparison_df = df_summary.set_index("Playlist")[["Budget", "Spent"]]
            st.bar_chart(comparison_df)

            
            if not df_summary.empty:
                # PDF export section
                if st.button("📄 Download Budget Summary (PDF)"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=letter)
                    width, height = letter

                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(200, height - 50, "FinAmp Budget Summary Report")

                    c.setFont("Helvetica", 12)
                    c.drawString(50, height - 80, f"User: {user}")
                    c.drawString(50, height - 100, f"Total Budget: PKR {total_budget:.2f}")
                    c.drawString(50, height - 120, f"Total Spent: PKR {total_spent:.2f}")
                    c.drawString(50, height - 140, f"Remaining: PKR {max(total_budget - total_spent, 0):.2f}")

                    y = height - 180
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(50, y, "Playlist")
                    c.drawString(200, y, "Budget")
                    c.drawString(300, y, "Spent")
                    c.drawString(400, y, "Remaining")
                    y -= 20

                    c.setFont("Helvetica", 11)
                    for _, row in df_summary.iterrows():
                        c.drawString(50, y, row["Playlist"])
                        c.drawString(200, y, f"{row['Budget']:.2f}")
                        c.drawString(300, y, f"{row['Spent']:.2f}")
                        c.drawString(400, y, f"{row['Remaining']:.2f}")
                        y -= 20
                        if y < 50:
                            c.showPage()
                            y = height - 50

                    c.save()
                    buffer.seek(0)
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=buffer,
                        file_name=f"{user}_budget_summary.pdf",
                        mime="application/pdf"
                    )

            
              

