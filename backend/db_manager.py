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
    """View all students in table format with sorting options"""
    print("\n=== SORT BY ===")
    print("1. Last changed (updated_at)")
    print("2. First name (alphabetical)")
    print("3. ID (IDN)")

    sort_choice = input("\nSelect sorting option (1-3): ").strip()

    try:
        response = table.scan()
        students = response['Items']

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Sort based on choice
        if sort_choice == '1':
            students.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
            sort_label = "Last Changed"
        elif sort_choice == '2':
            students.sort(key=lambda x: x.get('nama', '').lower())
            sort_label = "Name (A-Z)"
        elif sort_choice == '3':
            students.sort(key=lambda x: int(x['idn']))
            sort_label = "ID"
        else:
            students.sort(key=lambda x: int(x['idn']))
            sort_label = "ID (default)"

        print(f"\n{'='*120}")
        print(f"Sorted by: {sort_label}")
        print(f"{'='*120}")
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
    """Add new student interactively with option to add multiple"""
    while True:
        print("\n=== ADD NEW STUDENT ===")

        nama = input("Name: ").strip().title()
        if not nama:
            print("[ERROR] Name is required")
            continue

        jurusan = input("Major (Jurusan): ").strip().title()
        university = input("University [Western Michigan University]: ").strip() or "Western Michigan University"
        year = input("Year (e.g., Freshman, FALL 2025): ").strip()
        provinsi = input("Province (Provinsi): ").strip().title()

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

        # Ask if user wants to add more
        add_more = input("\nAdd more students? (yes/no): ").strip().lower()
        if add_more not in ['yes', 'y']:
            break

def edit_student():
    """Edit student data (single or batch)"""
    print("\n=== EDIT STUDENT ===")
    print("1. Edit single student")
    print("2. Edit batch (multiple students)")

    choice = input("\nSelect option (1-2): ").strip()

    if choice == '1':
        edit_single_student()
    elif choice == '2':
        edit_batch_students()
    else:
        print("[ERROR] Invalid option")

def edit_single_student():
    """Edit a single student's data"""
    try:
        idn = int(input("\nEnter student IDN to edit: "))

        # Get student
        response = table.get_item(Key={'idn': idn})

        if 'Item' not in response:
            print(f"[ERROR] Student with IDN {idn} not found")
            return

        student = response['Item']
        print(f"\nCurrent data for: {student.get('nama', 'N/A')}")
        print(f"IDN: {int(student['idn'])}")
        print(f"Name: {student.get('nama', 'N/A')}")
        print(f"Major: {student.get('jurusan', 'N/A')}")
        print(f"University: {student.get('university', 'N/A')}")
        print(f"Year: {student.get('year', 'N/A')}")
        print(f"Province: {student.get('provinsi', 'N/A')}")

        # Edit fields
        while True:
            print("\n=== SELECT FIELD TO EDIT ===")
            print("1. Name (Nama)")
            print("2. Major (Jurusan)")
            print("3. University")
            print("4. Year")
            print("5. Province (Provinsi)")
            print("6. Done editing")

            field_choice = input("\nSelect field (1-6): ").strip()

            if field_choice == '6':
                break

            field_map = {
                '1': ('nama', 'Name'),
                '2': ('jurusan', 'Major'),
                '3': ('university', 'University'),
                '4': ('year', 'Year'),
                '5': ('provinsi', 'Province')
            }

            if field_choice in field_map:
                field_key, field_name = field_map[field_choice]
                current_value = student.get(field_key, 'N/A')
                print(f"\nCurrent {field_name}: {current_value}")
                new_value = input(f"New {field_name}: ").strip()

                if new_value:
                    # Auto-format based on field
                    if field_key in ['nama', 'jurusan', 'provinsi']:
                        new_value = new_value.title()

                    student[field_key] = new_value
                    print(f"[SUCCESS] {field_name} updated to: {new_value}")
                else:
                    print("[INFO] No change made")
            else:
                print("[ERROR] Invalid option")

        # Update timestamp and save
        student['updated_at'] = datetime.now(TIMEZONE).isoformat()
        table.put_item(Item=student)
        print(f"\n[SUCCESS] Student {student['nama']} (IDN: {idn}) updated successfully")

    except ValueError:
        print("[ERROR] IDN must be a number")
    except ClientError as e:
        print(f"[ERROR] {e}")

def edit_batch_students():
    """Edit multiple students with the same change"""
    print("\n=== BATCH EDIT STUDENTS ===")

    # Get list of IDNs
    idns_input = input("Enter student IDNs (comma-separated, e.g., 1,5,12): ").strip()

    try:
        idns = [int(idn.strip()) for idn in idns_input.split(',')]
    except ValueError:
        print("[ERROR] Invalid IDN format. Use comma-separated numbers.")
        return

    if not idns:
        print("[ERROR] No IDNs provided")
        return

    # Show students to be edited
    print(f"\n=== STUDENTS TO BE EDITED ({len(idns)}) ===")
    students_to_edit = []

    for idn in idns:
        try:
            response = table.get_item(Key={'idn': idn})
            if 'Item' in response:
                student = response['Item']
                students_to_edit.append(student)
                print(f"IDN {idn}: {student.get('nama', 'N/A')}")
            else:
                print(f"IDN {idn}: [NOT FOUND]")
        except ClientError as e:
            print(f"IDN {idn}: [ERROR] {e}")

    if not students_to_edit:
        print("[ERROR] No valid students found")
        return

    # Select field to change
    while True:
        print("\n=== SELECT FIELD TO CHANGE FOR ALL ===")
        print("1. Major (Jurusan)")
        print("2. University")
        print("3. Year")
        print("4. Province (Provinsi)")
        print("5. Done editing")

        field_choice = input("\nSelect field (1-5): ").strip()

        if field_choice == '5':
            break

        field_map = {
            '1': ('jurusan', 'Major'),
            '2': ('university', 'University'),
            '3': ('year', 'Year'),
            '4': ('provinsi', 'Province')
        }

        if field_choice in field_map:
            field_key, field_name = field_map[field_choice]
            new_value = input(f"\nNew {field_name} for all selected students: ").strip()

            if not new_value:
                print("[INFO] No change made")
                continue

            # Auto-format based on field
            if field_key in ['jurusan', 'provinsi']:
                new_value = new_value.title()

            # Confirm
            confirm = input(f"\nUpdate {field_name} to '{new_value}' for {len(students_to_edit)} student(s)? (yes/no): ").strip().lower()

            if confirm in ['yes', 'y']:
                # Update all students
                updated_count = 0
                for student in students_to_edit:
                    try:
                        student[field_key] = new_value
                        student['updated_at'] = datetime.now(TIMEZONE).isoformat()
                        table.put_item(Item=student)
                        updated_count += 1
                    except ClientError as e:
                        print(f"[ERROR] Failed to update IDN {student['idn']}: {e}")

                print(f"\n[SUCCESS] Updated {updated_count}/{len(students_to_edit)} student(s)")
            else:
                print("[INFO] Update cancelled")
        else:
            print("[ERROR] Invalid option")

def delete_student():
    """Delete student (single or batch)"""
    print("\n=== REMOVE STUDENT ===")
    print("1. Remove single student")
    print("2. Remove batch (multiple students)")

    choice = input("\nSelect option (1-2): ").strip()

    if choice == '1':
        delete_single_student()
    elif choice == '2':
        delete_batch_students()
    else:
        print("[ERROR] Invalid option")

def delete_single_student():
    """Delete a single student by IDN"""
    try:
        idn = int(input("\nEnter student IDN to delete: "))

        # Get student first
        response = table.get_item(Key={'idn': idn})

        if 'Item' not in response:
            print(f"[ERROR] Student with IDN {idn} not found")
            return

        student = response['Item']
        print(f"\nStudent found:")
        print(f"IDN: {int(student['idn'])}")
        print(f"Name: {student.get('nama', 'N/A')}")
        print(f"Major: {student.get('jurusan', 'N/A')}")
        print(f"University: {student.get('university', 'N/A')}")

        confirm = input("\nAre you sure you want to delete? (yes/no): ").strip().lower()

        if confirm in ['yes', 'y']:
            table.delete_item(Key={'idn': idn})
            print(f"[SUCCESS] Deleted student {student.get('nama', 'N/A')} (IDN: {idn})")
        else:
            print("[INFO] Deletion cancelled")

    except ValueError:
        print("[ERROR] IDN must be a number")
    except ClientError as e:
        print(f"[ERROR] {e}")

def delete_batch_students():
    """Delete multiple students"""
    print("\n=== BATCH REMOVE STUDENTS ===")

    # Get list of IDNs
    idns_input = input("Enter student IDNs to delete (comma-separated, e.g., 1,5,12): ").strip()

    try:
        idns = [int(idn.strip()) for idn in idns_input.split(',')]
    except ValueError:
        print("[ERROR] Invalid IDN format. Use comma-separated numbers.")
        return

    if not idns:
        print("[ERROR] No IDNs provided")
        return

    # Show students to be deleted
    print(f"\n=== STUDENTS TO BE DELETED ({len(idns)}) ===")
    students_to_delete = []

    for idn in idns:
        try:
            response = table.get_item(Key={'idn': idn})
            if 'Item' in response:
                student = response['Item']
                students_to_delete.append(student)
                print(f"IDN {idn}: {student.get('nama', 'N/A')}")
            else:
                print(f"IDN {idn}: [NOT FOUND]")
        except ClientError as e:
            print(f"IDN {idn}: [ERROR] {e}")

    if not students_to_delete:
        print("[ERROR] No valid students found")
        return

    # Confirm deletion
    confirm = input(f"\n⚠️  Delete {len(students_to_delete)} student(s)? This cannot be undone! (yes/no): ").strip().lower()

    if confirm in ['yes', 'y']:
        deleted_count = 0
        for student in students_to_delete:
            try:
                table.delete_item(Key={'idn': int(student['idn'])})
                print(f"✓ Deleted: {student.get('nama', 'N/A')} (IDN: {student['idn']})")
                deleted_count += 1
            except ClientError as e:
                print(f"✗ Failed to delete IDN {student['idn']}: {e}")

        print(f"\n[SUCCESS] Deleted {deleted_count}/{len(students_to_delete)} student(s)")
    else:
        print("[INFO] Deletion cancelled")

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
        print("1.  Add new student(s)")
        print("2.  Edit student (single/batch)")
        print("3.  Show data (with sorting)")
        print("4.  Generate CSV export")
        print("5.  Remove student (single/batch)")
        print("6.  Search student by name")
        print("7.  Count total students")
        print("8.  Count by major")
        print("9.  Count by province")
        print("10. Count graduated students")
        print("11. Exit")
        print("="*60)

        choice = input("\nSelect option (1-11): ").strip()

        match choice:
            case '1':
                add_student()
            case '2':
                edit_student()
            case '3':
                view_all_students()
            case '4':
                export_to_csv()
            case '5':
                delete_student()
            case '6':
                name = input("Enter student name (or part of it): ")
                search_student(name)
            case '7':
                count_students()
            case '8':
                count_by_major()
            case '9':
                count_by_province()
            case '10':
                count_graduated_students()
            case '11':
                print("\nGoodbye!")
                break
            case _:
                print("[ERROR] Invalid option. Please select 1-11.")

if __name__ == '__main__':
    menu()
