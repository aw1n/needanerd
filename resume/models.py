from django.db import models
#from django import forms
from django.contrib import admin

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

class Resume(models.Model):
    student=models.ForeignKey('student.Student')
    objective=models.TextField(blank=True)

admin.site.register(Resume)

class Degree(models.Model):
    resume=models.ForeignKey('resume.Resume')
    degreetype=models.CharField(max_length=32, blank=True)
    major=models.CharField(max_length=32, blank=True)
    university=models.CharField(max_length=32, blank=False)
    '''Not using DateField because it expects a certain format which is only overridden with widgets (forms) which we are not using'''
    date=models.CharField(max_length=16, blank=True,null=True)
    gpa=models.CharField(max_length=8,blank=True)
    honors=models.CharField(max_length=16,blank=True)

admin.site.register(Degree)

class Skill(models.Model):
    resume=models.ForeignKey('resume.Resume')
    skill=models.CharField(max_length=32)

admin.site.register(Skill)

class Certification(models.Model):
    resume=models.ForeignKey('resume.Resume')
    name=models.CharField(max_length=32)
    authority=models.CharField(max_length=32, blank=True)
    licnumber=models.CharField(max_length=32, blank=True)
    url=models.CharField(max_length=128, blank=True)
    expdate=models.CharField(max_length=16, blank=True,null=True)
    neverexp=models.BooleanField(blank=True)
    
admin.site.register(Certification)

class Employment(models.Model):
    resume=models.ForeignKey('resume.Resume')
    company=models.CharField(max_length=64)
    title=models.CharField(max_length=64)
    startdate=models.CharField(max_length=16, blank=True,null=True)
    enddate=models.CharField(max_length=16, blank=True,null=True)
    jobfunctions=models.TextField(max_length=256)

admin.site.register(Employment)
'''
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('student',)
    
    objective = forms.CharField(required=False, label="Objective", widget=forms.widgets.Textarea(attrs={'rows':15, 'cols':100}))

class ResumeEditForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ("objective",)
    
    objective = forms.CharField(required=False, label="Objective", widget=forms.widgets.Textarea(attrs={'rows':15, 'cols':100}))

    def save(self):
        
        logger.debug('Saving Resume')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        
        resume=Resume.objects.get(pk=self.instance.pk)
        resume.body=self.cleaned_data["body"]
        resume.save()
        
        return resume

class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ("resume",)
 
class DegreeForm(forms.ModelForm):
    
    date = forms.DateField(label = "Date: (Format: DD/MM/YYYY)")
    degreetype = forms.CharField(label = "Type (i.e. B.S., B.A.)", max_length=32)
    gpa = forms.CharField(label = "G.P.A.", max_length=32)
    honors = forms.CharField(label = "Honors", max_length=32)
    
    class Meta:
        model = Degree
        exclude = ("resume",)
        
    def save(self, r):
        
        logger.debug('Saving Degree')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        degree=Degree(resume=r)
        degree.degreetype=self.cleaned_data["degreetype"]
        degree.major=self.cleaned_data["major"]
        degree.university=self.cleaned_data["university"]
        degree.date=self.cleaned_data["date"]
        degree.gpa=self.cleaned_data["gpa"]
        degree.honors=self.cleaned_data["honors"]
        degree.save()
        return degree
    
class DegreeEditForm(forms.ModelForm):
    
    date = forms.DateField(label = "Date: (Format: DD/MM/YYYY)")
    degreetype = forms.CharField(label = "Type (i.e. B.S., B.A.)", max_length=32)
    gpa = forms.CharField(label = "G.P.A.", max_length=32)
    honors = forms.CharField(label = "Honors", max_length=32)
    
    class Meta:
        model = Degree
        exclude = ("resume",)
    
    def save(self):
        
        logger.debug('Saving Degree')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        degree=Degree.objects.get(pk=self.instance.pk)
        degree.degreetype=self.cleaned_data["degreetype"]
        degree.major=self.cleaned_data["major"]
        degree.university=self.cleaned_data["university"]
        degree.date=self.cleaned_data["date"]
        degree.gpa=self.cleaned_data["gpa"]
        degree.honors=self.cleaned_data["honors"]
        degree.save()
        return degree

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ("resume",)
        
class SkillEditForm(forms.ModelForm):
    class Meta:
        model = Degree
        exclude = ("resume",)
        
    def save(self):
        
        logger.debug('Saving Degree')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        skill=Degree.objects.get(pk=self.instance.pk)
        skill.skill=self.cleaned_data["skill"]
        skill.save()
        return skill
    
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        exclude = ("resume",)
        expdate = forms.DateField(input_formats='%m/%Y') #Only care about month and year
        
class CertificationEditForm(forms.ModelForm):
    class Meta:
        model = Certification
        exclude = ("resume",)
        expdate = forms.DateField(input_formats='%m/%Y') #Only care about month and year
        
    def save(self):
        
        logger.debug('Saving Degree')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        certification=Degree.objects.get(pk=self.instance.pk)
        certification.certification=self.cleaned_data["certification"]
        certification.vendor=self.cleaned_data["vendor"]
        certification.save()
        return certification

class EmploymentForm(forms.ModelForm):
    
    class Meta:
        model = Employment
        exclude = ("resume",)
        startdate = forms.DateField(input_formats='%m/%Y') #Only care about month and year
        enddate = forms.DateField(input_formats='%m/%Y') #Only care about month and year

    def save(self, resumepk):
        
            if self.instance.pk:
                employment=Employment.objects.get(pk=self.instance.pk)
            else:
                employment = Employment()
                
            employment.r=Resume.objects.get(pk=resumepk)
            employment.company=self.cleaned_data['company']
            employment.title=self.cleaned_data['title']
            employment.startdate=self.cleaned_data['startdate']
            employment.enddate=self.cleaned_data['enddate']
            employment.jobfunctions=self.cleaned_data['jobfunctions']
            employment.save()

class EmploymentEditForm(forms.ModelForm):
    
    class Meta:
        model = Employment
        exclude = ("resume",)
        startdate = forms.DateField(input_formats='%m/%Y') #Only care about month and year
        enddate = forms.DateField(input_formats='%m/%Y') #Only care about month and year

    def save(self, resumepk):
        
            if self.instance.pk:
                employment=Employment.objects.get(pk=self.instance.pk)
            else:
                employment = Employment()
                
            employment.r=Resume.objects.get(pk=resumepk)
            employment.company=self.cleaned_data['company']
            employment.title=self.cleaned_data['title']
            employment.startdate=self.cleaned_data['startdate']
            employment.enddate=self.cleaned_data['enddate']
            employment.jobfunctions=self.cleaned_data['jobfunctions']
            employment.save()
'''