"""
MenuSystem - Manages menu navigation
"""


class MenuSystem:
    """Manages menu navigation"""

    def __init__(self, manager, viewer, editor, exporter):
        self.manager = manager
        self.viewer = viewer
        self.editor = editor
        self.exporter = exporter

    def view_menu(self):
        """View submenu"""
        while True:
            print("\n" + "="*60)
            print("VIEW DATA")
            print("="*60)
            print("1. Show all students (with sorting)")
            print("2. Show recent changes")
            print("3. Search student by name")
            print("4. Back to main menu")
            print("="*60)

            choice = input("\nSelect option (1-4): ").strip()

            if choice == '1':
                self.viewer.view_all()
            elif choice == '2':
                self.viewer.view_recent_changes()
            elif choice == '3':
                name = input("Enter student name (or part of it): ")
                self.viewer.search_student(name)
            elif choice == '4':
                break
            else:
                print("[ERROR] Invalid option")

    def manage_menu(self):
        """Manage submenu"""
        while True:
            print("\n" + "="*60)
            print("MANAGE STUDENTS")
            print("="*60)
            print("1. Add new student(s)")
            print("2. Edit student (single/batch)")
            print("3. Remove student (single/batch)")
            print("4. Back to main menu")
            print("="*60)

            choice = input("\nSelect option (1-4): ").strip()

            if choice == '1':
                self.editor.add_student()
            elif choice == '2':
                self.editor.edit_student()
            elif choice == '3':
                self.editor.delete_student()
            elif choice == '4':
                break
            else:
                print("[ERROR] Invalid option")

    def analytics_menu(self):
        """Analytics submenu"""
        while True:
            print("\n" + "="*60)
            print("ANALYTICS & STATISTICS")
            print("="*60)
            print("1. Count total students")
            print("2. Count by major")
            print("3. Count by province")
            print("4. Count graduated students")
            print("5. Back to main menu")
            print("="*60)

            choice = input("\nSelect option (1-5): ").strip()

            if choice == '1':
                self.manager.count_total()
            elif choice == '2':
                self.manager.count_by_field('jurusan', 'Major')
            elif choice == '3':
                self.manager.count_by_field('provinsi', 'Province')
            elif choice == '4':
                self.manager.count_graduated()
            elif choice == '5':
                break
            else:
                print("[ERROR] Invalid option")

    def main_menu(self):
        """Main menu"""
        while True:
            print("\n" + "="*60)
            print("WMU STUDENTS - DYNAMODB MANAGER")
            print("="*60)
            print("1. View Data")
            print("2. Manage Students")
            print("3. Analytics & Statistics")
            print("4. Generate CSV Export")
            print("5. Exit")
            print("="*60)

            choice = input("\nSelect option (1-5): ").strip()

            if choice == '1':
                self.view_menu()
            elif choice == '2':
                self.manage_menu()
            elif choice == '3':
                self.analytics_menu()
            elif choice == '4':
                self.exporter.export_to_csv()
            elif choice == '5':
                print("\nGoodbye!")
                break
            else:
                print("[ERROR] Invalid option")
