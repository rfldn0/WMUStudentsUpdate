from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
DB_FILE = 'students.db'

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def find_student(nama):
    """
    Find student by name (case-insensitive)
    Returns: student record or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM students WHERE LOWER(nama) = LOWER(?)',
        (nama.strip(),)
    )
    student = cursor.fetchone()
    conn.close()

    return dict(student) if student else None

def get_next_idn():
    """Get the next IDN number"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(idn) FROM students')
    max_idn = cursor.fetchone()[0]
    conn.close()

    return (max_idn or 0) + 1

def update_or_add_student(data):
    """Update existing student or add new one"""
    nama = data.get('nama', '').strip()
    jurusan = data.get('jurusan', '').strip()
    university = data.get('university', '').strip()
    year = data.get('year', '').strip()
    provinsi = data.get('provinsi', '').strip()

    if not nama:
        return {'status': 'error', 'message': 'Nama is required'}

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if student exists
    existing = find_student(nama)

    response_data = {
        'nama': nama,
        'jurusan': jurusan,
        'university': university,
        'year': year,
        'provinsi': provinsi
    }

    try:
        if existing:
            # Update existing student
            cursor.execute('''
                UPDATE students
                SET jurusan = ?, university = ?, year = ?, provinsi = ?, updated_at = ?
                WHERE LOWER(nama) = LOWER(?)
            ''', (jurusan, university, year, provinsi, datetime.now(), nama))

            conn.commit()
            conn.close()

            response_data['idn'] = existing['idn']
            return {
                'status': 'updated',
                'message': f'Successfully updated record for {nama}',
                'data': response_data
            }
        else:
            # Add new student
            idn = get_next_idn()

            cursor.execute('''
                INSERT INTO students (idn, nama, jurusan, university, year, provinsi)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (idn, nama, jurusan, university, year, provinsi))

            conn.commit()
            conn.close()

            response_data['idn'] = idn
            return {
                'status': 'added',
                'message': f'Successfully added new record for {nama}',
                'data': response_data
            }
    except sqlite3.IntegrityError as e:
        conn.close()
        return {'status': 'error', 'message': f'Database error: {str(e)}'}
    except Exception as e:
        conn.close()
        return {'status': 'error', 'message': f'Error: {str(e)}'}

@app.route('/')
def index():
    """Root endpoint - API information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM students')
    total = cursor.fetchone()[0]
    conn.close()

    return jsonify({
        'message': 'WMU Student Update API',
        'database': 'SQLite',
        'total_students': total,
        'frontend': 'https://rfldn0.github.io/WMUStudentsUpdate/',
        'endpoints': {
            '/submit': 'POST - Submit student data (form-data or JSON)',
            '/api/submit': 'POST - Submit student data (alias)',
            '/students': 'GET - List all students',
            '/students/<nama>': 'GET - Get student by name'
        }
    })

@app.route('/students', methods=['GET'])
def list_students():
    """List all students"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students ORDER BY nama')
    students = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'status': 'success',
        'count': len(students),
        'data': students
    })

@app.route('/students/<nama>', methods=['GET'])
def get_student(nama):
    """Get student by name"""
    student = find_student(nama)

    if student:
        return jsonify({
            'status': 'success',
            'data': student
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Student not found'
        }), 404

@app.route('/submit', methods=['POST'])
@app.route('/api/submit', methods=['POST'])
def submit():
    """Handle form and JSON submissions"""
    try:
        # Accept both form-data and JSON
        data = request.get_json() if request.is_json else request.form.to_dict()
        result = update_or_add_student(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
