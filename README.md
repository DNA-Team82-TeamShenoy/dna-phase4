# 99th Precinct Database System (Phase 4)
This project implements a relational database system for the "99th Precinct" (Brooklyn Nine-Nine). It features a MySQL backend with two frontend interfaces: a modern web dashboard (Streamlit) and a terminal-based CLI.

## 1. MySQL Setup
You need a running MySQL server to use this application. Follow the instructions for your operating system.
### Installation
 * macOS (via Homebrew):
    ```bash
    brew install mysql
    brew services start mysql
    ```

 * Windows: Download the MySQL Installer and follow the setup wizard.

 * Linux (Ubuntu/Debian):
    ```bash
    sudo apt install mysql-server & sudo systemctl start mysql.
    ```
 
 * Linux (Arch):
    ```bash
    sudo pacman -S mysql & sudo systemctl start mysqld.
    ```

## Configuration (Creating the User)
Regardless of your OS, you must create the specific user account the application uses to connect.
 * Open your terminal and log in to MySQL as root:
    ```bash
    mysql -u root -p
    ```
    (Enter your root password if set, otherwise just press Enter).

 * Run the following SQL commands inside the MySQL shell:
   -- Create the user 'detective' with password 'Team82'
    ```bash
    CREATE USER IF NOT EXISTS \'detective\'@\'localhost\' IDENTIFIED BY \'Team82\';
    ```

 * Grant full privileges
    ```
    GRANT ALL PRIVILEGES ON \*.\* TO 'detective'@'localhost';
    ```

 * Apply changes
    ```
    FLUSH PRIVILEGES;
    ```

 * Exit
    ```
    EXIT;
    ```

## 2. Database Setup
Once the MySQL user is configured, you need to build the database structure and populate it with the initial data.

Run these commands from the root directory of the project:

### A. Create the Schema (Tables)
    mysql -u detective -p99 < src/schema.sql

### 2. Populate the Data (Insert Rows)
    mysql -u detective -p99 < src/populate.sql
    

Note: If you receive a "command not found" error for mysql, ensure MySQL is in your system PATH.

### 3. UV Setup (Dependencies)
This project uses uv for fast and reliable Python dependency management.
 * Install uv (if not already installed):
   ```bash
   pip install uv
   ```
   (Or use brew install uv on macOS).

 * Sync/Install Dependencies:
   You do not need to manually create a virtual environment. The uv run command (used in the next steps) will automatically verify and install all required packages (streamlit, pymysql, pandas) defined in pyproject.toml.

### 4. Running the Web App
To start the graphical User Interface (Dashboard):
    ```
    uv run streamlit run src/main_app.py
    ```

 * This will automatically open your default web browser to http://localhost:8501.
 * Troubleshooting: If the app cannot connect to the database, try changing the Host in the sidebar from localhost to 127.0.0.1.

### 5. Running the CLI
To start the text-based Command Line Interface:
    ```
    uv run python src/cli_app.py
    ```

 * Follow the on-screen prompts to navigate the menu.
 * Use q to quit the application.

## 🛠️ Troubleshooting / Reset
If you need to completely wipe the database and start fresh (e.g., if data gets corrupted):
 * Drop the Database:
    ```bash
    mysql -u detective -p99 -e "DROP DATABASE IF EXISTS mini_world_db;"
    ```
 * Re-run the Setup:
    ```bash
    mysql -u detective -p99 < src/schema.sql
    mysql -u detective -p99 < src/populate.sql
    ```