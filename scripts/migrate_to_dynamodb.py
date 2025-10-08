#!/usr/bin/env python3
"""
Migrate data from SQLite to DynamoDB
Run this once after creating the DynamoDB table
"""

import boto3
import sqlite3
import os
from decimal import Decimal
from datetime import datetime

# Configuration
SQLITE_DB = os.path.join('backend', 'students.db')
DYNAMODB_TABLE = 'wmu-students'
REGION = 'us-east-1'

def get_sqlite_students():
    """Get all students from SQLite"""
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students ORDER BY idn')
    students = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return students

def migrate_to_dynamodb(students):
    """Migrate students to DynamoDB"""
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)

    successful = 0
    failed = 0

    print(f"\nMigrating {len(students)} students to DynamoDB...")
    print("-" * 60)

    for student in students:
        try:
            # Convert to DynamoDB format
            # DynamoDB doesn't support empty strings, convert to None
            item = {
                'idn': student['idn'],
                'nama': student['nama'] or 'Unknown',
                'jurusan': student.get('jurusan') or 'Not specified',
                'university': student.get('university') or 'Not specified',
                'year': student.get('year') or 'Not specified',
                'provinsi': student.get('provinsi') or 'Not specified',
                'created_at': student.get('created_at') or datetime.now().isoformat(),
                'updated_at': student.get('updated_at') or datetime.now().isoformat()
            }

            # Put item to DynamoDB
            table.put_item(Item=item)

            print(f"✅ Migrated: {student['nama']} (IDN: {student['idn']})")
            successful += 1

        except Exception as e:
            print(f"❌ Failed: {student['nama']} - {e}")
            failed += 1

    print("-" * 60)
    print(f"\n✅ Migration complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

def verify_migration():
    """Verify data in DynamoDB"""
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)

    # Get table item count
    response = table.scan(Select='COUNT')
    count = response['Count']

    print(f"\n📊 Verification:")
    print(f"Items in DynamoDB: {count}")

    # Get SQLite count
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM students')
    sqlite_count = cursor.fetchone()[0]
    conn.close()

    print(f"Items in SQLite: {sqlite_count}")

    if count == sqlite_count:
        print("✅ Counts match! Migration successful.")
    else:
        print(f"⚠️  Count mismatch! {sqlite_count - count} items missing.")

if __name__ == '__main__':
    print("="*60)
    print("SQLite to DynamoDB Migration")
    print("="*60)

    # Check if SQLite database exists
    if not os.path.exists(SQLITE_DB):
        print(f"❌ SQLite database not found: {SQLITE_DB}")
        exit(1)

    # Get students from SQLite
    students = get_sqlite_students()
    print(f"Found {len(students)} students in SQLite")

    # Confirm migration
    confirm = input(f"\nMigrate {len(students)} students to DynamoDB? (yes/no): ")

    if confirm.lower() == 'yes':
        migrate_to_dynamodb(students)
        verify_migration()
    else:
        print("Cancelled.")
