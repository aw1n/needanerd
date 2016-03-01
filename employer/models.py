#from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib import admin

from needanerd import employergroupname

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

class Employer(models.Model):
    
    userprofile=models.OneToOneField('appsecurity.UserProfile',primary_key=True)
    website=models.CharField(max_length=64,blank=True,null=True)
    description = models.TextField()
    company_name = models.CharField(blank=False, null=False, max_length=32)
    oncampus = models.BooleanField(null=False, blank=False, default=True)
    address1 = models.CharField(blank=True, max_length=32)
    address2 = models.CharField(blank=True, max_length=32)
    city = models.CharField(blank=True, max_length=16)
    state = models.CharField(blank=True, max_length=2)
    zipcode = models.CharField(blank=True, max_length=5)
    phone = models.CharField(blank=True, max_length=16)
    preferredstudents = models.ForeignKey('student.Student',blank=True,null=True)

admin.site.register(Employer)

class EmployerUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_email': _("This email is already registered to an account, either retrieve your password or use a new email"),
        'password_mismatch': _("The two password fields didn't match."),
        'address_invalid': _("Off campus employees must enter a valid address"),
    }
    
    email = forms.EmailField(label = "*Email")
    first_name = forms.CharField(label = "*First name")
    last_name = forms.CharField(label = "*Last name")
    company_name = forms.CharField(label = "*Company Name")
    website = forms.CharField(label = "Company Website",required=False)
    '''username = forms.RegexField(label=_("*Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})'''
    password1 = forms.CharField(label=_("*Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("*Password"),
        widget=forms.PasswordInput,
        help_text = _("Verification."))

    description = forms.CharField(label = "Description", widget=forms.widgets.Textarea(attrs={'rows':3, 'cols':40}), required=False)
    oncampus = forms.BooleanField(label = "On Campus Employer",widget=forms.CheckboxInput(),initial=True,required=False)    
    address1 = forms.CharField(label = "Address Line 1", help_text = _("Required for off campus employers"),required=False)
    address2 = forms.CharField(label = "Address Line 2",required=False)
    city = forms.CharField(label = "City",required=False)
    state = forms.CharField(label = "State", max_length=2, min_length=2, widget=forms.TextInput(attrs={'size':'2'}),required=False)
    zipcode = forms.CharField(label = "Zipcode", max_length=5, min_length=5, widget=forms.TextInput(attrs={'size':'5'}),required=False)
    phone = forms.CharField(label = "*Phone Number", max_length=16, min_length=10, widget=forms.TextInput(attrs={'size':'16'}))
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "company_name", "email", "password1","password2", "phone", "website","description","oncampus","address1","address2","city","state","zipcode",)
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

    def clean_address1(self):
        address1 = self.cleaned_data["address1"]
        oncampus = self.cleaned_data["oncampus"]
        if oncampus == False and (address1 is None or address1 == ''):
            raise forms.ValidationError(self.error_messages['address_invalid'])
        else:
            logger.debug('oncampus='+str(oncampus))
            logger.debug('address1='+address1)            
            return address1            
    
    def clean_city(self):
        city = self.cleaned_data["city"]
        oncampus = self.cleaned_data["oncampus"]
        if oncampus == False and (city is None or city == ''):
            raise forms.ValidationError(self.error_messages['address_invalid'])
        return city            
    
    def clean_state(self):
        state = self.cleaned_data["state"]
        oncampus = self.cleaned_data["oncampus"]
        if oncampus == False and (state is None or state == ''):
            raise forms.ValidationError(self.error_messages['address_invalid'])
        return state
    
    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        oncampus = self.cleaned_data["oncampus"]
        if oncampus == False and (zipcode is None or zipcode == ''):
            raise forms.ValidationError(self.error_messages['address_invalid'])
        return zipcode
        
    def save(self):
        
        logger.debug('Saving employer')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        if self.instance.pk:
            user=User.objects.get(pk=self.instance.pk)
        else:
            user = User()
        
        user.is_active=False
        user.first_name=self.cleaned_data["first_name"]
        user.last_name=self.cleaned_data["last_name"]
        user.username=(self.cleaned_data["email"])
        user.email=self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        user.save()
        
        site=self.cleaned_data["website"]
        description=self.cleaned_data["description"]
        company_name=self.cleaned_data["company_name"]
        oncampus=self.cleaned_data["oncampus"]
        address1=self.cleaned_data["address1"]
        address2=self.cleaned_data["address2"]
        city=self.cleaned_data["city"]
        state=self.cleaned_data["state"]
        zipcode=self.cleaned_data["zipcode"]
        phone=self.cleaned_data["phone"]
        
        if len(site) > 2 and not site.startswith("http://") and not site.startswith("https://"): 
            site="http://"+site
            
        newEmployer=Employer(website=site, company_name=company_name,oncampus=oncampus,description=description,address1=address1, address2=address2,city=city,state=state,zipcode=zipcode,phone=phone)
        newEmployer.userprofile=user.userprofile
        newEmployer.save()
        
        user.userprofile.employer=newEmployer
        user.userprofile.save()

        employergroup = Group.objects.get_or_create(name=employergroupname)
        user.groups.add(employergroup[0])

        user.save()
        return user

class EmployerUserEditForm(forms.ModelForm):
    
    error_messages = {
        'address_invalid': _("Off campus employees must enter a valid address"),
    }
    
    email = forms.EmailField(label = "*Email")
    first_name = forms.CharField(label = "*First name")
    last_name = forms.CharField(label = "*Last name")
    company_name = forms.CharField(label = "*Company Name")
    website = forms.CharField(label = "Company Website",required=False)
    description = forms.CharField(label = "Description", widget=forms.widgets.Textarea(attrs={'rows':3, 'cols':40}), help_text = _("Optional company description"),required=False)
    oncampus = forms.BooleanField(label = "On Campus Employer",widget=forms.CheckboxInput(),initial=True,required=False)    
    address1 = forms.CharField(label = "Address Line 1", help_text = _("Address only required for off campus employers"),required=False)
    address2 = forms.CharField(label = "Address Line 2",required=False)
    city = forms.CharField(label = "City",required=False)
    state = forms.CharField(label = "State", max_length=2, min_length=2, widget=forms.TextInput(attrs={'size':'2'}),required=False)
    zipcode = forms.CharField(label = "Zipcode", max_length=5, min_length=5, widget=forms.TextInput(attrs={'size':'5'}),required=False)
    phone = forms.CharField(label = "*Phone Number", max_length=16, min_length=10, widget=forms.TextInput(attrs={'size':'16'}))
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "company_name", "email", "phone", "website","description","oncampus","address1","address2","city","state","zipcode",)
    
    def clean_city(self):
        city = self.cleaned_data["city"]
        oncampus = self.cleaned_data["oncampus"]
        if oncampus == False and (city is None or city == ''):
            raise forms.ValidationError(self.error_messages['address_invalid'])
        return city            
    
    def clean_state(self):
        state = self.cleaned_data["state"]
        oncampus = self.cleaned_data["oncampus"]
        if oncampus == False and (state is None or state == ''):
            raise forms.ValidationError(self.error_messages['address_invalid'])
        return state
    
    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        oncampus = self.cleaned_data["oncampus"]
        if oncampus == False and (zipcode is None or zipcode == ''):
            raise forms.ValidationError(self.error_messages['address_invalid'])
        return zipcode
        
    def save(self):
        
        logger.debug('Saving employer')
        logger.debug('self.instance.pk='+str(self.instance.pk))
        employer=Employer.objects.get(pk=self.instance.userprofile.employer.pk)
        user=User.objects.get(pk=self.instance.pk)
        
        user.is_active=False
        user.first_name=self.cleaned_data["first_name"]
        user.last_name=self.cleaned_data["last_name"]
        user.username=(self.cleaned_data["email"])
        user.email=self.cleaned_data["email"]
        user.save()
        
        site=self.cleaned_data["website"]
        description=self.cleaned_data["description"]
        company_name=self.cleaned_data["company_name"]
        oncampus=self.cleaned_data["oncampus"]
        address1=self.cleaned_data["address1"]
        address2=self.cleaned_data["address2"]
        city=self.cleaned_data["city"]
        state=self.cleaned_data["state"]
        zipcode=self.cleaned_data["zipcode"]
        phone=self.cleaned_data["phone"]
        
        if len(site) > 2 and not site.startswith("http://") and not site.startswith("https://"):
            logger.debug('Adding scheme to site name');
            site="http://"+site
        
        employer.description=description
        logger.debug('setting website to '+site)
        employer.website=site
        employer.company_name=company_name
        employer.oncampus=oncampus
        employer.address1=address1
        employer.address2=address2
        employer.city=city
        employer.state=state
        employer.zipcode=zipcode
        employer.phone=phone
        employer.save()
        
        return user