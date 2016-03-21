#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.core.paginator import Paginator, InvalidPage, EmptyPage
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from appsecurity.models import UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from needanerd.views import isStudent, isEmployer, isAdmin
from student.models import Student
from resume.models import Resume
from django.core.mail import send_mail
import datetime, random, sha, logging
from django.conf import settings
from needanerd import studentgroupname
from django.contrib.auth.models import User, Group
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware

#from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
#import urls

# import the logging library
import logging, datetime

# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')


 


@requires_csrf_token
def login_user(request):
 
    logger.debug('login called')
    
    username = password = ''
    if request.POST:
        logger.debug('This is a POST')
        username = request.POST['username']
        password = request.POST['password']
        logger.debug('User %s, Password %s',username,password)
        user = authenticate(username=username, password=password)
        if user is not None:
            
            if user.is_active:
                logger.debug('Logging in user %s', user)
                login(request, user)
                
                'Set the session cookie to never expire if remember me is checked'
                if not request.POST.get('rememberme', None):
                    logger.debug('Setting the cookie session to 1 month')
                    request.session.set_expiry(2419200)
                    
                if 'next' in request.POST:
                    nexturl = request.POST['next']
                    logger.debug('Next %s',nexturl)
                    return HttpResponseRedirect(nexturl)
                else:
                    return HttpResponseRedirect('/profile/')
            else:
                errmsg = 'Account not activated, click the activation link in the email you were sent. Click <a href='+settings.HOST+'/accounts/reactivate/'+str(user.pk)+'/>here</a> to resend the activation email'
        else:
            errmsg = 'Invalid Email and Password Combo'
        return render_to_response('registration/login.html', {'errmsg':errmsg}, context_instance=RequestContext(request))
    else:
        if 'next' in request.GET:
            nexturl = request.GET['next']
            logger.debug('Next %s',nexturl)
            return render_to_response('registration/login.html', {'msg': 'Employers must register through email','nexturl':nexturl},context_instance=RequestContext(request))
        else:
            return render_to_response('registration/login.html', {'msg': 'Employers must register through email'}, context_instance=RequestContext(request))
        
@login_required
def social_login_post_processing(request):

    if request.user.is_authenticated():
        studentgroup = Group.objects.get_or_create(name=studentgroupname)
        user = get_object_or_404(User, username=request.user.username)
        
        newStudent=Student()
        newStudent.userprofile=user.userprofile
        newStudent.save()
        user.userprofile.student=newStudent
        user.userprofile.save()
        studentgroup = Group.objects.get_or_create(name=studentgroupname)
        user.groups.add(studentgroup[0])
        user.save()
        
        return HttpResponseRedirect(reverse_lazy('profile'))
    else:
        return HttpResponseRedirect(reverse_lazy('home'))

def activate(request):
    logger.debug('activate called')
    if 'oncampus' in request.GET:
        oncampus = request.GET['oncampus']
        logger.debug('oncampus='+str(oncampus))
        if oncampus == 'False':
            return render_to_response('activate.html', {'offcampus': True}, context_instance=RequestContext(request))
    else:
        logger.debug('oncampus var was not passed to activate')
    return render_to_response('activate.html', context_instance=RequestContext(request))

def reactivate(request, user_id):
    
    
    logger.debug('reactivate pk='+user_id)
    user=get_object_or_404(User, pk=user_id)
    
    if user.is_active:
        request.session['msg'] = 'This account has already been activated'
        return HttpResponseRedirect(reverse_lazy('home'))
    
    username = user.username
    
    salt = sha.new(str(random.random())).hexdigest()[:5]
    activation_key = sha.new(salt+username).hexdigest()
    now = timezone.now()
    key_expires = now + datetime.timedelta(2)
    
    userprofile = user.userprofile
    userprofile.activation_key=activation_key
    userprofile.key_expires=key_expires
    userprofile.save()
    
    now = timezone.now()
            
    subject = 'Need a Nerd Reactivation'
    message = "Hello %s, and thanks for signing up for a "\
        "need a nerd account!\n\nTo activate your account, click this link within 48 "\
        "hours:\n\n " % (user.first_name)
    message += settings.HOST
    message += "/accounts/confirm/"
    message += activation_key                                                                                                         
    recipients = [user.email]
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
    return HttpResponseRedirect('/accounts/activate/') # Redirect after POST
        
def confirm(request, key):
    logger.debug('Confirming account with activation key='+key)
    if request.user.is_authenticated():
        logger.debug('This user already has an account')
        return render_to_response('index.html', {'errmsg': 'You already have an account. Make sure you are not logged in as someone else if you are trying to activate a new account'}, context_instance=RequestContext(request))
    
    user_profile = get_object_or_404(UserProfile, activation_key=key)
    #now = datetime.datetime.utcnow()
    #now = now.replace(tzinfo=timezone.utc)
    now = timezone.now() 
    if user_profile.key_expires < now:
        return render_to_response('index.html', {'errmsg': 'This link has expired, you must re-register'}, context_instance=RequestContext(request))
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    #return render_to_response('confirm.html', {'success': True}, context_instance=RequestContext(request))
    return render_to_response('index.html', {'msg': 'Congratulations, your account is actived', 'success': True}, context_instance=RequestContext(request))


def user_delete(request, user_id):
    
    logger.debug('Attempting to delete user with pk='+user_id)
    user=get_object_or_404(User, pk=user_id)
    
    if int(request.user.pk) != int(user_id):
        logger.debug('request.user.pk='+str(request.user.pk))
        logger.debug('user_id='+str(user_id))
        return render_to_response('userdelete.html', {'wrongpk': True}, context_instance=RequestContext(request))
    if isStudent(user):
        
        resumes=Resume.objects.filter(student=user.userprofile.student)[:1]
            
        if resumes:
        
            resume=resumes[0]
            resume.delete()
                      
        try:
            user.userprofile.student
            user.userprofile.student.delete()
        except ObjectDoesNotExist:        
            logger.debug('No student was object was linked to this user profile')
        
        try:
            user.userprofile
            user.userprofile.delete()
        except ObjectDoesNotExist:        
            logger.debug('No user profile was found')
        
        user.delete()
        
        return render_to_response('userdelete.html', {'student': True}, context_instance=RequestContext(request))
    
    elif isEmployer(user):
        
        try:
            user.userprofile.employer.job_set.all()
            user.userprofile.employer.job_set.all().delete()
        except ObjectDoesNotExist:      
            logger.debug('No jobs were found for this employer')
        
        try:
            user.userprofile.employer
            user.userprofile.employer.delete()        
        except ObjectDoesNotExist:        
            logger.debug('No employer was object was linked to this user profile')
        
        try:
            user.userprofile
            user.userprofile.delete()
        except ObjectDoesNotExist:        
            logger.debug('No user profile was found')
        
        user.delete()
        return render_to_response('userdelete.html', {'employer': True}, context_instance=RequestContext(request))
    elif isAdmin(user):
        user.userprofile.delete()
        user.delete()
        return render_to_response('userdelete.html', {'admin': True}, context_instance=RequestContext(request))
    else:
        return render_to_response('userdelete.html', {'error': True}, context_instance=RequestContext(request))

