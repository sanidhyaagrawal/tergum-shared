from django.db import models
from django.conf import settings
from services.models import *

#Content of attachments in the job, ex- Generic content, Legal
class Content(models.Model):
    content_name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=250,null=True,verbose_name="short description of what the content is about")

    class Meta:
        verbose_name = "content"
        verbose_name_plural = "contents"

    # TO STRING METHOD
    def __str__(self):
        return self.content_name


# class Status(models.Model):
#     status_name = models.CharField(max_length=50)
#     progress = models.DecimalField(max_digits=5, decimal_places=2)

#     class Meta:
#         verbose_name = "status"
#         verbose_name_plural = "status"

#     # TO STRING METHOD
#     def __str__(self):
#         return self.status_name
#  #TODO now this is part of job itself so no need may be


class JobType(models.Model):
    job_type = models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name = "job type"
        verbose_name_plural = "job types"

    # TO STRING METHOD
    def __str__(self):
        return self.job_type

class Status(models.Model):
    OPEN = 'OP'
    PROGRESSING = 'PR'
    TRANSLATING = 'TR'
    PROOFREADING = 'PF'
    PENDING = 'PN'
    DONE = 'DN'    

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (PROGRESSING, 'Progressing'),
        (TRANSLATING, 'Translating'),
        (PROOFREADING, 'Proofreading'),
        (PENDING,'Pending'),
        (DONE, 'Done'),
       ]
    status_name =   models.CharField(max_length=2,
        choices=STATUS_CHOICES,
        default=PENDING,    )
    comment = models.TextField(max_length=250, null=True)
    entry_date = models.DateField(auto_now_add=True,verbose_name="date of record entry")
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "status"

    # TO STRING METHOD
    def __str__(self):
        return self.status_name

from django.core.exceptions import ValidationError
class Variables(models.Model):
    base_price = models.FloatField() #defaut price
    company_share = models.IntegerField() #30% of the total price paid by the employeer
    translator_share = models.IntegerField() #70% of the amount remaing after company_share
    proofreader_share = models.IntegerField() #30% of the amount remaing after company_share
    #content_expert_bonus = models.IntegerField() #10% subtracted from proofreader_share and added to translator_share
    def clean(self):
        if self.translator_share + self.proofreader_share != 100:
            raise ValidationError("translator_share and proofreader_share does not add up to make 100%")
        #elif self.content_expert_bonus > self.proofreader_share:
        #    raise ValidationError("content_expert_bonus is deducted from proofreader_share thus it can't be grater then proofreader_share itself.")

from itertools import permutations  
class Language(models.Model):
    language_name = models.CharField(unique=True, max_length=50)
    is_local = models.BooleanField()

    class Meta:
        verbose_name = "language"
        verbose_name_plural = "languages"

    def save(self, *args, **kwargs):
        #We automaticlly create "Rates" for all the possible combinations of
        #languages and job_types using defalut base price which can be edited 
        # from admin pannel. 
        all_languages = Language.objects.all()
        all_job_types = JobType.objects.all()
        perm = permutations(all_languages, 2)  
        base_price = Variables.objects.last().base_price
        for job_type in all_job_types:
            for langs in list(perm):   
                if Rate.objects.all().filter(source_language= langs[0], target_language=langs[1], job_type=job_type).exists():
                    pass
                else:
                    Rate.objects.create(source_language= langs[0], target_language= langs[1], base_rate=base_price, job_type=job_type)     
        super(Language, self).save(*args, **kwargs)
 
    # TO STRING METHOD
    def __str__(self):
        return self.language_name


class Quality(models.Model):
    quality_name = models.CharField(max_length=50)
    rate_multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    proofreading = models.BooleanField(default=False)
    class Meta:
        verbose_name = "quality"
        verbose_name_plural = "qualities"

    # TO STRING METHOD
    def __str__(self):
        return self.quality_name


class Rate(models.Model):
    source_language = models.ForeignKey(
        Language, related_name="source", on_delete=models.CASCADE,
    )
    target_language = models.ForeignKey(
        Language, related_name="target", on_delete=models.CASCADE,
    )
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE,)
    base_rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "rate"
        verbose_name_plural = "rates"

    # TO STRING METHOD
    def __str__(self):
        return "{} | {} --> {}, {}/word".format(self.job_type, self.source_language, self.target_language, self.base_rate)

#Q Think if having Attachment table is necessary or attachment should be part of the job?
#A As the Attachments most needed with the Job, Having the Job have a 
#ManyToMany relation with aatchments will be more efficent otherwise we'll have to 
#reverse look-up evertime to get a Job's attachments.


from common.verifiers import create_attachment_id, create_file_name
def content_file_name(instance, filename):
    import os.path
    from django.conf import settings
    i = 1
    random_file_name = create_file_name()
    file_path = '{owner}/'.format(owner=instance.owner.pk) 
    #here instance.user.pk is uysed rather then reverse lookup for related user becuase this file is created before assinging the verificationDocument object to user's document thus no results will be found in reverse lookup    
    orignal_name = instance.orignal_filename.split(".")[0]
    extention = instance.orignal_filename.split(".")[-1]
    exist = os.path.isfile(settings.MEDIA_ROOT+'/'+orignal_name +'_'+ random_file_name+"."+extention)
    new_path = file_path+'/'+orignal_name+'_'+random_file_name+"."+extention
    while exist:   
            new_path = ''
            new_path += file_path+'/'+orignal_name+'_'+random_file_name+'_'+str(i)+"."+extention

            
            i += 1
            exist = os.path.isfile(settings.MEDIA_ROOT+'/'+new_path)

    return new_path 

class Attachment(models.Model):
    attachment_id = models.CharField(max_length=25,unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    file = models.FileField(upload_to = content_file_name, blank=False, null=False)
    orignal_filename = models.CharField(max_length=260) #Defalut windows file name length
    word_count = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    class Meta:
        verbose_name = "attachment"
        verbose_name_plural = "attachments"

    # TO STRING METHOD
    def __str__(self):
        return self.orignal_filename

    def save(self, *args, **kwargs):
        #Attachment price is not being calculated here 
        #because admin might chnage prices after the job 
        #was created but the payment was already recived
        #thus it is being calculated in the apis.py
        self.attachment_id = create_attachment_id() 
        super(Attachment, self).save(*args, **kwargs)
 