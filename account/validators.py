from django.core.exceptions import ValidationError
import os

def image_validator(value):
    valid_extensions = ['.jpg', '.png', '.jpeg']
    extension = os.path.splitext(value.name)[1] # test.jpg
    if not extension.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions: '+ str(valid_extensions))