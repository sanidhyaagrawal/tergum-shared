
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User

#Custom validators for feilds like email.

def validateEmail(email) :
    '''
    checks if an email is valid and is not alredy used some other account
    reutns boolen for isValid, and a message to be sent to user.
    ''' 
    if not User.objects.all().filter(email = email).exists(): #email not alredy used.
        try:
            validate_email( email )
            return (True, 'Valid and Available')
        except ValidationError:
            return (False,"Please enter a valid email")
    else:
        return (False,"The email address is on another account, use another email or login")

