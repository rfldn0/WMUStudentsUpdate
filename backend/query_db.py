#!/usr/bin/env python3
"""
Quick script to query and modify SQLite database
Usage: python backend/query_db.py
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'students.db')

def connect():
    """Create database connection"""
    return sqlite3.connect(DB_PATH)

def view_all_students():
    """View all students"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY nama")

    print("\n" + "="*80)
    print("ALL STUDENTS")
    print("="*80)

    for row in cursor.fetchall():
        print(f"IDN: {row[1]} | Name: {row[2]} | Major: {row[3]} | University: {row[4]} | Year: {row[5]} | Province: {row[6]}")

    conn.close()

def search_student(name):
    """Search student by name"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE LOWER(nama) LIKE LOWER(?)", (f'%{name}%',))

    print(f"\n=== SEARCH RESULTS FOR: {name} ===")
    results = cursor.fetchall()

    if results:
        for row in results:
            print(f"IDN: {row[1]} | Name: {row[2]} | Major: {row[3]} | University: {row[4]}")
    else:
        print("No students found")

    conn.close()

def count_students():
    """Count total students"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    print(f"\nTotal Students: {count}")
    conn.close()

def add_student(nama, jurusan, university, year, provinsi):
    """Add new student"""
    conn = connect()
    cursor = conn.cursor()

    # Get next IDN
    cursor.execute("SELECT MAX(idn) FROM students")
    max_idn = cursor.fetchone()[0]
    new_idn = (max_idn or 0) + 1

    try:
        cursor.execute("""
            INSERT INTO students (idn, nama, jurusan, university, year, provinsi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (new_idn, nama, jurusan, university, year, provinsi))

        conn.commit()
        print(f"\n✅ Added student: {nama} (IDN: {new_idn})")
    except sqlite3.IntegrityError as e:
        print(f"\n❌ Error: {e}")

    conn.close()

def update_student(nama, field, new_value):
    """Update student field"""
    conn = connect()
    cursor = conn.cursor()

    valid_fields = ['jurusan', 'university', 'year', 'provinsi']
    if field not in valid_fields:
        print(f"❌ Invalid field. Use: {', '.join(valid_fields)}")
        return

    cursor.execute(f"""
        UPDATE students
        SET {field} = ?
        WHERE LOWER(nama) = LOWER(?)
    """, (new_value, nama))

    conn.commit()

    if cursor.rowcount > 0:
        print(f"\n✅ Updated {nama}: {field} = {new_value}")
    else:
        print(f"\n❌ Student not found: {nama}")

    conn.close()

def delete_student(nama):
    """Delete student by name"""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE LOWER(nama) = LOWER(?)", (nama,))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"\n✅ Deleted student: {nama}")
    else:
        print(f"\n❌ Student not found: {nama}")

    conn.close()

def run_custom_query(query):
    """Run custom SQL query"""
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            conn.commit()
            print(f"\n✅ Query executed. Rows affected: {cursor.rowcount}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

    conn.close()

def view_schema():
    """View database schema"""
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
    schema = cursor.fetchone()[0]

    print("\n=== DATABASE SCHEMA ===")
    print(schema)

    conn.close()

# ===== INTERACTIVE MENU =====

def menu():
    """Interactive menu"""
    while True:
        print("\n" + "="*50)
        print("WMU STUDENTS DATABASE - ADMIN PANEL")
        print("="*50)
        print("1. View all students")
        print("2. Search student")
        print("3. Count students")
        print("4. Add new student")
        print("5. Update student")
        print("6. Delete student")
        print("7. Run custom SQL query")
        print("8. View database schema")
        print("9. Exit")
        print("="*50)

        choice = input("\nSelect option (1-9): ").strip()

        if choice == '1':
            view_all_students()

        elif choice == '2':
            name = input("Enter student name (or part of it): ")
            search_student(name)

        elif choice == '3':
            count_students()

        elif choice == '4':
            print("\n--- ADD NEW STUDENT ---")
            nama = input("Name: ")
            jurusan = input("Major: ")
            university = input("University: ")
            year = input("Year: ")
            provinsi = input("Province: ")
            add_student(nama, jurusan, university, year, provinsi)

        elif choice == '5':
            print("\n--- UPDATE STUDENT ---")
            nama = input("Student name: ")
            field = input("Field to update (jurusan/university/year/provinsi): ")
            new_value = input("New value: ")
            update_student(nama, field, new_value)

        elif choice == '6':
            nama = input("Student name to delete: ")
            confirm = input(f"⚠️  Delete {nama}? (yes/no): ")
            if confirm.lower() == 'yes':
                delete_student(nama)

        elif choice == '7':
            print("\n--- CUSTOM SQL QUERY ---")
            query = input("Enter SQL: ")
            run_custom_query(query)

        elif choice == '8':
            view_schema()

        elif choice == '9':
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid option")

if __name__ == '__main__':
    menu()
