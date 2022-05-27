from django.db import models
from django.utils import timezone

import random
import re
# Create your models here.


def translation_default(arg1,arg2):
    return arg1 + " - " + arg2

def group_default(arg=None):
    if arg==None:
        return 'NA'
    return arg

class English(models.Model):
    value = models.CharField(max_length=100,unique=True)
    creation_date = models.DateTimeField('Date',auto_now=True)
    @classmethod
    def create(cls,name):
        self.value = name
    def __str__(self):
        return self.value 

class Dutch(models.Model):
    value = models.CharField(max_length=100,unique=True)
    creation_date = models.DateTimeField('Date',auto_now=True)
    @classmethod
    def create(cls,name):
        self.value = name
    def __str__(self):
        return self.value 

class TranslationGroup(models.Model):
    groupName = models.CharField(max_length=50,unique=True)
    created = models.DateField('Date',auto_now_add=True)
    def name(self):
        return re.sub(r'_',' ',self.groupName.capitalize())
    def __str__(self):
        return re.sub(r'_',' ',self.groupName.capitalize())


class Translation(models.Model):
    english = models.ForeignKey(English,
            on_delete=models.RESTRICT,
            )
    dutch = models.ForeignKey(Dutch,
            on_delete=models.RESTRICT,
            )
    translation_key = models.CharField(max_length=203,unique=True,
            default=translation_default(english.__str__(),dutch.__str__()))
    creation_date = models.DateField('Date',auto_now_add=True)
    translation_group = models.ManyToManyField(TranslationGroup,
#            on_delete=models.RESTRICT,
            )
    def __str__(self):
        return "English: " + self.english.__str__() + " --- " + "Dutch: " + self.dutch.__str__() + "\n"
    def choose(self):
        if random.randint(0,1) > 0:
            return self.english.value
        return self.dutch.value
