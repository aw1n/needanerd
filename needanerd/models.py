#from django.db import models
from django import forms

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

SUBJECT_CHOICES = ('general', 'suggestions', 'websites')

class ContactForm(forms.Form):
    first = forms.CharField(max_length=32,required=True,label="First Name")
    last = forms.CharField(max_length=32,required=True,label="Last Name")
    email = forms.EmailField(max_length=32,required=True,label="Email Address")
    subject = forms.CharField(max_length=32,required=True,label="Subject")
    message = forms.CharField(required=True,widget=forms.widgets.Textarea(),label="Message")
    
class ContactUserForm(forms.Form):
    message = forms.CharField(required=True,widget=forms.widgets.Textarea(attrs={'rows':100, 'cols':50}))
    cc_myself = forms.BooleanField(required=False)
    
'''
sclass StudentReview(models.Model):
    
    CHOICES=[(i+1,i+1) for i in range(5)]
    rating = models.IntegerField(choices=CHOICES)
    comments = models.CharField(max_length=128)
    student = models.ForeignKey('student.Student', blank=False)
    employer = models.ForeignKey('employer.Employer', blank=False)
    created_at = models.DateTimeField(auto_now_add = True)
    
class StudentReviewForm(forms.ModelForm):

    CHOICES=[(i+1, str(i+1)+ " Star(s)") for i in range(5)]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.Select())
    comments = forms.CharField(label = "Comments", widget=forms.widgets.Textarea(attrs={'rows':3, 'cols':40}), help_text = _("Details about the Student"))
    
    class Meta:
        model = StudentReview
        exclude = ("student","employer",)
        
class EmployerReview(models.Model):
    
    CHOICES=[(i+1,i+1) for i in range(5)]
    rating = models.IntegerField(choices=CHOICES)
    comments = models.CharField(max_length=128)
    student = models.ForeignKey('student.Student', blank=False)
    employer = models.ForeignKey('employer.Employer', blank=False)
    created_at = models.DateTimeField(auto_now_add = True)
    
class EmployerReviewForm(forms.ModelForm):

    CHOICES=[(i+1, str(i+1)+ " Star(s)") for i in range(5)]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.Select())
    comments = forms.CharField(label = "Comments", widget=forms.widgets.Textarea(attrs={'rows':3, 'cols':40}), help_text = _("Details about the Employer"))
    
    class Meta:
        model = StudentReview
        exclude = ("student","employer",)
'''