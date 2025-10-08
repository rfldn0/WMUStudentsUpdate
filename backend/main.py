from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
CORS(app)

# Configuration
DYNAMODB_TABLE = 'wmu-students'
REGION = 'us-east-1'

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

def decimal_to_int(obj):
    """Convert Decimal to int for JSON serialization"""
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def find_student(nama):
    """
    Find student by name using firstName + lastName matching
    Priority: firstName + lastName match > exact match

    Examples:
    - Input "Jordy Rumayomi" matches "Jordy Alvian Rumayomi" (firstName=Jordy, lastName=Rumayomi)
    - Input "Aprilia Mabel" matches "Aprilia Weni Irjani Mabel" (firstName=Aprilia, lastName=Mabel)

    Returns: student record or None
    """
    try:
        # Get all students
        response = table.scan()
        students = response['Items']

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Extract firstName (first word) and lastName (last word) from input
        nama_parts = nama.strip().split()

        if len(nama_parts) >= 2:
            input_first = nama_parts[0].lower()
            input_last = nama_parts[-1].lower()

            # PRIORITY 1: Check for firstName + lastName match
            for student in students:
                student_name_parts = student.get('nama', '').strip().split()
                if len(student_name_parts) >= 2:
                    student_first = student_name_parts[0].lower()
                    student_last = student_name_parts[-1].lower()

                    # Match if firstName AND lastName both match
                    if student_first == input_first and student_last == input_last:
                        return student

        # PRIORITY 2: Fallback to exact match (case-insensitive)
        for student in students:
            if student.get('nama', '').lower() == nama.lower():
                return student

        return None

    except ClientError as e:
        print(f"Error finding student: {e}")
        return None

def get_next_idn():
    """Get the next IDN number"""
    try:
        # Scan to find max IDN
        response = table.scan(
            ProjectionExpression='idn'
        )

        if not response['Items']:
            return 1

        max_idn = max([int(item['idn']) for item in response['Items']])
        return max_idn + 1

    except ClientError as e:
        print(f"Error getting next IDN: {e}")
        return 1

def update_or_add_student(data):
    """Update existing student or add new one"""
    # Auto-format names to Title Case (Victor Tabuni, Computer Science)
    nama = data.get('nama', '').strip().title()
    jurusan = data.get('jurusan', '').strip().title()
    university = data.get('university', '').strip()
    year = data.get('year', '').strip()
    provinsi = data.get('provinsi', '').strip().title()

    if not nama:
        return {'status': 'error', 'message': 'Nama is required'}

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
            # Update existing student - KEEP the original full name from database
            idn = int(existing['idn'])
            original_nama = existing.get('nama')  # Keep original full name

            table.update_item(
                Key={'idn': idn},
                UpdateExpression='SET jurusan = :j, university = :u, #y = :yr, provinsi = :p, updated_at = :ua',
                ExpressionAttributeValues={
                    ':j': jurusan,
                    ':u': university,
                    ':yr': year,
                    ':p': provinsi,
                    ':ua': datetime.now().isoformat()
                },
                ExpressionAttributeNames={
                    '#y': 'year'  # 'year' is a reserved word in DynamoDB
                }
            )

            # Return response with ORIGINAL full name preserved
            response_data['nama'] = original_nama  # Use database name, not input name
            response_data['idn'] = idn
            return {
                'status': 'updated',
                'message': f'Successfully updated record for {original_nama}',
                'data': response_data
            }
        else:
            # Add new student
            idn = get_next_idn()

            table.put_item(
                Item={
                    'idn': idn,
                    'nama': nama,
                    'jurusan': jurusan,
                    'university': university,
                    'year': year,
                    'provinsi': provinsi,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
            )

            response_data['idn'] = idn
            return {
                'status': 'added',
                'message': f'Successfully added new record for {nama}',
                'data': response_data
            }

    except ClientError as e:
        return {'status': 'error', 'message': f'Database error: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: {str(e)}'}

@app.route('/')
def index():
    """Root endpoint - API information"""
    try:
        # Get total count
        response = table.scan(Select='COUNT')
        total = response['Count']

        return jsonify({
            'message': 'WMU Student Update API',
            'database': 'DynamoDB',
            'total_students': total,
            'frontend': 'https://rfldn0.github.io/WMUStudentsUpdate/',
            'endpoints': {
                '/submit': 'POST - Submit student data (form-data or JSON)',
                '/api/submit': 'POST - Submit student data (alias)',
                '/students': 'GET - List all students',
                '/students/<nama>': 'GET - Get student by name'
            }
        })
    except ClientError as e:
        return jsonify({
            'message': 'WMU Student Update API',
            'database': 'DynamoDB',
            'error': str(e)
        })

@app.route('/students', methods=['GET'])
def list_students():
    """List all students"""
    try:
        response = table.scan()
        students = response['Items']

        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])

        # Sort by name
        students.sort(key=lambda x: x['nama'])

        # Convert Decimal to int for JSON serialization
        for student in students:
            student['idn'] = int(student['idn'])

        return jsonify({
            'status': 'success',
            'count': len(students),
            'data': students
        })

    except ClientError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/students/<nama>', methods=['GET'])
def get_student(nama):
    """Get student by name"""
    student = find_student(nama)

    if student:
        # Convert Decimal to int
        student['idn'] = int(student['idn'])

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
