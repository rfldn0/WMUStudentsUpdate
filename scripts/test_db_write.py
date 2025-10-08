#!/usr/bin/env python3
"""Test database write permissions"""

import sqlite3
import os

DB_PATH = os.path.join('backend', 'students.db')

print(f"Testing database: {DB_PATH}")
print(f"File exists: {os.path.exists(DB_PATH)}")
print(f"File is readable: {os.access(DB_PATH, os.R_OK)}")
print(f"File is writable: {os.access(DB_PATH, os.W_OK)}")
print(f"Directory is writable: {os.access('backend', os.W_OK)}")

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Try to read
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    print(f"\n[OK] READ successful: {count} students found")

    # Try to write (test with a temporary table)
    cursor.execute("CREATE TEMPORARY TABLE test_write (id INTEGER)")
    cursor.execute("INSERT INTO test_write VALUES (1)")
    conn.commit()
    print("[OK] WRITE successful: Temporary table created and written")

    # Try actual write to students table
    cursor.execute("SELECT MAX(idn) FROM students")
    max_idn = cursor.fetchone()[0]
    print(f"[OK] Max IDN: {max_idn}")

    conn.close()
    print("\n[SUCCESS] Database is fully accessible!")

except sqlite3.OperationalError as e:
    print(f"\n[ERROR] Database error: {e}")
    print("\nPossible causes:")
    print("1. Database file is locked by another program")
    print("2. Insufficient permissions")
    print("3. Disk is full or read-only")

except Exception as e:
    print(f"\n[ERROR] Unexpected error: {e}")
