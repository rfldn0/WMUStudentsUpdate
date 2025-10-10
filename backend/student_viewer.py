"""
StudentViewer - Handles student data viewing operations
"""

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from datetime import datetime, timedelta


class StudentViewer:
    """Handles student data viewing operations"""

    def __init__(self, manager):
        self.manager = manager

    def view_all(self):
        """View all students with sorting options"""
        print("\n=== SORT BY ===")
        print("1. Last changed")
        print("2. First name")
        print("3. ID")

        sort_choice = input("\nSelect sorting option (1-3): ").strip()
        students = self.manager.get_all_students()

        if not students:
            print("[INFO] No students found")
            return

        # Sort based on choice
        if sort_choice == '1':
            students.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
            sort_label = "Last Changed"
        elif sort_choice == '2':
            students.sort(key=lambda x: x.get('nama', '').lower())
            sort_label = "Name (A-Z)"
        else:
            students.sort(key=lambda x: int(x['idn']))
            sort_label = "ID"

        self._display_students_table(students, f"Sorted by: {sort_label}")

    def view_recent_changes(self):
        """View recently changed students"""
        print("\n=== VIEW RECENT CHANGES ===")
        print("1. Last 24 hours")
        print("2. Last 7 days")
        print("3. Last 30 days")
        print("4. Custom days")

        choice = input("\nSelect time range (1-4): ").strip()

        days_map = {'1': 1, '2': 7, '3': 30}
        days = days_map.get(choice)

        if choice == '4':
            try:
                days = int(input("Enter number of days: ").strip())
                if days <= 0:
                    print("[ERROR] Days must be positive")
                    return
            except ValueError:
                print("[ERROR] Invalid number")
                return
        elif not days:
            print("[ERROR] Invalid option")
            return

        students = self.manager.get_all_students()
        cutoff_time = datetime.now(self.manager.timezone) - timedelta(days=days)

        recent_students = []
        for student in students:
            updated_at_str = student.get('updated_at', '')
            if updated_at_str and 'T' in updated_at_str:
                try:
                    timestamp_part = updated_at_str.split('+')[0].split('-')[0] if '+' in updated_at_str else updated_at_str
                    updated_at = datetime.fromisoformat(timestamp_part.replace('Z', ''))
                    if updated_at.tzinfo is None:
                        updated_at = updated_at.replace(tzinfo=self.manager.timezone)
                    if updated_at >= cutoff_time:
                        recent_students.append(student)
                except:
                    pass

        if recent_students:
            recent_students.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
            print(f"\n{'='*130}")
            print(f"Recent changes in the last {days} day(s) - {len(recent_students)} student(s)")
            print(f"{'='*130}")
            print(f"{'IDN':<6} {'NAMA':<25} {'JURUSAN':<20} {'YEAR':<10} {'PROVINSI':<15} {'UPDATED':<25}")
            print("="*130)

            for student in recent_students:
                print(f"{int(student['idn']):<6} "
                      f"{student.get('nama', 'N/A'):<25} "
                      f"{student.get('jurusan', 'N/A'):<20} "
                      f"{student.get('year', 'N/A'):<10} "
                      f"{student.get('provinsi', 'N/A'):<15} "
                      f"{student.get('updated_at', 'N/A'):<25}")
            print("="*130)
        else:
            print(f"\n[INFO] No changes found in the last {days} day(s)")

    def search_student(self, name):
        """Search student by name"""
        try:
            response = self.manager.table.scan(FilterExpression=Attr('nama').contains(name))
            students = response['Items']

            if students:
                print(f"\n=== FOUND {len(students)} STUDENT(S) ===")
                for student in students:
                    self._display_student_details(student)
            else:
                print(f"\n[INFO] No students found matching: {name}")
        except ClientError as e:
            print(f"[ERROR] {e}")

    def _display_students_table(self, students, title=""):
        """Display students in table format"""
        print(f"\n{'='*120}")
        if title:
            print(title)
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

    def _display_student_details(self, student):
        """Display detailed student information"""
        print(f"\nIDN: {int(student['idn'])}")
        print(f"Name: {student.get('nama', 'N/A')}")
        print(f"Major: {student.get('jurusan', 'N/A')}")
        print(f"University: {student.get('university', 'N/A')}")
        print(f"Year: {student.get('year', 'N/A')}")
        print(f"Province: {student.get('provinsi', 'N/A')}")
        print(f"Created: {student.get('created_at', 'N/A')}")
        print(f"Updated: {student.get('updated_at', 'N/A')}")
