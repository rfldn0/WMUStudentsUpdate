from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo
import re
import os
from functools import wraps

app = Flask(__name__)

# Security: Strict CORS - only allow your GitHub Pages domain
CORS(app, resources={
    r"/*": {
        "origins": ["https://rfldn0.github.io"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "X-API-Key"],
        "max_age": 3600
    }
})

# Security: Rate limiting to prevent DoS attacks
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Security: Request size limit (1MB)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# Configuration
DYNAMODB_TABLE = 'wmu-students'
REGION = 'us-east-1'
TIMEZONE = ZoneInfo('America/Detroit')  # Eastern Time (Michigan)

# Security: API Key authentication (set via environment variable)
API_KEY = os.environ.get('API_KEY', 'CHANGE_THIS_IN_PRODUCTION')

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

# Security: Input validation patterns
NAME_PATTERN = re.compile(r'^[a-zA-Z\s\-\.]{1,100}$')
FIELD_PATTERN = re.compile(r'^[a-zA-Z\s\-\.&()]{1,100}$')
YEAR_PATTERN = re.compile(r'^(Freshman|Sophomore|Junior|Senior|FALL \d{4}|SPRING \d{4}|SUMMER \d{4})?$')

def require_api_key(f):
    """Decorator to require API key for write operations"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or provided_key != API_KEY:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_input(data):
    """Validate and sanitize user input"""
    errors = []

    # Validate name
    nama = data.get('nama', '').strip()
    if not nama:
        errors.append('Name is required')
    elif len(nama) > 100:
        errors.append('Name must be less than 100 characters')
    elif not NAME_PATTERN.match(nama):
        errors.append('Name contains invalid characters')

    # Validate jurusan (major)
    jurusan = data.get('jurusan', '').strip()
    if jurusan and (len(jurusan) > 100 or not FIELD_PATTERN.match(jurusan)):
        errors.append('Major contains invalid characters or is too long')

    # Validate university
    university = data.get('university', '').strip()
    if university and (len(university) > 100 or not FIELD_PATTERN.match(university)):
        errors.append('University contains invalid characters or is too long')

    # Validate year
    year = data.get('year', '').strip()
    if year and not YEAR_PATTERN.match(year):
        errors.append('Year format is invalid')

    # Validate provinsi
    provinsi = data.get('provinsi', '').strip()
    valid_provinces = ['Papua', 'Papua Selatan', 'Papua Barat', 'Papua Barat Daya',
                      'Papua Tengah', 'Papua Pegunungan', '']
    if provinsi and provinsi not in valid_provinces:
        errors.append('Invalid province')

    return errors

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
    # Security: Validate input first
    validation_errors = validate_input(data)
    if validation_errors:
        return {'status': 'error', 'message': '; '.join(validation_errors)}

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
                    ':ua': datetime.now(TIMEZONE).isoformat()
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
                    'created_at': datetime.now(TIMEZONE).isoformat(),
                    'updated_at': datetime.now(TIMEZONE).isoformat()
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

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle large request payloads"""
    return jsonify({'status': 'error', 'message': 'Request too large'}), 413

@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limit exceeded"""
    return jsonify({'status': 'error', 'message': 'Rate limit exceeded. Please try again later.'}), 429

@app.route('/')
@limiter.limit("10 per minute")
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
            'endpoints': {
                '/submit': 'POST - Submit student data (requires API key)',
                '/api/submit': 'POST - Submit student data (alias, requires API key)',
                '/students': 'GET - List all students',
                '/students/<nama>': 'GET - Get student by name'
            }
        })
    except ClientError:
        return jsonify({
            'message': 'WMU Student Update API',
            'database': 'DynamoDB',
            'error': 'Database unavailable'
        }), 500

@app.route('/students', methods=['GET'])
@limiter.limit("30 per minute")
def list_students():
    """List all students - limited to prevent data scraping"""
    try:
        response = table.scan()
        students = response['Items']

        # Security: Limit pagination to prevent abuse
        page_count = 0
        max_pages = 10
        while 'LastEvaluatedKey' in response and page_count < max_pages:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            students.extend(response['Items'])
            page_count += 1

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

    except ClientError:
        return jsonify({
            'status': 'error',
            'message': 'Unable to retrieve students'
        }), 500

@app.route('/students/<nama>', methods=['GET'])
@limiter.limit("20 per minute")
def get_student(nama):
    """Get student by name"""
    # Security: Validate name input
    if not nama or len(nama) > 100:
        return jsonify({
            'status': 'error',
            'message': 'Invalid name parameter'
        }), 400

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
@limiter.limit("10 per hour")
@require_api_key
def submit():
    """Handle form and JSON submissions - requires API key"""
    try:
        # Accept both form-data and JSON
        data = request.get_json() if request.is_json else request.form.to_dict()

        # Security: Validate content type
        if not (request.is_json or request.content_type.startswith('multipart/form-data')):
            return jsonify({'status': 'error', 'message': 'Invalid content type'}), 400

        result = update_or_add_student(data)

        # Don't return 500 for validation errors
        if result.get('status') == 'error':
            return jsonify(result), 400

        return jsonify(result)
    except Exception:
        return jsonify({'status': 'error', 'message': 'An error occurred processing your request'}), 500

if __name__ == '__main__':
    # Security: Disable debug mode in production
    is_production = os.environ.get('ENVIRONMENT', 'development') == 'production'
    app.run(debug=not is_production, host='0.0.0.0', port=5000)
