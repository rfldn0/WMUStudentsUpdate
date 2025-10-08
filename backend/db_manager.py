#!/usr/bin/env python3
"""
DynamoDB Table Manager - View and manage student data
Usage: python backend/db_manager.py
"""

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
from zoneinfo import ZoneInfo

# Configuration
DYNAMODB_TABLE = 'wmu-students'
REGION = 'us-east-1'
TIMEZONE = ZoneInfo('America/Detroit')  # Eastern Time (Michigan)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

def view_all_students():
    """View all students in table format"""
    try:
        response = table.scan()
        students = response['Items']

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Sort by IDN
        students.sort(key=lambda x: int(x['idn']))

        print("\n" + "="*120)
        print(f"{'IDN':<6} {'NAMA':<25} {'JURUSAN':<20} {'UNIVERSITY':<30} {'YEAR':<10} {'PROVINSI':<15}")
        print("="*120)

        for student in students:
            print(f"{int(student['idn']):<6} "
                  f"{student.get('nama', 'N/A'):<25} "
                  f"{student.get('jurusan', 'N/A'):<20} "
                  f"{student.get('university', 'N/A'):<30} "
                  f"{student.get('year', 'N/A'):<10} "
                  f"{student.get('provinsi', 'N/A'):<15}")

        print("="*120)
        print(f"Total: {len(students)} students")

    except ClientError as e:
        print(f"[ERROR] {e}")

def search_student(name):
    """Search student by name"""
    try:
        response = table.scan(
            FilterExpression=Attr('nama').contains(name)
        )

        students = response['Items']

        if students:
            print(f"\n=== FOUND {len(students)} STUDENT(S) ===")
            for student in students:
                print(f"\nIDN: {int(student['idn'])}")
                print(f"Name: {student.get('nama', 'N/A')}")
                print(f"Major: {student.get('jurusan', 'N/A')}")
                print(f"University: {student.get('university', 'N/A')}")
                print(f"Year: {student.get('year', 'N/A')}")
                print(f"Province: {student.get('provinsi', 'N/A')}")
                print(f"Created: {student.get('created_at', 'N/A')}")
                print(f"Updated: {student.get('updated_at', 'N/A')}")
        else:
            print(f"\n[INFO] No students found matching: {name}")

    except ClientError as e:
        print(f"[ERROR] {e}")

def count_students():
    """Count total students"""
    try:
        response = table.scan(Select='COUNT')
        count = response['Count']
        print(f"\nTotal Students in DynamoDB: {count}")
    except ClientError as e:
        print(f"[ERROR] {e}")

def count_by_major():
    """Count students by major"""
    try:
        response = table.scan()
        students = response['Items']

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Count by major
        majors = {}
        for student in students:
            major = student.get('jurusan', 'Not specified')
            majors[major] = majors.get(major, 0) + 1

        print("\n=== STUDENTS BY MAJOR ===")
        for major, count in sorted(majors.items(), key=lambda x: x[1], reverse=True):
            print(f"{major}: {count}")

        print(f"\nTotal Majors: {len(majors)}")

    except ClientError as e:
        print(f"[ERROR] {e}")

def count_by_province():
    """Count students by province"""
    try:
        response = table.scan()
        students = response['Items']

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Count by province
        provinces = {}
        for student in students:
            province = student.get('provinsi', 'Not specified')
            provinces[province] = provinces.get(province, 0) + 1

        print("\n=== STUDENTS BY PROVINCE ===")
        for province, count in sorted(provinces.items(), key=lambda x: x[1], reverse=True):
            print(f"{province}: {count}")

        print(f"\nTotal Provinces: {len(provinces)}")

    except ClientError as e:
        print(f"[ERROR] {e}")

def count_graduated_students():
    """Count graduated students (those with semester graduation format like 'FALL 2025')"""
    try:
        response = table.scan()
        students = response['Items']

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Define current student year options
        current_student_years = ['Freshman', 'Sophomore', 'Junior', 'Senior', '']

        # Count graduated vs current students
        graduated = []
        current_students = []

        for student in students:
            year = student.get('year', '').strip()

            # Check if it's a graduated student (not in current student years)
            if year and year not in current_student_years:
                graduated.append(student)
            else:
                current_students.append(student)

        print("\n=== STUDENT STATUS BREAKDOWN ===")
        print(f"Total Students: {len(students)}")
        print(f"Graduated Students: {len(graduated)}")
        print(f"Current Students: {len(current_students)}")

        if graduated:
            print("\n=== GRADUATED STUDENTS ===")
            print(f"{'IDN':<6} {'NAME':<30} {'GRADUATION':<20}")
            print("="*60)
            for student in sorted(graduated, key=lambda x: x.get('year', '')):
                print(f"{int(student['idn']):<6} "
                      f"{student.get('nama', 'N/A'):<30} "
                      f"{student.get('year', 'N/A'):<20}")

    except ClientError as e:
        print(f"[ERROR] {e}")

def add_student():
    """Add new student interactively"""
    print("\n=== ADD NEW STUDENT ===")

    nama = input("Name: ").strip().title()
    jurusan = input("Major: ").strip().title()
    university = input("University: ").strip()
    year = input("Year: ").strip()
    provinsi = input("Province: ").strip().title()

    if not nama:
        print("[ERROR] Name is required")
        return

    try:
        # Get next IDN
        response = table.scan(ProjectionExpression='idn')
        if response['Items']:
            max_idn = max([int(item['idn']) for item in response['Items']])
            new_idn = max_idn + 1
        else:
            new_idn = 1

        # Add student
        table.put_item(
            Item={
                'idn': new_idn,
                'nama': nama,
                'jurusan': jurusan,
                'university': university,
                'year': year,
                'provinsi': provinsi,
                'created_at': datetime.now(TIMEZONE).isoformat(),
                'updated_at': datetime.now(TIMEZONE).isoformat()
            }
        )

        print(f"\n[SUCCESS] Added student: {nama} (IDN: {new_idn})")

    except ClientError as e:
        print(f"[ERROR] {e}")

def delete_student():
    """Delete student by IDN"""
    try:
        idn = int(input("Enter student IDN to delete: "))

        # Get student first
        response = table.get_item(Key={'idn': idn})

        if 'Item' not in response:
            print(f"[ERROR] Student with IDN {idn} not found")
            return

        student = response['Item']
        print(f"\nStudent found: {student.get('nama', 'N/A')}")

        confirm = input("Are you sure you want to delete? (yes/no): ")

        if confirm.lower() == 'yes':
            table.delete_item(Key={'idn': idn})
            print(f"[SUCCESS] Deleted student IDN {idn}")
        else:
            print("Cancelled")

    except ValueError:
        print("[ERROR] IDN must be a number")
    except ClientError as e:
        print(f"[ERROR] {e}")

def export_to_csv():
    """Export all students to CSV"""
    import csv

    try:
        response = table.scan()
        students = response['Items']

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Sort by IDN
        students.sort(key=lambda x: int(x['idn']))

        # Write to CSV
        filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['idn', 'nama', 'jurusan', 'university', 'year', 'provinsi', 'created_at', 'updated_at'])
            writer.writeheader()

            for student in students:
                writer.writerow({
                    'idn': int(student['idn']),
                    'nama': student.get('nama', ''),
                    'jurusan': student.get('jurusan', ''),
                    'university': student.get('university', ''),
                    'year': student.get('year', ''),
                    'provinsi': student.get('provinsi', ''),
                    'created_at': student.get('created_at', ''),
                    'updated_at': student.get('updated_at', '')
                })

        print(f"\n[SUCCESS] Exported {len(students)} students to {filename}")

    except Exception as e:
        print(f"[ERROR] {e}")

def menu():
    """Interactive menu"""
    while True:
        print("\n" + "="*60)
        print("WMU STUDENTS - DYNAMODB MANAGER")
        print("="*60)
        print("1.  View all students (table)")
        print("2.  Search student by name")
        print("3.  Count total students")
        print("4.  Count by major")
        print("5.  Count by province")
        print("6.  Count graduated students")
        print("7.  Add new student")
        print("8.  Delete student")
        print("9.  Export to CSV")
        print("10. Exit")
        print("="*60)

        choice = input("\nSelect option (1-10): ").strip()

        if choice == '1':
            view_all_students()
        elif choice == '2':
            name = input("Enter student name (or part of it): ")
            search_student(name)
        elif choice == '3':
            count_students()
        elif choice == '4':
            count_by_major()
        elif choice == '5':
            count_by_province()
        elif choice == '6':
            count_graduated_students()
        elif choice == '7':
            add_student()
        elif choice == '8':
            delete_student()
        elif choice == '9':
            export_to_csv()
        elif choice == '10':
            print("\nGoodbye!")
            break
        else:
            print("[ERROR] Invalid option")

if __name__ == '__main__':
    menu()
