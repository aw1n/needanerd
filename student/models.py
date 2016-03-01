#from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib import admin
from resume.models import Resume
from needanerd import studentgroupname

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

class Student(models.Model):
    
    userprofile=models.OneToOneField('appsecurity.UserProfile',primary_key=True)
    currentmajor=models.CharField(max_length=32)

admin.site.register(Student)

'''This class is used to serialize a JSON response back to the user through the search REST functions'''
class StudentSearch(models.Model):
    studentid=models.IntegerField()
    first_name=models.CharField(max_length=32)
    last_name=models.CharField(max_length=32)
    currentmajor=models.CharField(max_length=32)
    objective=models.TextField(blank=True)
    
class StudentUserCreationForm(forms.ModelForm):
    
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_email': _("This email is already registered to an account, either retrieve your password or use a new email"),
        'password_mismatch': _("The two password fields didn't match."),
    }
    
    email = forms.EmailField(label = "Email", max_length=32)
    first_name = forms.CharField(label = "First name", max_length=16)
    last_name = forms.CharField(label = "Last name", max_length=32)
    currentmajor = forms.CharField(label = "Current Academic Major", max_length=32)
    ''' 
    username = forms.RegexField(label=_("Username"), max_length=32,
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})'''
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email","currentmajor",)
    '''
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
    '''
    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User.objects.get(username=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self):
        user = super(StudentUserCreationForm, self).save(commit=False)
        user.is_active=False
        user.set_password(self.cleaned_data["password1"])
        user.username=(self.cleaned_data["email"])
        
        'We have to save here so the userprofile is created'
        user.save()
        logger.debug('Saving user with username: '+user.username)
        
        newStudent=Student(currentmajor=self.cleaned_data["currentmajor"])
        newStudent.userprofile=user.userprofile
        newStudent.save()
        
        'Create a default resume'
        Resume.objects.create(student=newStudent)
        
        user.userprofile.student=newStudent
        user.userprofile.save()
        studentgroup = Group.objects.get_or_create(name=studentgroupname)
        user.groups.add(studentgroup[0])

        user.save()
        return user
    
class StudentUserEditForm(forms.ModelForm):
    
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")
    currentmajor = forms.CharField(label = "Current Academic Major")
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email","currentmajor",)

    def save(self):
        
        logger.debug('Saving student')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        student=Student.objects.get(pk=self.instance.userprofile.student.pk)
        user=User.objects.get(pk=self.instance.pk)
        
        student.currentmajor=self.cleaned_data["currentmajor"]
        student.save()
        user.first_name=self.cleaned_data["first_name"]
        user.last_name=self.cleaned_data["last_name"]
        user.username=(self.cleaned_data["email"])
        user.email=self.cleaned_data["email"]
        user.save()
        return user
