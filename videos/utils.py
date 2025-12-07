import hashlib

def compute_sha256_of_uploaded_file(uploaded_file, chunk_size=8192):
    """
    Calculate a SHA-256 hash for an uploaded file.
    This helps detect duplicate video uploads.
    """

    # Create a SHA-256 hash object
    file_hash = hashlib.sha256()

    # Read the uploaded file in small chunks (not all at once)
    # This prevents memory issues with large files
    for chunk in uploaded_file.chunks(chunk_size):
        file_hash.update(chunk)  # Add chunk data to the hash

    # Reset file pointer back to the beginning
    # so Django can save the file normally later
    try:
        uploaded_file.seek(0)
    except Exception:
        try:
            uploaded_file.file.seek(0)
        except Exception:
            pass  # If it fails, ignore — saving may still work

    # Return the final hash value as a 64-character hex string
    return file_hash.hexdigest()
