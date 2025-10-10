#!/usr/bin/env python3
"""
DynamoDB Table Manager - View and manage student data
Usage: python backend/db_manager.py

This is the main entry point for the WMU Students Database Manager.
All classes are modularized in separate files for better organization.
"""

from zoneinfo import ZoneInfo
from student_manager import StudentManager
from student_viewer import StudentViewer
from student_editor import StudentEditor
from csv_exporter import CSVExporter
from menu_system import MenuSystem

# Configuration
DYNAMODB_TABLE = 'wmu-students'
REGION = 'us-east-1'
TIMEZONE = ZoneInfo('America/Detroit')


def main():
    """Main application entry point"""
    # Initialize core manager
    manager = StudentManager(DYNAMODB_TABLE, REGION, TIMEZONE)

    # Initialize feature modules
    viewer = StudentViewer(manager)
    editor = StudentEditor(manager)
    exporter = CSVExporter(manager)

    # Initialize menu system
    menu_system = MenuSystem(manager, viewer, editor, exporter)

    # Start application
    menu_system.main_menu()


if __name__ == '__main__':
    main()
