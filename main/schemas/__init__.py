from marshmallow import ValidationError


def validate_white_spaces(string):
    if len(string.strip()) == 0:
        raise ValidationError('String must not be empty')
