from marshmallow import ValidationError


def validate_empty_string(string):
    if len(string.strip()) == 0:
        raise ValidationError('String must not be empty')