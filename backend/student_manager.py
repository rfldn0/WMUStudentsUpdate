"""
StudentManager - Core data operations and DynamoDB interactions
"""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime


class StudentManager:
    """Manages student data operations in DynamoDB"""

    def __init__(self, table_name, region, timezone):
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(table_name)
        self.timezone = timezone
        self.current_year_options = ['Freshman', 'Sophomore', 'Junior', 'Senior', '']

    def get_all_students(self):
        """Fetch all students from DynamoDB with pagination handling"""
        try:
            response = self.table.scan()
            students = response['Items']

            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                students.extend(response['Items'])

            return students
        except ClientError as e:
            print(f"[ERROR] {e}")
            return []

    def get_next_idn(self):
        """Get next available IDN"""
        try:
            response = self.table.scan(ProjectionExpression='idn')
            if response['Items']:
                return max([int(item['idn']) for item in response['Items']]) + 1
            return 1
        except ClientError as e:
            print(f"[ERROR] {e}")
            return 1

    def count_total(self):
        """Count total students"""
        try:
            response = self.table.scan(Select='COUNT')
            count = response['Count']
            print(f"\nTotal Students: {count}")
            return count
        except ClientError as e:
            print(f"[ERROR] {e}")
            return 0

    def count_by_field(self, field_name, display_name):
        """Generic count by field method"""
        students = self.get_all_students()

        field_counts = {}
        for student in students:
            value = student.get(field_name, 'Not specified')
            field_counts[value] = field_counts.get(value, 0) + 1

        print(f"\n=== STUDENTS BY {display_name.upper()} ===")
        for value, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{value}: {count}")

        print(f"\nTotal {display_name}: {len(field_counts)}")
        return field_counts

    def count_graduated(self):
        """Count graduated vs current students"""
        students = self.get_all_students()

        graduated = []
        current_students = []

        for student in students:
            year = student.get('year', '').strip()
            if year and year not in self.current_year_options:
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
