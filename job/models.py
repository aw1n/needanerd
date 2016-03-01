#from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.datastructures import MultiValueDictKeyError

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

'This class is used to serialize a JSON response back to the user through the search REST functions'
class JobSearch(models.Model):
    jobpk=models.CharField(max_length=32)
    studentpk=models.CharField(max_length=32, blank=True)
    name=models.CharField(max_length=32)
    applied=models.BooleanField()
    employer=models.CharField(max_length=32)
    employerpk=models.CharField(max_length=32)
    salary=models.CharField(max_length=32)
    updated_at=models.CharField(max_length=32)

class Job(models.Model):
    
    #studentwatch=models.ManyToManyField('student.Student', blank=True)
    applicant=models.ManyToManyField('student.Student', blank=True)
    employer=models.ForeignKey('employer.Employer')
    name=models.CharField(max_length=32)
    description=models.CharField(max_length=3200)
    skills=models.CharField(max_length=1000)
    startdate = models.CharField(max_length=16)
    enddate = models.CharField(max_length=16)
    salary=models.CharField(max_length=16)
    released = models.BooleanField(null=False, blank=False, default=True)
    #Used on first create
    created_at = models.DateTimeField(auto_now_add = True)
    #Auto add everytime the object is resaved
    updated_at = models.DateTimeField(auto_now = True)

admin.site.register(Job)

class JobForm(forms.ModelForm):

    name = forms.CharField(label="*Position", max_length=32, widget=forms.TextInput(attrs={'placeholder':''}))
    description = forms.CharField(label="*Description", widget=forms.widgets.Textarea(attrs={'rows':16, 'cols':100, 'placeholder':''}))
    skills = forms.CharField(label="*Skills", widget=forms.widgets.Textarea(attrs={'rows':4, 'cols':50, 'placeholder':''}))
    salary = forms.CharField(label="Salary Information", max_length=16, required=False,widget=forms.TextInput(attrs={'placeholder':''}))
    released = forms.BooleanField(label = "Release for Viewing",widget=forms.CheckboxInput(),initial=True,required=False)    
        
    class Meta:
        model = Job
        exclude = ("applicant","employer","startdate","enddate")
        
    def save(self, employerpk):
        
        logger.debug('Saving a new job')
        logger.debug('employerpk='+str(employerpk))
        logger.debug('self.instance.pk='+str(self.instance.pk))
        if self.instance.pk:
            job=Job.objects.get(pk=self.instance.pk)
        else:
            job = Job()
            
        job.name=self.cleaned_data['name']
        job.description=self.cleaned_data['description']
        job.skills=self.cleaned_data['skills']
        
        job.startdate=self.data['startdate']
        logger.debug('job.startdate='+job.startdate)
        
        try:
            permposition=self.data['permposition']
            job.enddate=""
            logger.debug('Permenant position job.enddate='+job.enddate)
        except MultiValueDictKeyError:
            job.enddate=self.data['enddate']
            logger.debug('job.enddate='+job.enddate)
                
        job.salary=self.cleaned_data['salary']
        job.released=self.cleaned_data['released']
        user=User.objects.get(pk=employerpk)
        job.employer = user.userprofile.employer
        logger.debug('Adding job to employer, company name = '+user.userprofile.employer.company_name)
        job.save()
        
        return job