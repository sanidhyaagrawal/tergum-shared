from django.db import models
from django.conf import settings
from common.models import *
import datetime
import random
import uuid

from services.verifiers import create_contract_id
class Contract(models.Model):
    contract_id = models.CharField(max_length=25,unique=True)   
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    job = models.ForeignKey('services.Job', on_delete=models.CASCADE,)
    is_signed =  models.BooleanField(default=False)
    signing_date =  models.DateTimeField(auto_now_add = False,verbose_name="Contract signed date", blank=True, null=True)
    completion_date =  models.DateTimeField(auto_now_add = False,verbose_name="Contract completion date", blank=True, null=True)
    #file = models.FileField(upload_to = content_file_name, blank=False, null=False)
    submissions = models.ManyToManyField('employee.Submissions',related_name='contract_submissions')
    dependency = models.ForeignKey("services.Contract", on_delete=models.SET_NULL, blank=True, null=True)
    completed = models.BooleanField(default=False)
    target_language = models.ForeignKey('common.Language',related_name='contract_target_language', on_delete=models.PROTECT, blank=True, null=True)
    contract_price = models.FloatField() #contract_price
    paid = models.BooleanField(default=False)
    final =  models.BooleanField(default=False)
    rating = models.FloatField(blank=True, null=True)
    feedback = models.CharField(max_length=1000, blank=True, null=True)   

    TRANSLATING = 'TR'
    PROOFREADING = 'PF'
    INTERPRETATION = 'IN'
    TRANSCRIBING = 'TS'

    STATUS_CHOICES = [
        (TRANSLATING, 'Translation'),
        (PROOFREADING, 'Proofreading'),
        (INTERPRETATION, 'Interpretation'),
        (TRANSCRIBING, 'Transcribing'),
    ]

    status =   models.CharField(max_length=2,
        choices=STATUS_CHOICES,
        default=TRANSLATING,)

    def status_verbose(self):
        return dict(Contract.STATUS_CHOICES)[self.status]    
    class Meta:
        verbose_name = 'contract'
        verbose_name_plural = 'contracts'
    # TO STRING METHOD
    def __str__(self):
        return "Job: {} CID: {} {} {} {}".format(self.job.job_id, self.contract_id, self.contract_price, self.status, self.job.calculate_total_price )
   
    def completeds_submissions(self):
        all_submissions = self.submissions.all()
        print(all_submissions)
        #total = len(all_submissions)
        completed = 0
        for submission in self.submissions.all():
            #print(submission, submission.refrence_attachment)
            if bool(submission.submission_file):
                completed += 1
        return completed

    def completion_percentage(self):
        percent = (self.completeds_submissions()/self.total_submissions())*100
        return percent

    def total_submissions(self):
        all_submissions = self.submissions.all()
        total = len(all_submissions)
        return total 

    def all_submitted(self):
        if self.completeds_submissions() == self.total_submissions():
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if len(self.contract_id) == 0:
            self.contract_id = create_contract_id() 
        super(Contract, self).save(*args, **kwargs)
 
class Company(models.Model):
    company_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'
    # TO STRING METHOD
    def __str__(self):
        return self.company_name

class Message(models.Model):
    text = models.CharField(max_length=1000)  
    employee = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

from services.verifiers import create_job_id
class Job(models.Model):
    job_id = models.CharField(max_length=25,unique=True)  
    employeer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #TODO include company name as optional field in service
    # company_name = models.CharField(max_length=25,blank=True) 
    job_type  = models.ForeignKey('common.JobType', on_delete=models.CASCADE, blank=True, null=True)
    quality = models.ForeignKey('common.Quality', on_delete=models.CASCADE, blank=True, null=True)
    source_language = models.ForeignKey('common.Language', related_name='source_language', on_delete=models.CASCADE, blank=True, null=True)
    target_language =  models.ManyToManyField('common.Language',related_name='target_language')
    deadline =  models.DateField(auto_now_add=False, verbose_name="deadline for delivery", null=True, blank=True)
    posted_date =  models.DateTimeField(auto_now_add=True,verbose_name="job posted date")
    instruction = models.TextField(blank=True, null=True)
    content =  models.ForeignKey('common.Content', on_delete=models.CASCADE, blank=True, null=True)
    attachments = models.ManyToManyField('common.Attachment',related_name='job_attachments')
    accepted =  models.BooleanField(default=False) #draft --> pending
    paid =  models.BooleanField(default=False) #pending --> paid
    status = models.ForeignKey('common.Status', on_delete=models.CASCADE, null=True)
    chat = models.ManyToManyField('services.Message',related_name='chat_message', blank=True)
    class Meta:
        verbose_name = 'job'
        verbose_name_plural = 'jobs'
    # TO STRING METHOD
    def __str__(self):
        return self.job_id
    
   
    def completed_contracts(self):
        completed_contracts = Contract.objects.all().filter(job=self, completed=True).count()
        return completed_contracts

    def signed_contracts(self):
        signed_contracts = Contract.objects.all().filter(job=self, completed=False, is_signed=True).count()
        return signed_contracts
        
    def completion_percentage(self):
        percent = (self.completed_contracts()/self.total_submissions())*100
        return percent

    def total_contracts(self):
        total_contracts = Contract.objects.all().filter(job=self).count()
        return total_contracts 

    def all_submitted(self):
        if self.completed_contracts() == self.total_contracts():
            return True
        else:
            return False

    @property
    def targetLanguageToString(self):  
        '''
        get a comma separated string of all target languages.
        '''
        # initialize an empty string 
        string = ""  
        # traverse in the string   
        for ele in self.target_language.all():  
            string += ele.language_name + ", "   
        string = string[:-2]
        # return string   
        return string  

    @property
    def get_number_of_target_languages(self):
        return len(list(self.target_language.all()))        
      

    @property
    def calculate_total_price(self):
        '''
        sums the price of all the individual attachments       
        '''
        total = 0
        for attachment in self.attachments.all():
            if attachment.price != None:
                total += attachment.price
        return round(total, 2)
    
    def save(self, *args, **kwargs):
        if len(self.job_id) == 0:
            self.job_id = create_job_id() 
        super(Job, self).save(*args, **kwargs)
 