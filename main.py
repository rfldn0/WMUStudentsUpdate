from flask import Flask, request, jsonify
from flask_cors import CORS
from openpyxl import load_workbook

app = Flask(__name__)
CORS(app)

# Configuration
EXCEL_FILE = 'WMU Stuedents Upgrade 1.xlsx'
SHEET_NAME = 'MICHIGAN STUDENTS DATA'
DATA_START_ROW = 4  # First data row after headers
NAMA_COLUMN = 4
IDN_COLUMN = 3
JURUSAN_COLUMN = 5
UNIVERSITY_COLUMN = 6
YEAR_COLUMN = 7
PROVINSI_COLUMN = 8

def open_workbook():
    """Open and return workbook and worksheet"""
    wb = load_workbook(EXCEL_FILE)
    ws = wb[SHEET_NAME]
    return wb, ws

def find_student(ws, nama):
    """
    Find student by name (case-insensitive)
    Returns: row_number or None
    """
    nama_lower = nama.lower().strip()
    for idx in range(DATA_START_ROW, ws.max_row + 1):
        cell_value = ws.cell(row=idx, column=NAMA_COLUMN).value
        if cell_value and cell_value.lower().strip() == nama_lower:
            return idx
    return None

def get_next_idn(ws):
    """Get the next IDN number"""
    max_idn = 0
    for idx in range(DATA_START_ROW, ws.max_row + 1):
        idn_value = ws.cell(row=idx, column=IDN_COLUMN).value
        if idn_value and isinstance(idn_value, (int, float)):
            max_idn = max(max_idn, int(idn_value))
    return max_idn + 1

def save_student_data(ws, row_num, nama, jurusan, university, year, provinsi, idn=None):
    """Save student data to specified row"""
    if idn:
        ws.cell(row=row_num, column=IDN_COLUMN, value=idn)
    ws.cell(row=row_num, column=NAMA_COLUMN, value=nama)
    ws.cell(row=row_num, column=JURUSAN_COLUMN, value=jurusan)
    ws.cell(row=row_num, column=UNIVERSITY_COLUMN, value=university)
    ws.cell(row=row_num, column=YEAR_COLUMN, value=year)
    ws.cell(row=row_num, column=PROVINSI_COLUMN, value=provinsi)

def update_or_add_student(data):
    """Update existing student or add new one"""
    nama = data.get('nama', '').strip()
    jurusan = data.get('jurusan', '').strip()
    university = data.get('university', '').strip()
    year = data.get('year', '').strip()
    provinsi = data.get('provinsi', '').strip()

    if not nama:
        return {'status': 'error', 'message': 'Nama is required'}

    wb, ws = open_workbook()
    row_num = find_student(ws, nama)

    response_data = {
        'nama': nama,
        'jurusan': jurusan,
        'university': university,
        'year': year,
        'provinsi': provinsi
    }

    if row_num:
        # Update existing student
        save_student_data(ws, row_num, nama, jurusan, university, year, provinsi)
        wb.save(EXCEL_FILE)
        wb.close()
        return {
            'status': 'updated',
            'message': f'Successfully updated record for {nama}',
            'data': response_data
        }
    else:
        # Add new student
        new_row = ws.max_row + 1
        idn = get_next_idn(ws)
        save_student_data(ws, new_row, nama, jurusan, university, year, provinsi, idn)
        wb.save(EXCEL_FILE)
        wb.close()
        response_data['idn'] = idn
        return {
            'status': 'added',
            'message': f'Successfully added new record for {nama}',
            'data': response_data
        }

@app.route('/')
def index():
    """Root endpoint - redirects to GitHub Pages"""
    return jsonify({
        'message': 'WMU Student Update API',
        'frontend': 'https://rfldn0.github.io/WMUStudentsUpdate/',
        'endpoints': {
            '/submit': 'POST - Submit student data (form-data)',
            '/api/submit': 'POST - Submit student data (JSON)'
        }
    })

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
