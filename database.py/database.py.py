import sqlite3

def init_db():
    conn = sqlite3.connect("medquery_ops.db")
    cursor = conn.cursor()

    # Create Equipment Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            equipment_id TEXT PRIMARY KEY,
            modality TEXT,
            location TEXT,
            status TEXT
        )
    """)

    # Create Downtime Log Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS downtime_log (
            downtime_id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT,
            outage_hours REAL,
            fault_type TEXT,
            date TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
        )
    """)

    # Create Study Log Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_log (
            study_id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT,
            modality TEXT,
            shift TEXT,
            turnaround_time_mins REAL,
            status TEXT,
            date TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
        )
    """)

    # Insert Sample Data
    cursor.executemany("INSERT OR IGNORE INTO equipment VALUES (?, ?, ?, ?)", [
        ("MR-01", "MRI", "Main Wing", "Degraded"),
        ("MR-02", "MRI", "Emergency", "Active"),
        ("CT-01", "CT", "Main Wing", "Active"),
        ("US-01", "Ultrasound", "ICU", "Active"),
        ("US-02", "Ultrasound", "Outpatient", "Active")
    ])

    cursor.executemany("INSERT INTO downtime_log (equipment_id, outage_hours, fault_type, date) VALUES (?, ?, ?, ?)", [
        ("MR-01", 103.2, "Hardware (Cooling/Magnet)", "2026-10-01"),
        ("MR-02", 45.0, "Software Error", "2026-10-03"),
        ("CT-01", 12.5, "Calibration", "2026-10-04"),
        ("US-01", 140.3, "Hardware (Transducer)", "2026-10-05")
    ])

    cursor.executemany("INSERT INTO study_log (equipment_id, modality, shift, turnaround_time_mins, status, date) VALUES (?, ?, ?, ?, ?, ?)", [
        ("MR-01", "MRI", "Day", 116.2, "Clean", "2026-10-01"),
        ("MR-01", "MRI", "Night", 150.0, "Clean", "2026-10-01"),
        ("CT-01", "CT", "Day", 52.0, "Clean", "2026-10-02"),
        ("CT-01", "CT", "Night", 100.9, "Clean", "2026-10-02"),
        ("US-02", "Ultrasound", "Day", 25.7, "Clean", "2026-10-03")
    ])

    conn.commit()
    conn.close()
    print("Database 'medquery_ops.db' initialized successfully!")

if __name__ == "__main__":
    init_db()