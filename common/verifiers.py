#import secrets
from os import urandom

        
def create_attachment_id():
    '''
    create unique and cryptographically strong random id for an attachment
    '''
    attachment_id = urandom(10).hex()
    #secrets.token_urlsafe(64) #2848 bits 
    isTaken, attachment_obj = attachment_id_is_valid(attachment_id)
    while isTaken:
        attachment_id = urandom(10).hex()
        #secrets.token_urlsafe(64) #2848 bits 
        is_taken, attachment_obj = attachment_id_is_valid(attachment_id)
    return attachment_id


def attachment_id_is_valid(attachment_id):
    '''
    check if a attachment_obj exists realted to given attachment_id
    '''
    try:
            attachment_obj = Attachment.objects.get(attachment_id=attachment_id)
            return (True, attachment_obj)
    except:
            return (False, None)    

        
def create_file_name():
    return urandom(3).hex()
    #secrets.token_urlsafe(5) #2848 bits 
  