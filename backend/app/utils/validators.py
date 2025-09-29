import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_data(data):
    """Validate user registration data"""
    if not data:
        return False, 'Data tidak boleh kosong'
    
    required_fields = ['username', 'password', 'email', 'nama']
    for field in required_fields:
        if field not in data or not data[field] or not data[field].strip():
            return False, f'Field {field} wajib diisi'
    
    # Validate username length
    if len(data['username']) > 50:
        return False, 'Username tidak boleh lebih dari 50 karakter'
    
    # Validate email format and length
    if len(data['email']) > 100:
        return False, 'Email tidak boleh lebih dari 100 karakter'
    
    if not validate_email(data['email']):
        return False, 'Format email tidak valid'
    
    # Validate nama length
    if len(data['nama']) > 100:
        return False, 'Nama tidak boleh lebih dari 100 karakter'
    
    # Validate password length
    if len(data['password']) < 6:
        return False, 'Password minimal 6 karakter'
    
    if len(data['password']) > 255:
        return False, 'Password tidak boleh lebih dari 255 karakter'
    
    return True, None

def validate_login_data(data):
    """Validate user login data"""
    if not data:
        return False, 'Data tidak boleh kosong'
    
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data or not data[field] or not data[field].strip():
            return False, f'Field {field} wajib diisi'
    
    return True, None

def validate_update_data(data):
    """Validate user update data"""
    if not data:
        return False, 'Data tidak boleh kosong'
    
    # At least one field should be provided
    allowed_fields = ['username', 'email', 'nama']
    has_valid_field = False
    
    for field in allowed_fields:
        if field in data and data[field] and data[field].strip():
            has_valid_field = True
            break
    
    if not has_valid_field:
        return False, 'Minimal satu field harus diisi (username, email, atau nama)'
    
    # Validate field lengths and formats if provided
    if 'username' in data and data['username']:
        if len(data['username']) > 50:
            return False, 'Username tidak boleh lebih dari 50 karakter'
    
    if 'email' in data and data['email']:
        if len(data['email']) > 100:
            return False, 'Email tidak boleh lebih dari 100 karakter'
        if not validate_email(data['email']):
            return False, 'Format email tidak valid'
    
    if 'nama' in data and data['nama']:
        if len(data['nama']) > 100:
            return False, 'Nama tidak boleh lebih dari 100 karakter'
    
    return True, None