from django.core.exceptions import ValidationError
import re
from django.utils import timezone


# Only letters (A-Z, a-z, space)
def only_letters(value):
    if value:
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise ValidationError(
                f"'{value}' contains invalid characters. Only letters and spaces are allowed."
            )
    return value


# Mobile number must be exactly 10 digits
def mobile_10_digits(value):
    if value:
        if not re.match(r'^\d{10}$', value):
            raise ValidationError(
                f"'{value}' is not a valid 10-digit mobile number."
            )
    return value



# validators for tickets 

def validate_future_date_not_allowed(value):
    if value > timezone.now().date:
        raise ValidationError("Date cannot be in the future")
    

def resolution_after_call(call_time,resolution_time):
    if call_time and resolution_time:
        if resolution_time < call_time:
            raise ValidationError(
                "Resolution time can not be earlier than call time."
            )
        