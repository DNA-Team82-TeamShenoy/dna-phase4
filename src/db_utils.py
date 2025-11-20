import datetime
from typing import Dict, Optional, Tuple

import pandas as pd
import pymysql


class DatabaseManager:
    """
    Handles raw SQL connections and execution using PyMySQL.
    Strictly avoids ORMs to meet Phase 4 requirements.
    """

    def __init__(self, config: Dict[str, str], verbose: bool = False):
        self.config = config
        self.connection = None
        self.log_file = "sql_commands.log"
        self.verbose = verbose

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

    def _log_query(self, cursor, query: str, params: Optional[Tuple]):
        """Logs the executed SQL command to a file and optionally prints to console."""
        try:
            # mogrify returns the exact string that was executed (params substituted)
            executed_sql = cursor.mogrify(query, params)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 1. Write to Log File
            with open(self.log_file, "a") as f:
                f.write(f"[{timestamp}] {executed_sql};\n")

            # 2. Print to Console if Verbose
            if self.verbose:
                print(f"\n[EXECUTING SQL]: {executed_sql}")

        except Exception as e:
            print(f"Logging failed: {e}")

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
        """Executes a SELECT query and returns results as a Pandas DataFrame."""
        if not self.connection or not self.connection.open:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                self._log_query(cursor, query, params)  # Log before or after execution
                cursor.execute(query, params)
                result = cursor.fetchall()
                return pd.DataFrame(result)
        except pymysql.Error as e:
            raise Exception(f"Query Error: {e}")

    def execute_update(self, query: str, params: Optional[Tuple] = None) -> str:
        """Executes INSERT, UPDATE, or DELETE queries."""
        if not self.connection or not self.connection.open:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                self._log_query(cursor, query, params)
                cursor.execute(query, params)
                return f"Success: {cursor.rowcount} row(s) affected."
        except pymysql.Error as e:
            raise Exception(f"Update Error: {e}")

    # ==========================================
    #  READ OPERATIONS (10 Required)
    # ==========================================

    def get_squad_roster(self, squad_name_filter: str) -> pd.DataFrame:
        """1. Join Detective and Squad to filter by squad name."""
        sql = """SELECT d.badge_no, d.first_name, d.last_name, d.rank, s.squad_name 
                 FROM Detective d JOIN Squad s ON d.squad_id = s.squad_id 
                 WHERE s.squad_name LIKE %s"""
        return self.execute_query(sql, (f"%{squad_name_filter}%",))

    def get_case_load(self) -> pd.DataFrame:
        """2. Aggregate count of cases per detective."""
        sql = """SELECT d.first_name, d.last_name, COUNT(a.case_id) as active_cases 
                 FROM Detective d LEFT JOIN Assigned_To a ON d.badge_no = a.badge_no 
                 GROUP BY d.badge_no, d.first_name, d.last_name ORDER BY active_cases DESC"""
        return self.execute_query(sql)

    def get_heist_winners(self) -> pd.DataFrame:
        """3. Join Halloween_Heist and Detective."""
        sql = """SELECT h.heist_year, h.objective_item, CONCAT(d.first_name, ' ', d.last_name) as winner 
                 FROM Halloween_Heist h LEFT JOIN Detective d ON h.winner_id = d.badge_no 
                 ORDER BY h.heist_year DESC"""
        return self.execute_query(sql)

    def search_evidence(self, keyword: str) -> pd.DataFrame:
        """4. Search Evidence Log by description."""
        sql = """SELECT e.evidence_tag, e.description, c.case_title FROM Evidence_Log e 
                 JOIN Case_File c ON e.case_id = c.case_id WHERE e.description LIKE %s"""
        return self.execute_query(sql, (f"%{keyword}%",))

    def get_perpetrator_network(self) -> pd.DataFrame:
        """5. List perpetrators and their known associates."""
        sql = """SELECT p.primary_alias, poi.name, a.associate_name FROM Perpetrator p 
                 JOIN Person_Of_Interest poi ON p.person_id = poi.person_id 
                 LEFT JOIN Perpetrator_Known_Associate a ON p.perp_id = a.perp_id"""
        return self.execute_query(sql)

    def get_unsolved_cases(self) -> pd.DataFrame:
        """6. Filter Cases that are not Closed."""
        sql = "SELECT * FROM Case_File WHERE status != 'Closed'"
        return self.execute_query(sql)

    def get_resource_custody(self) -> pd.DataFrame:
        """7. Show who has custody of which resource."""
        sql = """SELECT r.asset_tag, r.item_name, CONCAT(d.first_name, ' ', d.last_name) as holder 
                 FROM Precinct_Resource r LEFT JOIN Custodian_Of c ON r.asset_tag = c.asset_tag 
                 LEFT JOIN Detective d ON c.badge_no = d.badge_no"""
        return self.execute_query(sql)

    def get_betting_history(self) -> pd.DataFrame:
        """8. Show bets and outcomes."""
        sql = """SELECT b.bet_timestamp, b.stake, b.outcome, CONCAT(d1.first_name, ' ', d1.last_name) as challenger,
                 CONCAT(d2.first_name, ' ', d2.last_name) as defendant
                 FROM Bet_Ledger b JOIN Detective d1 ON b.challenger_id = d1.badge_no
                 JOIN Detective d2 ON b.defendant_id = d2.badge_no"""
        return self.execute_query(sql)

    def get_interview_logs(self) -> pd.DataFrame:
        """9. See who interviewed whom."""
        sql = """SELECT r.case_id, CONCAT(d.first_name, ' ', d.last_name) as detective, p.primary_alias as perp
                 FROM Records_Interview r JOIN Detective d ON r.badge_no = d.badge_no
                 JOIN Perpetrator p ON r.perp_id = p.perp_id"""
        return self.execute_query(sql)

    def get_detective_specializations(self) -> pd.DataFrame:
        """10. List specializations."""
        sql = """SELECT d.first_name, d.last_name, s.specialization 
                 FROM Detective d JOIN Detective_Specialization s ON d.badge_no = s.badge_no"""
        return self.execute_query(sql)

    # ==========================================
    #  WRITE OPERATIONS (10 Required)
    # ==========================================

    def insert_evidence(self, case_id: int, tag: str, desc: str, loc: str, badge: int):
        """1. INSERT Evidence."""
        sql = "INSERT INTO Evidence_Log (case_id, evidence_tag, description, logged_by_id, storage_location) VALUES (%s, %s, %s, %s, %s)"
        return self.execute_update(sql, (case_id, tag, desc, badge, loc))

    def update_case_status(self, case_id: int, new_status: str):
        """2. UPDATE Case Status."""
        sql = "UPDATE Case_File SET status = %s WHERE case_id = %s"
        return self.execute_update(sql, (new_status, case_id))

    def delete_resource(self, asset_tag: str):
        """3. DELETE Resource."""
        sql = "DELETE FROM Precinct_Resource WHERE asset_tag = %s"
        return self.execute_update(sql, (asset_tag,))

    def create_new_case(self, case_id: int, title: str):
        """4. INSERT New Case."""
        sql = "INSERT INTO Case_File (case_id, case_title, status) VALUES (%s, %s, 'Open')"
        return self.execute_update(sql, (case_id, title))

    def assign_detective(self, badge_no: int, case_id: int):
        """5. INSERT Assignment."""
        sql = "INSERT INTO Assigned_To (badge_no, case_id) VALUES (%s, %s)"
        return self.execute_update(sql, (badge_no, case_id))

    def add_person_of_interest(self, person_id: int, name: str, p_type: str):
        """6. INSERT Person Of Interest (Superclass)."""
        sql = "INSERT INTO Person_Of_Interest (person_id, name, poi_type) VALUES (%s, %s, %s)"
        return self.execute_update(sql, (person_id, name, p_type))

    def add_perpetrator_details(self, perp_id: int, person_id: int, alias: str):
        """7. INSERT Perpetrator (Subclass)."""
        sql = "INSERT INTO Perpetrator (perp_id, person_id, primary_alias) VALUES (%s, %s, %s)"
        return self.execute_update(sql, (perp_id, person_id, alias))

    def promote_detective(self, badge_no: int, new_rank: str):
        """8. UPDATE Detective Rank."""
        sql = "UPDATE Detective SET `rank` = %s WHERE badge_no = %s"
        return self.execute_update(sql, (new_rank, badge_no))

    def transfer_detective(self, badge_no: int, new_squad_id: int):
        """9. UPDATE Detective Squad."""
        sql = "UPDATE Detective SET squad_id = %s WHERE badge_no = %s"
        return self.execute_update(sql, (new_squad_id, badge_no))

    def delete_evidence(self, evidence_tag: str):
        """10. DELETE Evidence Log."""
        sql = "DELETE FROM Evidence_Log WHERE evidence_tag = %s"
        return self.execute_update(sql, (evidence_tag,))
