from django.db import models
from core.models import TimestampedModel
import uuid

# Create your models here.

from django.conf import settings
import os.path
from common.verifiers import create_attachment_id, create_file_name
def image_file_name(instance, filename):
    i = 1
    random_file_name = create_file_name()
    file_path = 'staff/{owner}/'.format(owner=instance.user.pk) 
    #here instance.user.pk is uysed rather then reverse lookup for related user becuase this file is created before assinging the verificationDocument object to user's document thus no results will be found in reverse lookup    
    extention = ".png"
    new_path = ''
    new_path += file_path+'/'+random_file_name+"."+extention
    exist = os.path.isfile(settings.MEDIA_ROOT+'/'+new_path)

    while exist:   
            new_path = ''
            new_path += file_path+'/'+random_file_name+'_'+str(i)+"."+extention
            i += 1
            exist = os.path.isfile(settings.MEDIA_ROOT+'/'+new_path)

    return new_path 
from PIL import Image
from services.models import Contract

class Profile(TimestampedModel):
    TRANSLATOR = "TR"
    EDITOR = "ED"
    MANAGER = "MA"
    SECRETARY = "SE"
    ACCOUNTANT = "AC"
    INTERPRATOR = "IN"
    OTHER = "OT"

    TITLE_CHOICES = [
        (TRANSLATOR, "Translator"),
        (EDITOR, "Editor"),
        (MANAGER, "Manager"),
        (SECRETARY, "Secretary"),
        (ACCOUNTANT, "Accountant"),
        (INTERPRATOR, "Interpreter"),
        (OTHER, "Other"),
    ]
   
    user = models.OneToOneField("users.User", on_delete=models.PROTECT)
    title = models.CharField(max_length=2, choices=TITLE_CHOICES, default=TRANSLATOR,)  
    bio = models.TextField(blank=True)   
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    #overview = models.TextField(max_length=250, blank=True)
    image = models.ImageField(upload_to = image_file_name, default="base\placeholder.png")
    from_languages =  models.ManyToManyField('common.Language', related_name='profile_from_languages_relation', blank=True)
    to_languages =  models.ManyToManyField('common.Language', related_name='profile_to_language_relation', blank=True)
    content_types = models.ManyToManyField('common.Content', related_name='profile_to_language_relation', blank=True)
    #uid = models.UUIDField(unique=True, editable=False,  default=uuid.uuid4, verbose_name='Public identifier',)

    def total_earning(self):
        total_earning = 0
        completed_contracts = Contract.objects.all().filter(profile=self.user, completed=True, paid=True)
        for contract in completed_contracts:
            total_earning += contract.contract_price
        return total_earning

    def due_earning(self):
        due_earning = 0
        completed_contracts = Contract.objects.all().filter(profile=self.user, completed=True, paid=False)
        for contract in completed_contracts:
            due_earning += contract.contract_price
        return due_earning

    def active_contracts(self):
        ongoing_projects = Contract.objects.all().filter(profile=self.user, completed=False).count()
        return ongoing_projects

    def completed_contracts(self):
        completed_contracts = Contract.objects.all().filter(profile=self.user, completed=True).count()
        return completed_contracts
        

    def title_verbose(self):
        return dict(Profile.TITLE_CHOICES)[self.title]    

    def __str__(self):
        return self.user.email

    @property
    def get_full_name(self):
        return self.first_name+" "+self.last_name

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.image.path)
    #TODO  property or something to return the skills a profile have 
    #TODO  property or something to return the earning (total value) a profile earned
    #TODO  

'''
## Skill model was copied from Employee app since we don't need it anymore      
class Skill(models.Model):
    profile = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    language = models.ForeignKey("common.Language", on_delete=models.CASCADE)
    # TODO  skill level here is required, some sort of Intermidiate, Professional and Expert. Think about this

    class Meta:
        verbose_name = "skill"
        verbose_name_plural = "skills"

    # TO STRING METHOD
    def __str__(self):
        return self.profile.first_name
'''