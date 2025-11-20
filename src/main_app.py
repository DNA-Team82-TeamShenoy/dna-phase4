import os

import streamlit as st

from db_utils import DatabaseManager

# Page Configuration
st.set_page_config(
    page_title="99th Precinct Database",
    page_icon="👮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styling
st.markdown(
    """
    <style>
    .main-header {font-size: 2.5rem; font-weight: 700; color: #1f4e79;}
    .sub-header {font-size: 1.5rem; font-weight: 600; color: #333;}
    .success-msg {color: green; font-weight: bold;}
    .error-msg {color: red; font-weight: bold;}
    </style>
""",
    unsafe_allow_html=True,
)


def main():
    # ==========================================
    # Sidebar: Connection & Navigation
    # ==========================================
    with st.sidebar:
        st.title("👮 99th Precinct DB")
        st.markdown("---")

        with st.expander("Database Connection", expanded=True):
            db_host = st.text_input("Host", "localhost")
            db_user = st.text_input("User", "detective")
            db_pass = st.text_input("Password", "Team82", type="password")
            db_name = st.text_input("Database", "mini_world_db")
            connect_btn = st.button("Connect/Refresh")

        if "db_manager" not in st.session_state or connect_btn:
            config = {
                "host": db_host,
                "user": db_user,
                "password": db_pass,
                "database": db_name,
            }
            st.session_state.db_manager = DatabaseManager(config)

        st.markdown("---")
        nav_option = st.radio(
            "Navigation",
            ["Dashboard", "Queries (Read)", "Updates (Write)", "Table Inspector"],
        )

    # ==========================================
    # Main Connection Check
    # ==========================================
    db = st.session_state.db_manager
    success, msg = db.connect()

    if not success:
        st.error(f"Database Connection Failed: {msg}")
        return

    # ==========================================
    # PAGE: Dashboard
    # ==========================================
    if nav_option == "Dashboard":
        st.markdown(
            '<div class="main-header">Welcome, Detective.</div>', unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            st.info("📋 **Queries**: 10 Operations available.")
        with col2:
            st.warning("✏️ **Updates**: 10 Operations available.")

        st.subheader("Recent Activity Log")
        st.caption("Showing executed SQL queries (Chronological Order)")

        if os.path.exists("sql_commands.log"):
            try:
                with open("sql_commands.log", "r") as f:
                    lines = f.readlines()

                if lines:
                    # Display lines in original chronological order
                    log_content = "".join(lines)
                    st.code(log_content, language="sql")
                else:
                    st.info("Log file is empty.")
            except Exception as e:
                st.error(f"Error reading log file: {e}")
        else:
            st.info("No logs found yet.")

    # ==========================================
    # PAGE: Queries (Read)
    # ==========================================
    elif nav_option == "Queries (Read)":
        st.markdown(
            '<div class="main-header">📂 Database Queries</div>', unsafe_allow_html=True
        )

        options = [
            "1. View Squad Roster (Filter by Squad Name)",
            "2. Generate Detective Case Load Report (Aggregation)",
            "3. View Halloween Heist Hall of Fame (Joins)",
            "4. Search Evidence Log by Keyword",
            "5. View Perpetrator Network (Known Associates)",
            "6. List All Unsolved/Open Cases",
            "7. View Precinct Resource Custody Status",
            "8. View Betting History (Challenger vs Defendant)",
            "9. View Interview Records (Detective vs Perp)",
            "10. List Detective Specializations",
        ]
        query_type = st.selectbox("Select Query", options)
        st.markdown("---")

        try:
            if "1." in query_type:
                f = st.text_input("Squad Name Filter:", "")
                if st.button("Run"):
                    st.dataframe(db.get_squad_roster(f))
            elif "2." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_case_load())
            elif "3." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_heist_winners())
            elif "4." in query_type:
                k = st.text_input("Keyword:", "")
                if st.button("Run"):
                    st.dataframe(db.search_evidence(k))
            elif "5." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_perpetrator_network())
            elif "6." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_unsolved_cases())
            elif "7." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_resource_custody())
            elif "8." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_betting_history())
            elif "9." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_interview_logs())
            elif "10." in query_type:
                if st.button("Run"):
                    st.dataframe(db.get_detective_specializations())

        except Exception as e:
            st.error(f"Error: {e}")

    # ==========================================
    # PAGE: Updates (Write)
    # ==========================================
    elif nav_option == "Updates (Write)":
        st.markdown(
            '<div class="main-header">✏️ Record Updates</div>', unsafe_allow_html=True
        )

        options = [
            "1. Log New Evidence Item (INSERT)",
            "2. Update Case File Status (UPDATE)",
            "3. Dispose of Precinct Resource (DELETE)",
            "4. Create New Case File (INSERT)",
            "5. Assign Detective to Case (INSERT)",
            "6. Add New Person of Interest (INSERT)",
            "7. Add Perpetrator Details (INSERT)",
            "8. Promote Detective Rank (UPDATE)",
            "9. Transfer Detective to New Squad (UPDATE)",
            "10. Delete Evidence Record (DELETE)",
        ]
        update_type = st.selectbox("Select Update", options)
        st.markdown("---")

        try:
            with st.form("update_form"):
                if "1." in update_type:
                    cid = st.number_input("Case ID", 100)
                    tag = st.text_input("Tag")
                    desc = st.text_input("Description")
                    loc = st.text_input("Location")
                    badge = st.number_input("Badge No", 9900)
                    if st.form_submit_button("Execute"):
                        st.success(db.insert_evidence(cid, tag, desc, loc, badge))

                elif "2." in update_type:
                    cid = st.number_input("Case ID", 100)
                    stat = st.selectbox("Status", ["Open", "Closed", "Cold"])
                    if st.form_submit_button("Execute"):
                        st.success(db.update_case_status(cid, stat))

                elif "3." in update_type:
                    tag = st.text_input("Asset Tag")
                    if st.form_submit_button("Execute"):
                        st.success(db.delete_resource(tag))

                elif "4." in update_type:
                    cid = st.number_input("New Case ID", 200)
                    title = st.text_input("Title")
                    if st.form_submit_button("Execute"):
                        st.success(db.create_new_case(cid, title))

                elif "5." in update_type:
                    badge = st.number_input("Badge No", 9900)
                    cid = st.number_input("Case ID", 100)
                    if st.form_submit_button("Execute"):
                        st.success(db.assign_detective(badge, cid))

                elif "6." in update_type:
                    pid = st.number_input("Person ID", 600)
                    name = st.text_input("Name")
                    ptype = st.selectbox("Type", ["Witness", "Perpetrator", "Victim"])
                    if st.form_submit_button("Execute"):
                        st.success(db.add_person_of_interest(pid, name, ptype))

                elif "7." in update_type:
                    perpid = st.number_input("Perp ID", 10)
                    pid = st.number_input("Person ID", 600)
                    alias = st.text_input("Alias")
                    if st.form_submit_button("Execute"):
                        st.success(db.add_perpetrator_details(perpid, pid, alias))

                elif "8." in update_type:
                    badge = st.number_input("Badge No", 9900)
                    rank = st.text_input("New Rank")
                    if st.form_submit_button("Execute"):
                        st.success(db.promote_detective(badge, rank))

                elif "9." in update_type:
                    badge = st.number_input("Badge No", 9900)
                    sq = st.number_input("New Squad ID", 1)
                    if st.form_submit_button("Execute"):
                        st.success(db.transfer_detective(badge, sq))

                elif "10." in update_type:
                    tag = st.text_input("Evidence Tag")
                    if st.form_submit_button("Execute"):
                        st.success(db.delete_evidence(tag))

        except Exception as e:
            st.error(f"Operation Failed: {e}")

    # ==========================================
    # PAGE: Table Inspector
    # ==========================================
    elif nav_option == "Table Inspector":
        st.markdown(
            '<div class="main-header">🗄️ Table Inspector</div>', unsafe_allow_html=True
        )
        tables = db.execute_query("SHOW TABLES")
        if not tables.empty:
            t = st.selectbox("Table", tables.iloc[:, 0].tolist())
            st.dataframe(
                db.execute_query(f"SELECT * FROM {t}"), use_container_width=True
            )


if __name__ == "__main__":
    main()
