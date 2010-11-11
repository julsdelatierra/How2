 # -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='get_common_data')
    image = models.ImageField(upload_to='avatars/', null=True)
    birthday = models.DateField(null=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=100, null=True)
    interest = models.TextField(null=True)
    code = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user.username

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    template = models.TextField()
    is_active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Language(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class How2(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(Category, limit_choices_to={'is_active':True})
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User)
    rating = models.IntegerField(default=0, max_length=1)
    language = models.ForeignKey(Language)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
    def __unicode__(self):
        return self.title

class Suggestion(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    how2 = models.ForeignKey(How2)
    author = models.ForeignKey(User)
    suggestion = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
    def __unicode__(self):
        return self.howto.author.username

class Selected(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    how2 = models.ForeignKey(How2)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
    def __unicode__(self):
        return self.howto.title

class How2Contribution(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    mode = models.BooleanField()
    asker = models.ForeignKey(User, related_name='asker_how2')
    asked = models.ForeignKey(User, related_name='asked_how2', null=True)
    
    def __unicode__(self):
        return self.title

class UserMenu(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(unique=True, max_length=30)
    link = models.CharField(max_length=30)
    tooltip = models.TextField(null=True)
    to = models.BooleanField(help_text='0=anyone,1=registered')
    
    def __unicode__(self):
        return self.text

class Reading(models.Model):
    id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(User, related_name='reader')
    writer = models.ForeignKey(User, related_name='writers')
    
    def __unicode__(self):
        return self.reader.username
    
class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    voter = models.ForeignKey(User)
    how2 = models.ForeignKey(How2)
 
class Translation(models.Model):
    id = models.AutoField(primary_key=True)
    orig = models.ForeignKey(How2)
    title = models.CharField(max_length=200)
    content = models.TextField()
    lang = models.ForeignKey(Language)
    
    def __unicode__(self):
        return self.title