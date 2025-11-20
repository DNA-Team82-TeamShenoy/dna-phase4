USE mini_world_db;

-- ==========================================
-- 1. Insert Strong Entities (Parents)
-- ==========================================

-- Table: Squad
INSERT INTO Squad (squad_id, squad_name, shift) VALUES
(1, '99th Precinct - Day Shift', 'Day'),
(2, '99th Precinct - Night Shift', 'Night'),
(3, 'Cyber Crimes Unit', 'Day');

-- Table: Detective
-- (Includes `rank` in backticks just to be safe matching the schema)
INSERT INTO Detective (badge_no, first_name, last_name, `rank`, squad_id) VALUES
(9901, 'Raymond', 'Holt', 'Captain', 1),
(9902, 'Terry', 'Jeffords', 'Sergeant', 1),
(9903, 'Jake', 'Peralta', 'Detective', 1),
(9904, 'Amy', 'Santiago', 'Sergeant', 1),
(9905, 'Rosa', 'Diaz', 'Detective', 1),
(9906, 'Charles', 'Boyle', 'Detective', 1),
(9907, 'Michael', 'Hitchcock', 'Detective', 1),
(9908, 'Norm', 'Scully', 'Detective', 1),
(9909, 'Keith', 'Pembroke', 'Captain', 2);

-- Table: Case_File
INSERT INTO Case_File (case_id, case_title, status) VALUES
(101, 'The Pontiac Bandit', 'Open'),
(102, 'The Oolong Slayer', 'Closed'),
(103, 'Halloween Heist I', 'Closed'),
(104, 'Jimmy Jab Games', 'Closed'),
(105, 'Operation Beans', 'Open');

-- Table: Precinct_Resource
INSERT INTO Precinct_Resource (asset_tag, item_name) VALUES
('RES-001', 'Kwazy Cupcakes Tablet'),
('RES-002', 'Antique Typewriter'),
('RES-003', 'Breakroom Vending Machine'),
('RES-004', 'Tactical Baton');

-- Table: Person_Of_Interest
INSERT INTO Person_Of_Interest (person_id, name, poi_type) VALUES
(501, 'Doug Judy', 'Perpetrator'),
(502, 'Madeline Wuntch', 'Perpetrator'), 
(503, 'Adrian Pimento', 'Confidential Informant'),
(504, 'Trudy Judy', 'Perpetrator'),
(505, 'Kevin Cozner', 'Witness');

-- Table: Halloween_Heist
INSERT INTO Halloween_Heist (heist_year, objective_item, winner_id) VALUES
(2013, 'The Medal of Valor', 9903), 
(2014, 'Holts Watch', 9901),        
(2015, 'The Crown', 9904),          
(2016, 'The Plaque', 9905);         

-- ==========================================
-- 2. Insert Subclass Entities
-- ==========================================

-- Table: Perpetrator
INSERT INTO Perpetrator (perp_id, person_id, primary_alias) VALUES
(1, 501, 'The Pontiac Bandit'),
(2, 502, 'The Grackle'),
(3, 504, 'Pontiac Bandit Copycat');

-- Table: Confidential_Informant
INSERT INTO Confidential_Informant (person_id) VALUES
(503);

-- ==========================================
-- 3. Insert Normalization Tables
-- ==========================================

-- Table: Detective_Specialization
INSERT INTO Detective_Specialization (badge_no, specialization) VALUES
(9903, 'Undercover'),
(9903, 'Improv'),
(9905, 'Weapons'),
(9905, 'Intimidation'),
(9906, 'Gastronomy'),
(9904, 'Organization'),
(9902, 'Strength');

-- Table: Perpetrator_Known_Associate
INSERT INTO Perpetrator_Known_Associate (perp_id, associate_name) VALUES
(1, 'Trudy Judy'),
(1, 'George Judy'),
(2, 'Chief CJ');

-- ==========================================
-- 4. Insert Weak Entities
-- ==========================================

-- Table: Evidence_Log
INSERT INTO Evidence_Log (case_id, evidence_tag, description, logged_by_id, storage_location) VALUES
(101, 'EV-101-A', 'Red Pontiac Firebird Key', 9903, 'Locker 4A'),
(102, 'EV-102-B', 'Oolong Tea Bag Wrapper', 9903, 'Archives'),
(103, 'EV-103-C', 'Safe Combination Note', 9904, 'Desk Drawer');

-- Table: Case_Update
INSERT INTO Case_Update (case_id, update_timestamp, entry_text, detective_id) VALUES
(101, '2023-10-30 09:00:00', 'Suspect spotted near the docks.', 9905),
(101, '2023-10-30 14:00:00', 'Suspect escaped on a jetski.', 9903),
(102, '2015-05-12 10:00:00', 'Pattern identified in tea killings.', 9903);

-- Table: Bet_Ledger
INSERT INTO Bet_Ledger (defendant_id, bet_timestamp, challenger_id, stake, outcome) VALUES
(9903, '2024-01-15 12:00:00', 9904, 'Who can drink the most water', 'Amy Won'),
(9907, '2024-02-20 13:00:00', 9908, 'Who falls asleep first', 'Scully Won'),
(9903, '2024-03-01 09:00:00', 9901, 'Heist Winner Prediction', 'Jake Lost');

-- ==========================================
-- 5. Insert Relationship Tables (M:N)
-- ==========================================

-- Table: Assigned_To
INSERT INTO Assigned_To (badge_no, case_id) VALUES
(9903, 101),
(9905, 101),
(9903, 102),
(9906, 105);

-- Table: Targets
INSERT INTO Targets (perp_id, case_id) VALUES
(1, 101),
(2, 105);

-- Table: Custodian_Of
INSERT INTO Custodian_Of (badge_no, asset_tag) VALUES
(9902, 'RES-001'),
(9903, 'RES-002'),
(9908, 'RES-003');

-- Table: Records_Interview
INSERT INTO Records_Interview (badge_no, perp_id, case_id) VALUES
(9903, 1, 101),
(9901, 2, 105);

-- Table: Documents_Heist_Participation
INSERT INTO Documents_Heist_Participation (badge_no, heist_year, role) VALUES
(9903, 2013, 'Winner'),
(9901, 2013, 'Loser'),
(9904, 2013, 'Distraction'),
(9905, 2014, 'Participant');

-- END
