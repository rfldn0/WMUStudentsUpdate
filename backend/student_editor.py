"""
StudentEditor - Handles student data editing operations
"""

from botocore.exceptions import ClientError
from datetime import datetime


class StudentEditor:
    """Handles student data editing operations"""

    def __init__(self, manager):
        self.manager = manager

    def add_student(self):
        """Add new student(s) with continuous input"""
        while True:
            print("\n=== ADD NEW STUDENT ===")

            nama = input("Name: ").strip().title()
            if not nama:
                print("[ERROR] Name is required")
                continue

            jurusan = input("Major: ").strip().title()
            university = input("University [Western Michigan University]: ").strip() or "Western Michigan University"
            year = input("Year: ").strip()
            provinsi = input("Province: ").strip().title()

            try:
                new_idn = self.manager.get_next_idn()

                self.manager.table.put_item(
                    Item={
                        'idn': new_idn,
                        'nama': nama,
                        'jurusan': jurusan,
                        'university': university,
                        'year': year,
                        'provinsi': provinsi,
                        'created_at': datetime.now(self.manager.timezone).isoformat(),
                        'updated_at': datetime.now(self.manager.timezone).isoformat()
                    }
                )

                print(f"\n[SUCCESS] Added student: {nama} (IDN: {new_idn})")
            except ClientError as e:
                print(f"[ERROR] {e}")

            add_more = input("\nAdd more students? (yes/no): ").strip().lower()
            if add_more not in ['yes', 'y']:
                break

    def edit_student(self):
        """Edit student - single or batch"""
        print("\n=== EDIT STUDENT ===")
        print("1. Edit single student")
        print("2. Edit batch")

        choice = input("\nSelect option (1-2): ").strip()

        if choice == '1':
            self._edit_single()
        elif choice == '2':
            self._edit_batch()
        else:
            print("[ERROR] Invalid option")

    def _edit_single(self):
        """Edit single student"""
        try:
            idn = int(input("\nEnter student IDN: ").strip())
            response = self.manager.table.get_item(Key={'idn': idn})

            if 'Item' not in response:
                print(f"[ERROR] Student with IDN {idn} not found")
                return

            student = response['Item']
            self._display_student_info(student)

            while True:
                print("\n=== SELECT FIELD TO EDIT ===")
                print("1. Name")
                print("2. Major")
                print("3. University")
                print("4. Year")
                print("5. Province")
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
                        if field_key in ['nama', 'jurusan', 'provinsi']:
                            new_value = new_value.title()
                        student[field_key] = new_value
                        print(f"[SUCCESS] {field_name} updated")
                else:
                    print("[ERROR] Invalid option")

            student['updated_at'] = datetime.now(self.manager.timezone).isoformat()
            self.manager.table.put_item(Item=student)
            print(f"\n[SUCCESS] Student {student['nama']} (IDN: {idn}) updated")

        except ValueError:
            print("[ERROR] IDN must be a number")
        except ClientError as e:
            print(f"[ERROR] {e}")

    def _edit_batch(self):
        """Edit multiple students with same change"""
        print("\n=== BATCH EDIT STUDENTS ===")

        idns_input = input("Enter student IDNs (comma-separated): ").strip()

        try:
            idns = [int(idn.strip()) for idn in idns_input.split(',')]
        except ValueError:
            print("[ERROR] Invalid IDN format")
            return

        if not idns:
            print("[ERROR] No IDNs provided")
            return

        students_to_edit = []
        print(f"\n=== STUDENTS TO BE EDITED ({len(idns)}) ===")

        for idn in idns:
            try:
                response = self.manager.table.get_item(Key={'idn': idn})
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

        while True:
            print("\n=== SELECT FIELD TO CHANGE ===")
            print("1. Major")
            print("2. University")
            print("3. Year")
            print("4. Province")
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
                new_value = input(f"\nNew {field_name} for all: ").strip()

                if not new_value:
                    continue

                if field_key in ['jurusan', 'provinsi']:
                    new_value = new_value.title()

                confirm = input(f"\nUpdate {field_name} to '{new_value}' for {len(students_to_edit)} student(s)? (yes/no): ").strip().lower()

                if confirm in ['yes', 'y']:
                    updated_count = 0
                    for student in students_to_edit:
                        try:
                            student[field_key] = new_value
                            student['updated_at'] = datetime.now(self.manager.timezone).isoformat()
                            self.manager.table.put_item(Item=student)
                            updated_count += 1
                        except ClientError as e:
                            print(f"[ERROR] Failed to update IDN {student['idn']}: {e}")

                    print(f"\n[SUCCESS] Updated {updated_count}/{len(students_to_edit)} student(s)")
            else:
                print("[ERROR] Invalid option")

    def delete_student(self):
        """Delete student - single or batch"""
        print("\n=== REMOVE STUDENT ===")
        print("1. Remove single student")
        print("2. Remove batch")

        choice = input("\nSelect option (1-2): ").strip()

        if choice == '1':
            self._delete_single()
        elif choice == '2':
            self._delete_batch()
        else:
            print("[ERROR] Invalid option")

    def _delete_single(self):
        """Delete single student"""
        try:
            idn = int(input("\nEnter student IDN to delete: ").strip())
            response = self.manager.table.get_item(Key={'idn': idn})

            if 'Item' not in response:
                print(f"[ERROR] Student with IDN {idn} not found")
                return

            student = response['Item']
            self._display_student_info(student)

            confirm = input("\nAre you sure you want to delete? (yes/no): ").strip().lower()

            if confirm in ['yes', 'y']:
                self.manager.table.delete_item(Key={'idn': idn})
                print(f"[SUCCESS] Deleted student {student.get('nama', 'N/A')} (IDN: {idn})")
            else:
                print("[INFO] Deletion cancelled")

        except ValueError:
            print("[ERROR] IDN must be a number")
        except ClientError as e:
            print(f"[ERROR] {e}")

    def _delete_batch(self):
        """Delete multiple students"""
        print("\n=== BATCH REMOVE STUDENTS ===")

        idns_input = input("Enter student IDNs to delete (comma-separated): ").strip()

        try:
            idns = [int(idn.strip()) for idn in idns_input.split(',')]
        except ValueError:
            print("[ERROR] Invalid IDN format")
            return

        if not idns:
            print("[ERROR] No IDNs provided")
            return

        students_to_delete = []
        print(f"\n=== STUDENTS TO BE DELETED ({len(idns)}) ===")

        for idn in idns:
            try:
                response = self.manager.table.get_item(Key={'idn': idn})
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

        confirm = input(f"\nDelete {len(students_to_delete)} student(s)? This cannot be undone! (yes/no): ").strip().lower()

        if confirm in ['yes', 'y']:
            deleted_count = 0
            for student in students_to_delete:
                try:
                    self.manager.table.delete_item(Key={'idn': int(student['idn'])})
                    print(f"Deleted: {student.get('nama', 'N/A')} (IDN: {student['idn']})")
                    deleted_count += 1
                except ClientError as e:
                    print(f"Failed to delete IDN {student['idn']}: {e}")

            print(f"\n[SUCCESS] Deleted {deleted_count}/{len(students_to_delete)} student(s)")
        else:
            print("[INFO] Deletion cancelled")

    def _display_student_info(self, student):
        """Display student information"""
        print(f"\nIDN: {int(student['idn'])}")
        print(f"Name: {student.get('nama', 'N/A')}")
        print(f"Major: {student.get('jurusan', 'N/A')}")
        print(f"University: {student.get('university', 'N/A')}")
        print(f"Year: {student.get('year', 'N/A')}")
        print(f"Province: {student.get('provinsi', 'N/A')}")
