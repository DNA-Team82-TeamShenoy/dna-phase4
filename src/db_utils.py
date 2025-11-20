from typing import Dict, Optional, Tuple

import pandas as pd
import pymysql


class DatabaseManager:
    """
    Handles raw SQL connections and execution using PyMySQL.
    Strictly avoids ORMs to meet Phase 4 requirements.
    """

    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.connection = None

    def connect(self):
        """Establishes a connection to the MySQL database."""
        try:
            self.connection = pymysql.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            return True, "Connected successfully."
        except pymysql.Error as e:
            return False, f"Connection failed: {e}"

    def close(self):
        """Closes the connection if open."""
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
        """
        Executes a SELECT query and returns results as a Pandas DataFrame.
        Uses raw SQL with parameterized queries for security.
        """
        if not self.connection or not self.connection.open:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return pd.DataFrame(result)
        except pymysql.Error as e:
            raise Exception(f"Query Error: {e}")

    def execute_update(self, query: str, params: Optional[Tuple] = None) -> str:
        """
        Executes INSERT, UPDATE, or DELETE queries.
        Returns a success message or raises an exception.
        """
        if not self.connection or not self.connection.open:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                # Row count gives feedback on how many rows were affected
                return f"Success: {cursor.rowcount} row(s) affected."
        except pymysql.Error as e:
            raise Exception(f"Update Error: {e}")

    # ==========================================
    #  READ OPERATIONS (5 Required)
    # ==========================================

    def get_squad_roster(self, squad_name_filter: str) -> pd.DataFrame:
        """Query 1: Join Detective and Squad to filter by squad name."""
        sql = """
            SELECT d.badge_no, d.first_name, d.last_name, d.rank, s.squad_name, s.shift
            FROM Detective d
            JOIN Squad s ON d.squad_id = s.squad_id
            WHERE s.squad_name LIKE %s
        """
        # Add wildcards for partial matching
        return self.execute_query(sql, (f"%{squad_name_filter}%",))

    def get_case_load(self) -> pd.DataFrame:
        """Query 2: Aggregate count of cases per detective."""
        sql = """
            SELECT d.first_name, d.last_name, COUNT(a.case_id) as active_cases
            FROM Detective d
            LEFT JOIN Assigned_To a ON d.badge_no = a.badge_no
            GROUP BY d.badge_no, d.first_name, d.last_name
            ORDER BY active_cases DESC
        """
        return self.execute_query(sql)

    def get_heist_winners(self) -> pd.DataFrame:
        """Query 3: Join Halloween_Heist and Detective."""
        sql = """
            SELECT h.heist_year, h.objective_item, CONCAT(d.first_name, ' ', d.last_name) as winner
            FROM Halloween_Heist h
            LEFT JOIN Detective d ON h.winner_id = d.badge_no
            ORDER BY h.heist_year DESC
        """
        return self.execute_query(sql)

    def search_evidence(self, keyword: str) -> pd.DataFrame:
        """Query 4: Search Evidence Log by description."""
        sql = """
            SELECT e.evidence_tag, e.description, e.storage_location, c.case_title
            FROM Evidence_Log e
            JOIN Case_File c ON e.case_id = c.case_id
            WHERE e.description LIKE %s
        """
        return self.execute_query(sql, (f"%{keyword}%",))

    def get_perpetrator_network(self) -> pd.DataFrame:
        """Query 5: List perpetrators and their known associates."""
        sql = """
            SELECT p.primary_alias, poi.name as real_name, a.associate_name
            FROM Perpetrator p
            JOIN Person_Of_Interest poi ON p.person_id = poi.person_id
            LEFT JOIN Perpetrator_Known_Associate a ON p.perp_id = a.perp_id
        """
        return self.execute_query(sql)

    # ==========================================
    #  WRITE OPERATIONS (3 Required)
    # ==========================================

    def insert_evidence(self, case_id: int, tag: str, desc: str, loc: str, badge: int):
        """Update 1 (INSERT): Add to Evidence_Log."""
        sql = """
            INSERT INTO Evidence_Log (case_id, evidence_tag, description, logged_by_id, storage_location)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_update(sql, (case_id, tag, desc, badge, loc))

    def update_case_status(self, case_id: int, new_status: str):
        """Update 2 (UPDATE): Update Case_File status."""
        sql = """
            UPDATE Case_File
            SET status = %s
            WHERE case_id = %s
        """
        return self.execute_update(sql, (new_status, case_id))

    def delete_resource(self, asset_tag: str):
        """Update 3 (DELETE): Remove from Precinct_Resource."""
        sql = """
            DELETE FROM Precinct_Resource
            WHERE asset_tag = %s
        """
        return self.execute_update(sql, (asset_tag,))
