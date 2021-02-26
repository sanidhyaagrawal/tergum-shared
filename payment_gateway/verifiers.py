#import secrets
from os import urandom

from .models import payment_tokens

def create_payment_token(job_obj):
    '''
    create unique and cryptographically strong payment_token, this does not
    need to be unique as it is tempory and works in pair with job_obj.
    '''
    payment_token = urandom(10).hex()
    #secrets.token_urlsafe(10)
    payment_tokens.objects.create(payment_token=payment_token, job=job_obj)
    return payment_token

def payment_token_is_valid(payment_token, job_obj):
    '''
    check if a payment_token exists realted to given job_obj, 
    delete it if it exits so it can't be used again and return True.
    '''
    payment_token_obj = payment_tokens.objects.all().filter(payment_token = payment_token, job=job_obj)
    print(payment_token_obj)
    if len(payment_token_obj) != 0:
        payment_token_obj.delete()
        return True
    else:
        return False    