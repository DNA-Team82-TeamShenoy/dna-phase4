-- 1. Create and Select Database
DROP DATABASE IF EXISTS mini_world_db;
CREATE DATABASE mini_world_db;
USE mini_world_db;

-- 2. Create Strong Entity Tables

-- Table: Squad
CREATE TABLE Squad (
    squad_id INT PRIMARY KEY,
    squad_name VARCHAR(100) NOT NULL,
    shift VARCHAR(50)
);

-- Table: Detective
CREATE TABLE Detective (
    badge_no INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    `rank` VARCHAR(100), -- Backticks added to fix reserved keyword error
    squad_id INT,
    FOREIGN KEY (squad_id) REFERENCES Squad(squad_id) ON DELETE SET NULL
);

-- Table: Case_File
CREATE TABLE Case_File (
    case_id INT PRIMARY KEY,
    case_title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Open'
);

-- Table: Precinct_Resource
CREATE TABLE Precinct_Resource (
    asset_tag VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL
);

-- Table: Halloween_Heist
CREATE TABLE Halloween_Heist (
    heist_year INT PRIMARY KEY,
    objective_item VARCHAR(255),
    winner_id INT,
    FOREIGN KEY (winner_id) REFERENCES Detective(badge_no) ON DELETE SET NULL
);

-- Table: Person_Of_Interest (Superclass)
CREATE TABLE Person_Of_Interest (
    person_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    poi_type VARCHAR(50) -- e.g., 'Perpetrator', 'Victim', 'Witness'
);

-- 3. Create Subclass Tables

-- Table: Perpetrator
CREATE TABLE Perpetrator (
    perp_id INT PRIMARY KEY,
    person_id INT NOT NULL,
    primary_alias VARCHAR(255),
    FOREIGN KEY (person_id) REFERENCES Person_Of_Interest(person_id) ON DELETE CASCADE
);

-- Table: Confidential_Informant
CREATE TABLE Confidential_Informant (
    person_id INT PRIMARY KEY,
    FOREIGN KEY (person_id) REFERENCES Person_Of_Interest(person_id) ON DELETE CASCADE
);

-- 4. Create Normalization Tables (1NF Decompositions)

-- Table: Detective_Specialization
CREATE TABLE Detective_Specialization (
    badge_no INT,
    specialization VARCHAR(100),
    PRIMARY KEY (badge_no, specialization),
    FOREIGN KEY (badge_no) REFERENCES Detective(badge_no) ON DELETE CASCADE
);

-- Table: Perpetrator_Known_Associate
CREATE TABLE Perpetrator_Known_Associate (
    perp_id INT,
    associate_name VARCHAR(255),
    PRIMARY KEY (perp_id, associate_name),
    FOREIGN KEY (perp_id) REFERENCES Perpetrator(perp_id) ON DELETE CASCADE
);

-- 5. Create Weak Entity Tables

-- Table: Evidence_Log
CREATE TABLE Evidence_Log (
    case_id INT,
    evidence_tag VARCHAR(50),
    description TEXT,
    logged_by_id INT,
    storage_location VARCHAR(255),
    PRIMARY KEY (case_id, evidence_tag),
    FOREIGN KEY (case_id) REFERENCES Case_File(case_id) ON DELETE CASCADE,
    FOREIGN KEY (logged_by_id) REFERENCES Detective(badge_no) ON DELETE SET NULL
);

-- Table: Case_Update
CREATE TABLE Case_Update (
    case_id INT,
    update_timestamp DATETIME,
    entry_text TEXT,
    detective_id INT,
    PRIMARY KEY (case_id, update_timestamp),
    FOREIGN KEY (case_id) REFERENCES Case_File(case_id) ON DELETE CASCADE,
    FOREIGN KEY (detective_id) REFERENCES Detective(badge_no) ON DELETE SET NULL
);

-- Table: Bet_Ledger
CREATE TABLE Bet_Ledger (
    defendant_id INT,
    bet_timestamp DATETIME,
    challenger_id INT,
    stake VARCHAR(255),
    outcome VARCHAR(255),
    PRIMARY KEY (defendant_id, bet_timestamp),
    FOREIGN KEY (defendant_id) REFERENCES Detective(badge_no) ON DELETE CASCADE,
    FOREIGN KEY (challenger_id) REFERENCES Detective(badge_no) ON DELETE CASCADE
);

-- 6. Create Relationship Tables (M:N)

-- Table: Assigned_To
CREATE TABLE Assigned_To (
    badge_no INT,
    case_id INT,
    PRIMARY KEY (badge_no, case_id),
    FOREIGN KEY (badge_no) REFERENCES Detective(badge_no) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES Case_File(case_id) ON DELETE CASCADE
);

-- Table: Targets
CREATE TABLE Targets (
    perp_id INT,
    case_id INT,
    PRIMARY KEY (perp_id, case_id),
    FOREIGN KEY (perp_id) REFERENCES Perpetrator(perp_id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES Case_File(case_id) ON DELETE CASCADE
);

-- Table: Custodian_Of
CREATE TABLE Custodian_Of (
    badge_no INT,
    asset_tag VARCHAR(50),
    PRIMARY KEY (badge_no, asset_tag),
    FOREIGN KEY (badge_no) REFERENCES Detective(badge_no) ON DELETE CASCADE,
    FOREIGN KEY (asset_tag) REFERENCES Precinct_Resource(asset_tag) ON DELETE CASCADE
);

-- Table: Records_Interview
CREATE TABLE Records_Interview (
    badge_no INT,
    perp_id INT,
    case_id INT,
    PRIMARY KEY (badge_no, perp_id, case_id),
    FOREIGN KEY (badge_no) REFERENCES Detective(badge_no) ON DELETE CASCADE,
    FOREIGN KEY (perp_id) REFERENCES Perpetrator(perp_id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES Case_File(case_id) ON DELETE CASCADE
);

-- Table: Documents_Heist_Participation
CREATE TABLE Documents_Heist_Participation (
    badge_no INT,
    heist_year INT,
    role VARCHAR(100),
    PRIMARY KEY (badge_no, heist_year),
    FOREIGN KEY (badge_no) REFERENCES Detective(badge_no) ON DELETE CASCADE,
    FOREIGN KEY (heist_year) REFERENCES Halloween_Heist(heist_year) ON DELETE CASCADE
);
 -- END
