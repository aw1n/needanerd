#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.core.paginator import Paginator, InvalidPage, EmptyPage
#from django.core.urlresolvers import reverse
from job.models import Job
from smtplib import SMTPException
from needanerd.models import ContactForm, ContactUserForm
#rom resume.models import *
#from student.models import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
#from django.core import serializers
#from django.db.models import Q 
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
#from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.utils import timezone
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, mail_admins
from django.conf import settings

from needanerd import studentgroupname, employergroupname

#import datetime, random, sha
#import operator
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

def isAdmin(user):
    if user.is_staff:
        return True
    else:
        return False
    
def home(request):
    
    logger.debug('Home page accessed')
    
    msg = request.session.get('msg')
    if msg:
        logger.debug('Message: ' + msg)
        del request.session['msg']
    else:
        logger.debug('No message')
        if not request.user.is_authenticated():
            msg = 'Employers must register through email'
        
    #Show the 5 latest job postings if they are available
    if Job.objects.count() > 6:
        j=Job.objects.filter(released=True).order_by('-updated_at')[:6]
        logger.debug('Found ' + str(len(j)) + ' objects' )
    elif Job.objects.count() > 0:
        j=Job.objects.filter(released=True).order_by('-updated_at')[:Job.objects.count()]
        logger.debug('Found ' + str(len(j)) + ' objects' )
    else:
        j=None
    
    
    #if 'appsecurity.views.isAdmin'(request.user):
    #    return render_to_response('index.html', {'admin': True, 'jobs': j}, context_instance=RequestContext(request))
    #else:
    return render_to_response('index.html', {'msg': msg, 'jobs': j}, context_instance=RequestContext(request))

def isStudent(user):
    if user.groups.filter(name=studentgroupname).count() > 0:
        logger.debug('User is in the student group')
        return True
    else:
        logger.debug('User is a not in the student group')
        return False

def isEmployer(user):
    if user.groups.filter(name=employergroupname).count() > 0:
        logger.debug('User is in the employer group')
        return True
    else:
        logger.debug('User is a not in the employer group')
        return False

def profile(request):
    
    logger.debug('profile called')
   
    if isStudent(request.user):
        logger.debug('userprofile pk=%s',request.user.userprofile.pk)
        return HttpResponseRedirect('/students/profile/')
    elif isEmployer(request.user):
        logger.debug('userprofile pk=%s',request.user.userprofile.pk)
        return HttpResponseRedirect('/employers/profile/')
    else:
        logger.debug('userprofile is neither student nor employer, discuss amongst yourselves')
        return HttpResponseRedirect(reverse_lazy('home'))

def notfound(request):
    return render_to_response('404.html',context_instance=RequestContext(request))

def contact(request):
    
    if request.method == 'POST': # If the form has been submitted...
        logger.debug('request.method == POST')
        
        form = ContactForm(data=request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            logger.debug('contact form filled out correctly')
            first = form.cleaned_data['first']
            last = form.cleaned_data['last']
            email = form.cleaned_data['email']
            subject = "needanerd message: " + form.cleaned_data['subject']
            message = "Message from " + first + " " + last + "\nEmail: " + email + "\n\n" + form.cleaned_data['message']
            
            try:
                
                mail_admins(subject, message)
                logger.debug('Mail send to all admins, ok')
                subject="Thank You For Contacting NeedaNerd"
                confirmation="This is an automated message. You have contacted need a nerd through the online form. Please wait for a response. Thank You"
                send_mail(subject, confirmation, settings.DEFAULT_FROM_EMAIL, email.split())
                
            except SMTPException, err:
                logger.debug('Mail send error: %s', err)
            
            request.session['msg'] = 'You have successfully contacted Need a Nerd, we will respond shortly'    
            return HttpResponseRedirect(reverse_lazy('profile')) # Redirect after POST
        
        else:
            return render_to_response('contactbsform.html', {'user': request.user, 'form': form}, context_instance=RequestContext(request))

    '''    
    else:
        if request.user.is_authenticated():
            form = ContactForm() # An unbound form
            form.fields['sender'].initial=request.user.email
        else:
            form = ContactForm() # An unbound form
    '''
    return render_to_response('contactbsform.html', {
        'user': request.user},
        context_instance=RequestContext(request))
    
@login_required
def contactUserForm(request, user_id):
    
    logger.debug('contactUserForm called')
    
    user=get_object_or_404(User, pk=user_id)
    logger.debug('request.user.username ' + request.user.email)
    
    if request.method == 'POST': # If the form has been submitted...
        logger.debug('request.method == POST')
        form = ContactUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            logger.debug('contact form filled out correctly')
            subject = settings.EMAIL_SUBJECT_PREFIX
            subject += " message from "
            subject += request.user.username
            message = form.cleaned_data['message']
            'For whatever reason I could not obtain the values from the form so well just reinsert them here'
            recipients = [user.email]
            cc_myself = form.cleaned_data['cc_myself']
            
            if cc_myself:
                recipients.append(settings.DEFAULT_FROM_EMAIL)
                
            from django.core.mail import send_mail
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
            
            request.session['msg'] = 'Email sent successfully!'
            return HttpResponseRedirect(reverse_lazy('profile')) # Redirect after POST
        
    else:
        if request.user.is_authenticated():
            form = ContactUserForm() # An unbound form

    return render_to_response('contactuser.html', {
        'form': form, 'user':user},
        context_instance=RequestContext(request))

    