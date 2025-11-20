import getpass
import sys

from db_utils import DatabaseManager


def print_menu():
    print("\n--- 99th Precinct Database CLI ---")
    print("1.  [READ]  View Squad Roster (Filter by Squad Name)")
    print("2.  [READ]  Generate Detective Case Load Report (Aggregation)")
    print("3.  [READ]  View Halloween Heist Hall of Fame (Joins)")
    print("4.  [READ]  Search Evidence Log by Keyword")
    print("5.  [READ]  View Perpetrator Network (Known Associates)")
    print("6.  [READ]  List All Unsolved/Open Cases")
    print("7.  [READ]  View Precinct Resource Custody Status")
    print("8.  [READ]  View Betting History (Challenger vs Defendant)")
    print("9.  [READ]  View Interview Records (Detective vs Perp)")
    print("10. [READ]  List Detective Specializations")
    print("-" * 60)
    print("11. [WRITE] Log New Evidence Item (INSERT)")
    print("12. [WRITE] Update Case File Status (UPDATE)")
    print("13. [WRITE] Dispose of Precinct Resource (DELETE)")
    print("14. [WRITE] Create New Case File (INSERT)")
    print("15. [WRITE] Assign Detective to Case (INSERT)")
    print("16. [WRITE] Add New Person of Interest (INSERT)")
    print("17. [WRITE] Add Perpetrator Details (INSERT)")
    print("18. [WRITE] Promote Detective Rank (UPDATE)")
    print("19. [WRITE] Transfer Detective to New Squad (UPDATE)")
    print("20. [WRITE] Delete Evidence Record (DELETE)")
    print("q.  Quit")


def main():
    print("Connect to Database:")
    user = input("User [default: detective]: ") or "detective"
    password = getpass.getpass("Password [default: ******]: ") or "Team82"
    host = input("Host [default: localhost]: ") or "localhost"
    dbname = input("Database [default: mini_world_db]: ") or "mini_world_db"

    config = {"user": user, "password": password, "host": host, "database": dbname}
    # Verbose=True ensures SQL queries are printed to CLI
    db = DatabaseManager(config, verbose=True)

    success, msg = db.connect()
    if not success:
        print(msg)
        sys.exit(1)
    print(msg)

    while True:
        print_menu()
        choice = input("\nSelection > ").strip().lower()

        try:
            if choice == "q":
                break

            # READ OPERATIONS
            elif choice == "1":
                f = input("Filter by Squad Name [e.g., '99', 'Cyber']: ")
                print(db.get_squad_roster(f).to_string())
            elif choice == "2":
                print(db.get_case_load().to_string())
            elif choice == "3":
                print(db.get_heist_winners().to_string())
            elif choice == "4":
                k = input("Search keyword [e.g., 'Key', 'Wrapper']: ")
                print(db.search_evidence(k).to_string())
            elif choice == "5":
                print(db.get_perpetrator_network().to_string())
            elif choice == "6":
                print(db.get_unsolved_cases().to_string())
            elif choice == "7":
                print(db.get_resource_custody().to_string())
            elif choice == "8":
                print(db.get_betting_history().to_string())
            elif choice == "9":
                print(db.get_interview_logs().to_string())
            elif choice == "10":
                print(db.get_detective_specializations().to_string())

            # WRITE OPERATIONS
            elif choice == "11":
                db.insert_evidence(
                    input("Case ID [INT]: "),
                    input("Tag [STRING, Unique, e.g. EV-999]: "),
                    input("Desc [TEXT]: "),
                    input("Loc [STRING]: "),
                    input("Badge [INT]: "),
                )
                print("Evidence Logged.")

            elif choice == "12":
                db.update_case_status(
                    input("Case ID [INT]: "),
                    input("New Status [STRING: 'Open', 'Closed']: "),
                )
                print("Status Updated.")

            elif choice == "13":
                db.delete_resource(input("Asset Tag [STRING, e.g. RES-001]: "))
                print("Resource Deleted.")

            elif choice == "14":
                db.create_new_case(
                    input("New Case ID [INT]: "), input("Title [STRING]: ")
                )
                print("Case Created.")

            elif choice == "15":
                db.assign_detective(input("Badge No [INT]: "), input("Case ID [INT]: "))
                print("Assigned.")

            elif choice == "16":
                db.add_person_of_interest(
                    input("Person ID [INT]: "),
                    input("Name [STRING]: "),
                    input("Type [STRING: 'Witness', 'Perpetrator', 'Victim']: "),
                )
                print("POI Added.")

            elif choice == "17":
                db.add_perpetrator_details(
                    input("Perp ID [INT]: "),
                    input("Person ID [INT, must match POI]: "),
                    input("Alias [STRING]: "),
                )
                print("Perp Added.")

            elif choice == "18":
                db.promote_detective(
                    input("Badge No [INT]: "), input("New Rank [STRING]: ")
                )
                print("Rank Updated.")

            elif choice == "19":
                db.transfer_detective(
                    input("Badge No [INT]: "), input("New Squad ID [INT]: ")
                )
                print("Transfer Complete.")

            elif choice == "20":
                db.delete_evidence(input("Evidence Tag [STRING]: "))
                print("Evidence Deleted.")

            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
