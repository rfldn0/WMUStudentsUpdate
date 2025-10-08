from main import update_or_add_student

# Test data
test_data = {
    'nama': 'Junior Frank',
    'jurusan': 'Cybersecurity',
    'university': 'Western Michigan University',
    'year': 'FALL 2025',
    'provinsi': 'Papua Selatan'
}

try:
    result = update_or_add_student(test_data)
    print("Success!")
    print(result)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
