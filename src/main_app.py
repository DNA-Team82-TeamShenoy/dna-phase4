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

        # Connection Form
        with st.expander("Database Connection", expanded=True):
            db_host = st.text_input("Host", "localhost")
            db_user = st.text_input("User", "root")
            db_pass = st.text_input("Password", type="password")
            db_name = st.text_input("Database", "mini_world_db")

            connect_btn = st.button("Connect/Refresh")

        # Initialize Session State for DB
        if "db_manager" not in st.session_state or connect_btn:
            config = {
                "host": db_host,
                "user": db_user,
                "password": db_pass,
                "database": db_name,
            }
            st.session_state.db_manager = DatabaseManager(config)

        # Navigation
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
        st.info(
            "Please ensure your MySQL server is running and credentials are correct."
        )
        return

    # ==========================================
    # PAGE: Dashboard
    # ==========================================
    if nav_option == "Dashboard":
        st.markdown(
            '<div class="main-header">Welcome, Detective.</div>', unsafe_allow_html=True
        )
        st.write(
            "Use the sidebar to navigate the Brooklyn 99 Evidence Management System."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.info(
                "📋 **Queries Section**: View rosters, heist history, and search evidence."
            )
        with col2:
            st.warning(
                "✏️ **Updates Section**: Log evidence, close cases, or manage resources."
            )

        # Quick Stats (Example of a simple query on load)
        try:
            df_cases = db.execute_query(
                "SELECT status, COUNT(*) as count FROM Case_File GROUP BY status"
            )
            st.subheader("Current Case Status Overview")
            st.bar_chart(df_cases, x="status", y="count")
        except Exception as e:
            st.error(f"Could not load dashboard stats: {e}")

    # ==========================================
    # PAGE: Queries (Read)
    # ==========================================
    elif nav_option == "Queries (Read)":
        st.markdown(
            '<div class="main-header">📂 Database Queries</div>', unsafe_allow_html=True
        )

        query_type = st.selectbox(
            "Select Operation",
            [
                "1. The Squad Roster (Filter by Squad)",
                "2. Detective Case Load (Aggregation)",
                "3. Halloween Heist Hall of Fame (Joins)",
                "4. Search Evidence Log (Text Search)",
                "5. Perpetrator Network (Multi-Table Join)",
            ],
        )

        st.markdown("---")

        try:
            if "Squad Roster" in query_type:
                st.subheader("Search Detective Squads")
                squad_filter = st.text_input(
                    "Enter Squad Name (e.g., '99th', 'Cyber'):", ""
                )
                if st.button("Search Squad"):
                    results = db.get_squad_roster(squad_filter)
                    st.dataframe(results, use_container_width=True)

            elif "Case Load" in query_type:
                st.subheader("Detective Case Assignments")
                if st.button("Generate Report"):
                    results = db.get_case_load()
                    st.dataframe(results, use_container_width=True)

            elif "Halloween" in query_type:
                st.subheader("Heist Winners")
                if st.button("View Winners"):
                    results = db.get_heist_winners()
                    st.dataframe(results, use_container_width=True)

            elif "Evidence Log" in query_type:
                st.subheader("Evidence Text Search")
                keyword = st.text_input("Enter keyword (e.g., 'Key', 'Tea'):", "")
                if st.button("Search Evidence"):
                    results = db.search_evidence(keyword)
                    st.dataframe(results, use_container_width=True)

            elif "Perpetrator" in query_type:
                st.subheader("Criminal Associates Network")
                if st.button("Load Network"):
                    results = db.get_perpetrator_network()
                    st.dataframe(results, use_container_width=True)

        except Exception as e:
            st.error(f"Query Execution Error: {e}")

    # ==========================================
    # PAGE: Updates (Write)
    # ==========================================
    elif nav_option == "Updates (Write)":
        st.markdown(
            '<div class="main-header">✏️ Record Updates</div>', unsafe_allow_html=True
        )

        update_type = st.selectbox(
            "Select Action",
            [
                "1. Log New Evidence (INSERT)",
                "2. Update Case Status (UPDATE)",
                "3. Dispose Resource (DELETE)",
            ],
        )

        st.markdown("---")

        try:
            # --- INSERT OPERATION ---
            if "INSERT" in update_type:
                st.subheader("Log New Evidence Item")
                with st.form("insert_form"):
                    case_id = st.number_input("Case ID", min_value=1, step=1)
                    ev_tag = st.text_input("Evidence Tag (Unique)", "EV-XXX")
                    desc = st.text_area("Description")
                    loc = st.text_input("Storage Location", "Archives")
                    badge = st.number_input("Logged By (Badge No)", min_value=1, step=1)

                    submitted = st.form_submit_button("Log Evidence")

                    if submitted:
                        msg = db.insert_evidence(case_id, ev_tag, desc, loc, badge)
                        st.success(msg)
                        # Show new state
                        st.write("### Updated Log for Case:")
                        st.dataframe(
                            db.execute_query(
                                f"SELECT * FROM Evidence_Log WHERE case_id={case_id}"
                            )
                        )

            # --- UPDATE OPERATION ---
            elif "UPDATE" in update_type:
                st.subheader("Update Case File Status")

                # Helper to show current cases
                st.write("Current Active Cases:")
                st.dataframe(
                    db.execute_query(
                        "SELECT case_id, case_title, status FROM Case_File"
                    )
                )

                with st.form("update_form"):
                    case_id_upd = st.number_input(
                        "Case ID to Update", min_value=1, step=1
                    )
                    new_status = st.selectbox(
                        "New Status", ["Open", "Closed", "Cold", "Re-Opened"]
                    )

                    submitted = st.form_submit_button("Update Status")

                    if submitted:
                        msg = db.update_case_status(case_id_upd, new_status)
                        st.success(msg)
                        # Verify update
                        st.write("### Verification:")
                        st.dataframe(
                            db.execute_query(
                                f"SELECT * FROM Case_File WHERE case_id={case_id_upd}"
                            )
                        )

            # --- DELETE OPERATION ---
            elif "DELETE" in update_type:
                st.subheader("Dispose of Precinct Resource")

                st.write("Current Resources:")
                st.dataframe(db.execute_query("SELECT * FROM Precinct_Resource"))

                with st.form("delete_form"):
                    asset_tag = st.text_input("Asset Tag to Delete (e.g., RES-001)")

                    submitted = st.form_submit_button("Delete Asset")

                    if submitted:
                        msg = db.delete_resource(asset_tag)
                        st.success(msg)
                        st.write("### Remaining Resources:")
                        st.dataframe(
                            db.execute_query("SELECT * FROM Precinct_Resource")
                        )

        except Exception as e:
            st.error(f"Operation Failed: {e}")

    # ==========================================
    # PAGE: Table Inspector (Enhanced)
    # ==========================================
    elif nav_option == "Table Inspector":
        st.markdown(
            '<div class="main-header">🗄️ Table Inspector</div>', unsafe_allow_html=True
        )

        # 1. Get List of Tables
        try:
            tables = db.execute_query("SHOW TABLES")

            if tables.empty:
                st.warning("No tables found in the database.")
            else:
                # Extract table names to a list
                table_list = tables.iloc[:, 0].tolist()

                col1, col2 = st.columns([1, 3])
                with col1:
                    selected_table = st.selectbox("Select a Table", table_list)

                if selected_table:
                    # 2. Create Tabs for Schema vs Data
                    tab_structure, tab_data = st.tabs(
                        ["📋 Table Schema", "💾 View Data"]
                    )

                    with tab_structure:
                        st.subheader(f"Structure: {selected_table}")
                        desc = db.execute_query(f"DESCRIBE {selected_table}")
                        st.dataframe(desc, use_container_width=True)

                    with tab_data:
                        st.subheader(f"Contents: {selected_table}")
                        # Fetch all data from the selected table
                        # Note: In a production app with millions of rows, you'd want to add LIMIT
                        table_data = db.execute_query(f"SELECT * FROM {selected_table}")

                        st.caption(f"Row Count: {len(table_data)}")
                        st.dataframe(table_data, use_container_width=True)

        except Exception as e:
            st.error(f"Error inspecting tables: {e}")


if __name__ == "__main__":
    main()
