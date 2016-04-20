from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q 
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.contrib.auth.decorators import user_passes_test, login_required
from job.models import Job, JobForm, JobSearch#, JobEditForm
from resume.models import Resume
from needanerd.views import isStudent, isEmployer
from needanerd import studentgroupname, employergroupname
from needanerd.urls import permission_denied_url
from django.utils.datastructures import MultiValueDictKeyError
from student.models import Student
from datetime import datetime
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
import operator
import logging
from threading import Thread

# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

def notifyStudentsNewJob(job):

    studentList=User.objects.filter(groups__name=studentgroupname).order_by('last_name')
    
    logger.debug('Now notifying %s students of the new posting',studentList.count())
            
    subject = 'Need a Nerd Notification: '+job.name+' apply now!'
    message = 'Hello Nerd, There is a new job posting.  Login to need a nerd for details\n'+settings.HOST+'/jobs/'+str(job.pk)
    for s in studentList:
        recipient=s.email
        logger.debug('Sending notification email to '+recipient)
        from django.core.mail import send_mail
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
        
@login_required
def jobsearch(request):
    
    if 'str' in request.GET:
        strval = request.GET['str']
            
    logger.debug('Search for jobs based up on search string='+strval)
    
    #userList=User.objects.filter(groups__name=groups.studentgroupname).filter(Q(first_name__contains=strval) |
    #                                                                          Q(last_name__contains=strval )).order_by('last_name')
    
    search_args = []
    for term in strval.split():
        for query in ('name__icontains', 'employer__company_name__icontains', 'skills__icontains', 'description__icontains'):
            search_args.append(Q(**{query: term}))

    jobList = Job.objects.filter(reduce(operator.or_, search_args))
    
    js = []
    for job in jobList:
        appliedValue=False
        if isStudent(request.user):
            studentpk=str(request.user.pk)
            if job in request.user.userprofile.student.job_set.all():
                appliedValue=True
        'There is a probably a better way to do this but I am getting tired'
        user=User.objects.select_related().filter(userprofile__employer__job__pk=job.pk).get()
        datestr=job.updated_at.strftime('%b')
        datestr=datestr.upper()
        datestr+=job.updated_at.strftime(' %d %Y')
        if studentpk:
            obj = JobSearch(jobpk=str(job.pk), studentpk=studentpk, name=job.name, employer=job.employer.company_name, employerpk=user.pk, salary=job.salary, applied=appliedValue, updated_at=datestr)
        else:
            obj = JobSearch(jobpk=str(job.pk), name=job.name, employer=job.employer.company_name, employerpk=user.pk, salary=job.salary, applied=appliedValue, updated_at=datestr)
        js.append(obj)
        
    logger.debug('Found %s jobs',jobList.count())
    json_serializer = serializers.get_serializer("json")()
    response = json_serializer.serialize(js)
    return HttpResponse(response)

@login_required
@user_passes_test(isStudent, login_url=permission_denied_url)
def applyJob(request):
    u = request.user
    e = User.objects.filter(groups__name=employergroupname)
    
    resumes=Resume.objects.filter(student=u.userprofile.student)[:1]
    if resumes:
        resume=resumes[0]
    else:
        resume=None
    
    
    joblist = Job.objects.filter(released=True).order_by('-updated_at')
    paginator = Paginator(joblist, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        j = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        j = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        j = paginator.page(paginator.num_pages)
    
     
    return render_to_response('applyjobs.html', {'student': u, 'jobs': j, 'employers': e, 'resume': resume}, context_instance=RequestContext(request))

@login_required
def jobList(request, student_id):
    
    u = get_object_or_404(User, pk=student_id)
    
    if isStudent(u):
        logger.debug('Found student with user id=%d',u.id)
        joblist = u.userprofile.student.job_set.all()
        msg = 'You have applied to the following positions'
    else:
        joblist = Job.objects.filter(released=True).order_by('-updated_at')
    
    paginator = Paginator(joblist, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        j = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        j = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        j = paginator.page(paginator.num_pages)

    return render_to_response('listjobs.html', {'msg': msg, 'student': u, 'jobs': j}, context_instance=RequestContext(request))

@login_required
def job_detail(request, job_id):
    logger.debug("job_detail called")
    j = get_object_or_404(Job, pk=job_id)
    u=User.objects.select_related().filter(userprofile__student__job__pk=j.pk)
    logger.debug('Student(s) found for the job')
    form = JobForm(instance=j) # An unbound form    
    return render_to_response('job_detail.html', {'job': j, 'students': u, 'form': form, 'startdate': j.startdate, 'enddate': j.enddate}, context_instance=RequestContext(request))

@login_required
def applicantlist(request, job_id):
    
    logger.debug("ApplicantList called")
    j = get_object_or_404(Job, pk=job_id)

    if not j.employer.pk == request.user.userprofile.employer.pk:
        return HttpResponseForbidden()

    applicants = Student.objects.filter(job__pk=j.pk)
    logger.debug('Found ' + str(len(applicants)) + ' applicant(s) for job id='+str(j.pk));
    paginator = Paginator(applicants, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        a = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        a = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        a = paginator.page(paginator.num_pages)

    logger.debug('Job.name='+j.name);
    return render_to_response('listapplicants.html', {'applicants': a, 'job': j}, context_instance=RequestContext(request))


@login_required
@user_passes_test(isEmployer, login_url=permission_denied_url)
def deleteJob(request, job_id):
    logger.debug("deleteJob called")
    j = get_object_or_404(Job, pk=job_id)
    response = HttpResponse('')
    if j.employer.pk == request.user.userprofile.employer.pk:
        j.delete()
        logger.debug('Job Deleted')
        response.write("Job Deleted")
    else:        
        response.write("You are not authorized to delete this job")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
    return HttpResponse(response)

def checkdates(form):
            
        logger.debug('checkdates called')
        
        startdate=form.data['startdate']
        if not startdate:
            logger.debug('Startdate not provided')
            form.date_errors = 'Start date not provided'
            return False
        
        permposition=form.data.get('permposition', False)
        if permposition:
            logger.debug('This is a permenant position')
            return True
        
        enddate=form.data['enddate']
        logger.debug('startdate='+str(startdate))
        logger.debug('enddate='+enddate)
        
        startdatearr = startdate.split('/')
        startmonth = startdatearr[0]
        startyear = startdatearr[1]
        startdatenew = startmonth + "/01/" + startyear
        
        enddatearr = enddate.split('/')
        endmonth = enddatearr[0]
        endyear = enddatearr[1]
        enddatenew = endmonth + "/01/" + endyear
        
        start = datetime.strptime(startdatenew, '%m/%d/%Y')
        end = datetime.strptime(enddatenew, '%m/%d/%Y')
        if end < datetime.now():
            form.date_errors="ERROR: The end date cannot be before the current date"
            logger.debug(form.date_errors)
            return False
            #raise forms.ValidationError("You cannot enter an end date in the past") 
        elif end < start:
            form.date_errors="ERROR: The start date cannot be after the end date"
            logger.debug(form.date_errors)
            return False
            #raise forms.ValidationError("End date cannot be before start date")
        else:
            return True
        
@login_required
@user_passes_test(isEmployer, login_url=permission_denied_url)
def jobForm(request):
    if request.method == 'POST': # If the form has been submitted...
        logger.debug('request.method == POST')
        form = JobForm(request.POST) # A form bound to the POST data
        checkdatesbool = checkdates(form)
        logger.debug('Checkdates() returned ' + str(checkdatesbool))
        if form.is_valid() and checkdatesbool: # All validation rules pass
            job = form.save(request.user.pk)
            t = Thread(target=notifyStudentsNewJob, args=(job,))
            t.start()
            return HttpResponseRedirect('/employers/myjobs/') # Redirect after POST
        else:
            logger.debug('Posted form is not valid')
            logger.debug('form.errors='+str(form.errors))
            logger.debug('form.non_field_errors='+str(form.non_field_errors))
            
    else:
        logger.debug('form is not valid')
        form = JobForm() # An unbound form

    return render_to_response('addjob.html', {
        'form': form},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(isEmployer, login_url=permission_denied_url)
def editJobForm(request, job_id):
    
    logger.debug("Edit Job Form")
    j = get_object_or_404(Job, pk=job_id)
    if j.employer.pk == request.user.userprofile.employer.pk:
        if request.method == 'POST': # If the form has been submitted...
            logger.debug('request.method == POST')
            form = JobForm(request.POST, instance=j) # A form bound to the POST data
            if form.is_valid() and checkdates(form): # All validation rules pass
                logger.debug('form.is_valid()==true for employerid='+form.data['employerid'])
                form.save(request.user.pk)
                return HttpResponseRedirect('/employers/myjobs/') # Redirect after POST
            else:
                logger.debug('Posted form is not valid')
                logger.debug('form.errors='+str(form.errors))
                logger.debug('form.non_field_errors='+str(form.non_field_errors))
                logger.debug('form.date_errors='+str(form.date_errors))
        else:
            form = JobForm(instance=j) # An unbound form    
        return render_to_response('editjob.html', {'form': form, 'jobid': job_id, 'startdate': j.startdate, 'enddate': j.enddate}, context_instance=RequestContext(request))
    
    else:        
        response=HttpResponse()
        response.write("You are not authorized to delete this job")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response  
