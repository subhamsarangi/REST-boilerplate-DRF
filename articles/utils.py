import uuid


def get_image_upload_path(_, filename):
    old_filename, ext = filename.split('.')
    new_filename = f"{old_filename}-{uuid.uuid4()}.{ext}"
    return f"heroimages/{new_filename}"