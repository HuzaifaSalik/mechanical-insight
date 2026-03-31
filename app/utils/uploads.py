"""Image upload and processing utilities"""
import os
import uuid
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file_size(file):
    """Validate file size is within limit"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE


def generate_unique_filename(filename):
    """Generate a unique filename to prevent overwrites"""
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return unique_name


def save_uploaded_image(file, subfolder='general'):
    """
    Save an uploaded image file with validation and processing.
    
    Args:
        file: FileStorage object from Flask request
        subfolder: Subdirectory within uploads folder
        
    Returns:
        tuple: (success: bool, filename_or_error: str)
    """
    if not file or file.filename == '':
        return False, 'No file selected'
    
    if not allowed_file(file.filename):
        return False, f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
    
    if not validate_file_size(file):
        return False, f'File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB'
    
    try:
        # Secure and generate unique filename
        original_name = secure_filename(file.filename)
        filename = generate_unique_filename(original_name)
        
        # Create upload directory if not exists
        upload_dir = os.path.join(current_app.static_folder, 'uploads', subfolder)
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, filename)
        
        # Save file
        file.save(filepath)
        
        # Process image with Pillow (optimize)
        try:
            img = Image.open(filepath)
            
            # Auto-orient based on EXIF data
            if hasattr(img, '_getexif') and img._getexif():
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)
            
            # Resize if too large (max 1920px width)
            max_width = 1920
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
            
            # Save optimized
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(filepath, quality=85, optimize=True)
            
        except Exception as e:
            print(f"Image processing warning: {e}")
            # File is already saved, just skip optimization
        
        return True, f'uploads/{subfolder}/{filename}'
        
    except Exception as e:
        return False, f'Error saving file: {str(e)}'


def create_thumbnail(filepath, size=(300, 300)):
    """Create a thumbnail version of an image"""
    try:
        img = Image.open(os.path.join(current_app.static_folder, filepath))
        img.thumbnail(size, Image.LANCZOS)
        
        # Generate thumbnail path
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        thumb_filename = f"thumb_{filename}"
        thumb_path = os.path.join(current_app.static_folder, directory, thumb_filename)
        
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(thumb_path, quality=80, optimize=True)
        
        return f"{directory}/{thumb_filename}"
    except Exception as e:
        print(f"Thumbnail creation error: {e}")
        return None


def delete_uploaded_image(filepath):
    """Delete an uploaded image file"""
    try:
        full_path = os.path.join(current_app.static_folder, filepath)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception as e:
        print(f"Error deleting file: {e}")
    return False
