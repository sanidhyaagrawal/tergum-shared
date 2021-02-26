#import secrets
from os import urandom

def create_job_id():
    '''
    create unique and cryptographically strong random id for a job
    '''
    job_id = urandom(5).hex()
    #secrets.randbits(32) #numbers only
    is_taken, job_obj = job_id_is_valid(job_id)
    while is_taken:
        job_id = urandom(5).hex()
        #secrets.randbits(32) #numbers only 
        is_taken, job_obj = job_id_is_valid(job_id)
    return job_id


def job_id_is_valid(job_id):
    from services.models import Job

    '''
    check if a job_obj exists realted to given job_id
    '''
    try:
            job_obj = Job.objects.get(job_id=job_id)
            return (True, job_obj)
    except:
            return (False, None)    

def create_contract_id():
    '''
    create unique and cryptographically strong random id for a contract
    '''
    contract_id = urandom(5).hex()
    #secrets.randbits(32) #numbers only
    is_taken, contract_obj = contract_id_is_valid(contract_id)
    while is_taken:
        contract_id = urandom(5).hex()
        #secrets.randbits(32) #numbers only 
        is_taken, contract_obj = contract_id_is_valid(contract_id)
    return contract_id

def contract_id_is_valid(contract_id):
    from services.models import Contract
    '''
    check if a contract_obj exists realted to given contract_id
    '''
    try:
            contract_obj = Contract.objects.get(contract_id=contract_id)
            return (True, contract_obj)
    except:
            return (False, None)    
            
def create_file_name(lines_in_text_input):  
    '''
    create a file name based on provided text
    '''     
    for line in lines_in_text_input:
        #TODO replce this monstrosity with regex expression
        line= line.strip().replace(">", "").replace("<", "").replace('"', "").replace("/", "").replace("|", "").replace("{}".format("/"), "").replace("]", "")
        line= line.replace(":", "").replace(":", "").replace(".", "").replace(" ", "_").replace("?", "").replace("*", "").replace(" ", "").replace("[", "")
        if len(line) > 7:
            input_text_file_name = "{}{}".format(str(line[:7]), ".txt")
            break
        else:
            input_text_file_name = "{}{}".format(str(line), ".txt")
            break    
        

    return input_text_file_name
