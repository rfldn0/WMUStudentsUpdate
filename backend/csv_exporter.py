"""
CSVExporter - Handles CSV export operations
"""

import csv
from datetime import datetime


class CSVExporter:
    """Handles CSV export operations"""

    def __init__(self, manager):
        self.manager = manager

    def export_to_csv(self):
        """Export students to CSV - all or by province"""
        print("\n=== GENERATE CSV EXPORT ===")
        print("1. Export all students")
        print("2. Export by province")

        choice = input("\nSelect option (1-2): ").strip()

        students = self.manager.get_all_students()
        filename_suffix = "_all"

        if choice == '2':
            provinces = sorted(set(s.get('provinsi', 'Not specified') for s in students))

            print("\n=== AVAILABLE PROVINCES ===")
            for i, prov in enumerate(provinces, 1):
                count = sum(1 for s in students if s.get('provinsi', 'Not specified') == prov)
                print(f"{i}. {prov} ({count} students)")

            prov_choice = input(f"\nSelect province (1-{len(provinces)}): ").strip()

            try:
                prov_idx = int(prov_choice) - 1
                if 0 <= prov_idx < len(provinces):
                    selected_province = provinces[prov_idx]
                    students = [s for s in students if s.get('provinsi', 'Not specified') == selected_province]
                    filename_suffix = f"_{selected_province.replace(' ', '_')}"
                else:
                    print("[ERROR] Invalid selection")
                    return
            except ValueError:
                print("[ERROR] Invalid selection")
                return

        students.sort(key=lambda x: int(x['idn']))

        filename = f"students_export{filename_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
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
