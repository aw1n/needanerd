from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from employer.models import Employer, EmployerUserCreationForm, EmployerUserEditForm
from django.core import serializers
from needanerd.urls import permission_denied_url
from needanerd.views import isStudent, isEmployer
from job.models import Job
import datetime, random, sha
from needanerd import employergroupname
import logging
from django.conf import settings
from django.core.mail import send_mail, mail_admins
from django.utils import timezone

# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

@login_required
def employers(request):
    
    userList=User.objects.filter(groups__name=employergroupname)
    logger.debug('Found %s employers',userList.count())
    
    paginator = Paginator(userList, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)
    return render_to_response('employers.html', {'employers': users}, context_instance=RequestContext(request))


    return render_to_response('employers.html', {'employers': userList}, context_instance=RequestContext(request))

@login_required
def employer_profile(request):
    
    logger.debug("employer_profile called")
    
    if isEmployer(request.user):
        logger.debug('user pk=%s',request.user.pk)
        return employer_detail(request, request.user.pk)
    else:
        logger.debug('userprofile is neither student nor employer, discuss amongst yourselves')
        return HttpResponseRedirect(reverse_lazy('home'))

@login_required
def employer_detail(request, employer_id):
    
    logger.debug("employer_detail called")
    u = get_object_or_404(User, pk=employer_id)
    
    if not isEmployer(u):
        'Invalid URL just send them home'
        logger.debug('Invalid URL, just send them home')
        return HttpResponseRedirect(reverse_lazy('home'))
    
    msg = request.session.get('msg')
    if msg:
        logger.debug('Message: %s',msg)
        del request.session['msg']
    else:
        logger.debug('No message')
    
    '''
    reviewList=EmployerReview.objects.select_related().filter(employer__pk=u.userprofile.employer.pk).order_by('-created_at')
    paginator = Paginator(reviewList, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reviews = paginator.page(paginator.num_pages)
    return render_to_response('employer_detail.html', {'employer': u, 'jobs': j,'reviews': reviews},context_instance=RequestContext(request))
    '''
    '''if int(employer_id) == request.user.pk:
        j=Job.objects.select_related().filter(employer__pk=u.userprofile.employer.pk)
    else:
        logger.debug('request.user.pk='+str(request.user.pk)+' employer_id='+employer_id)
        'Filter by jobs released for viewing'
        j=Job.objects.select_related().filter(employer__pk=u.userprofile.employer.pk, released=True)'''
    
    
    if u.pk == request.user.pk:
        logger.debug('has CRUD Privs');
        return render_to_response('employer_detail.html', {'msg':msg,'employer': u, 'hasCRUDPrivs': True},context_instance=RequestContext(request))
    else:
        logger.debug('does not have CRUD Privs');    
        return render_to_response('employer_detail.html', {'msg':msg,'employer': u},context_instance=RequestContext(request))

@login_required
@user_passes_test(isEmployer, login_url=permission_denied_url)
def myjobs(request):
    
    logger.debug("myjobs called")
    u = get_object_or_404(User, pk=request.user.pk)
    
    j=Job.objects.filter(employer__pk=u.userprofile.employer.pk)
    
    return render_to_response('myjobs.html', {'employer': u, 'jobs':j},context_instance=RequestContext(request))

        
def employerForm(request):
    if request.method == 'POST': # If the form has been submitted...
        logger.debug('request.method == POST')
        form = EmployerUserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            logger.debug('form.is_valid()==true')
            form.save()
            username=form.cleaned_data['email']
            logger.debug('New username is: '+username)
            firstname=form.cleaned_data['first_name']
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+username).hexdigest()
            now = timezone.now()
            #key_expires = datetime.datetime.utcnow() + datetime.timedelta(2)
            key_expires = now + datetime.timedelta(2)
            
            user = User.objects.get(username=username)
            userprofile = user.userprofile
            userprofile.activation_key=activation_key
            userprofile.key_expires=key_expires
            userprofile.save()
            subject = 'Confirm Your Need a Nerd Account'
            message = "Hello %s, and thanks for signing up for a "\
                    "need a nerd account!\n\nTo activate your account, click this link within 48 "\
                    "hours:\n\n " % (firstname)
            message += settings.HOST
            message += "/accounts/confirm/"
            message += activation_key                                                                                                               
            
            oncampus= form.cleaned_data['oncampus']
            
            if oncampus == True:
                recipients = [form.cleaned_data['email']]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
                return HttpResponseRedirect('/accounts/activate/') # Redirect after POST
            else:
                recipients = ['needanerd_admin@auburn.edu']
                message = "The following user has requested an account: "+username+"\
                \n\nTo activate your account, click this link within 48 \
                hours:\n\n"
                message += settings.HOST
                message += "/accounts/confirm/%s" % (activation_key)                                                                                                             
                mail_admins(subject, message)
                logger.debug('Mail send to all admins, ok')
                return HttpResponseRedirect('/accounts/activate/?oncampus=False') # Redirect after POST
        
    else:
        logger.debug('form is not valid')
        form = EmployerUserCreationForm() # An unbound form

    return render_to_response('registerEmployer.html', {
        'form': form},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(isEmployer, login_url=permission_denied_url)
def editEmployerForm(request, employer_id):
    
    logger.debug("Edit Job Form")
    u = get_object_or_404(User, pk=employer_id)
    if u.pk == request.user.pk:
        if request.method == 'POST': # If the form has been submitted...
            logger.debug('request.method == POST')
            form = EmployerUserEditForm(request.POST, instance=u) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                logger.debug('form.is_valid()==true')
                form.save()
                return HttpResponseRedirect('/employers/'+str(u.pk)+'/') # Redirect after POST
        else:
            form = EmployerUserEditForm(instance=u, initial={'website': u.userprofile.employer.website, 'company_name': u.userprofile.employer.company_name,
                                                             'description': u.userprofile.employer.description, 'oncampus': u.userprofile.employer.oncampus,
                                                             'address1': u.userprofile.employer.address1, 'address2': u.userprofile.employer.address2,
                                                             'city': u.userprofile.employer.city, 'state': u.userprofile.employer.state,
                                                             'zipcode': u.userprofile.employer.zipcode, 'phone': u.userprofile.employer.phone}) # An unbound form
    
        return render_to_response('editemployer.html', {
            'form': form},
            context_instance=RequestContext(request))
    else:        
        response=HttpResponse()
        response.write("You are not authorized to edit this profile")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response  
    