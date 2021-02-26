from django.db import models

# Create your models here.
from django.conf import settings
from services.models import *
import os
from common.verifiers import create_attachment_id, create_file_name
def submission_file_name(instance, filename):
    import os.path
    from django.conf import settings
    i = 1
    random_file_name = create_file_name()
    file_path = '{owner}/'.format(owner=instance.refrence_attachment.owner.pk) 
    #here instance.user.pk is uysed rather then reverse lookup for related user becuase this file is created before assinging the verificationDocument object to user's document thus no results will be found in reverse lookup    
    orignal_name = instance.refrence_attachment.orignal_filename.split(".")[0]+"_{}".format(str(instance.target_language.language_name))+"_{}".format("Proofreaded")
    extention = instance.refrence_attachment.orignal_filename.split(".")[-1]
    exist = os.path.isfile(settings.MEDIA_ROOT+'/'+orignal_name +'_'+ random_file_name+"."+extention)
    new_path = file_path+'/'+orignal_name+'_'+random_file_name+"."+extention
    while exist:   
            new_path = ''
            new_path += file_path+'/'+orignal_name+'_'+random_file_name+'_'+str(i)+"."+extention
            i += 1
            exist = os.path.isfile(settings.MEDIA_ROOT+'/'+new_path)
    return new_path 

class Submissions(models.Model):
    refrence_attachment = models.ForeignKey("common.Attachment", on_delete=models.CASCADE)
    target_language = models.ForeignKey('common.Language', on_delete=models.PROTECT, blank=True, null=True)

    submited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    submission_file = models.FileField(upload_to = submission_file_name, blank=True, null=True)
    submission_filename = models.CharField(max_length=260) #Defalut windows file name length
    submit_date =  models.DateTimeField(auto_now_add = False, verbose_name="Submission date", blank=True, null=True)
    
    final =  models.BooleanField(default=False)
    proofreading_contract =  models.BooleanField(default=False)
    submission_dependency = models.ForeignKey("employee.Submissions", on_delete=models.CASCADE, blank=True, null=True)


    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    @property
    def is_submitted(self):
        print(bool(self.submission_file))
        if bool(self.submission_file):
            return True
        else:
            return False

    def filename(self):
        return os.path.basename(self.submission_file.name)

    # TO STRING METHOD
    def __str__(self):
        return self.refrence_attachment.orignal_filename

class Notifications(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    creation_date =  models.DateTimeField(auto_now_add = False, verbose_name="Submission date", blank=True, null=True)
    link = models.CharField(max_length=300) #Defalut windows file name length
    text = models.CharField(max_length=100) #Defalut windows file name length
    read = models.BooleanField(default=False)