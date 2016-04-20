import json
import time

from lxml import etree as ElementTree
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from student.models import StudentUserCreationForm, StudentUserEditForm, StudentSearch
from needanerd import studentgroupname
from needanerd.views import isStudent
from needanerd.urls import permission_denied_url
from resume.models import *
from job.models import Job
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.db.models import Q 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

import datetime, random, sha, logging
import operator
import httplib

logger = logging.getLogger('NeedANerd.custom')

@login_required
def students(request):
    
    logger.debug("students called")
    
    studentList=User.objects.filter(groups__name=studentgroupname)
    logger.debug('Found %s students',studentList.count())
    
    paginator = Paginator(studentList, 5) # Show 5 contacts per page
    page = request.GET.get('page')
    
    try:
        students = paginator.page(page)
        
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
        
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)
    
    return render_to_response('students.html', {'students': students}, context_instance=RequestContext(request))

@login_required
def student_profile(request):
    
    logger.debug("student_profile called")
    
    if isStudent(request.user):
        logger.debug('user pk=%s',request.user.pk)
        return student_detail(request, request.user.pk)
    else:
        logger.debug('userprofile is neither student nor employer, discuss amongst yourselves')
        return HttpResponseRedirect(reverse_lazy('home'))
    
@login_required
def student_detail(request, student_id):
    
    logger.debug("student_detail called")
    
    u = get_object_or_404(User, pk=student_id)
    j = u.userprofile.student.job_set.all()
    
    logger.debug('Found student with user id=%d',u.id)
    
    if not isStudent(u):
        'Invalid URL just send them home'
        logger.debug('Invalid URL, just send them home')
        return HttpResponseRedirect(reverse_lazy('home'))
    
    resumes=Resume.objects.filter(student=u.userprofile.student)[:1]
            
    if resumes:
        
        resume=resumes[0]
        
        #resume = Resume(student=u.userprofile.student)
        #logger.debug('resume.pk='+str(resume.pk))
        degrees=Degree.objects.filter(resume__pk=resume.pk)
        skills=Skill.objects.filter(resume__pk=resume.pk)
        certs=Certification.objects.filter(resume__pk=resume.pk)
        empls=Employment.objects.filter(resume__pk=resume.pk)
        
        resume_json = serializers.serialize("json", [resume])
        degrees_json  = serializers.serialize("json", degrees)
        employers_json  = serializers.serialize("json", empls)
        skills_json  = serializers.serialize("json", skills)
        certs_json  = serializers.serialize("json", certs)
        logger.debug(degrees_json)
        logger.debug('resume str: ' + resume_json)

    msg = request.session.get('msg')
    if msg:
        logger.debug('Message: ' + msg)
        del request.session['msg']
    else:
        logger.debug('No message')
        
    'Check for LinkedIn Variables'
    error=request.GET.get('error')
    accesscode = request.GET.get('code')
    
    if u.pk != request.user.pk:
        
        if resumes:
            return render_to_response('student_detail.html', {'msg':msg,'student': u, 'resume': resume_json, 'jobs': j, 'degrees': degrees_json, 'skills': skills_json, 'certs': certs_json, 'empls': employers_json}, context_instance=RequestContext(request))
        else:
            logger.debug('Resume was not found for the student')
            return render_to_response('student_detail.html', {'msg':msg,'student': u, 'jobs': j}, context_instance=RequestContext(request))
    
    if error:
        
        logger.debug('Error code found: '+error)
        request.session['msg'] = 'Your login attempt with LinkedIn was unsuccessful: ' + error
        '''
        if u.pk == request.user.pk:
            if resumes:
                return render_to_response('student_detail.html', {'msg':msg,'hasCRUDPrivs': True, 'student': u, 'resume': resume_json, 'jobs': j, 'degrees': degrees_json, 'skills': skills_json, 'certs': certs_json, 'empls': employers_json}, context_instance=RequestContext(request))
            else:
                return render_to_response('student_detail.html', {'msg':msg,'hasCRUDPrivs': True, 'student': u}, context_instance=RequestContext(request))
        else:
            return render_to_response('student_detail.html', {'msg':msg,'student': u, 'resume': resume_json, 'jobs': j, 'degrees': degrees_json, 'skills': skills_json, 'certs': certs_json, 'empls': employers_json}, context_instance=RequestContext(request))
        '''
        return HttpResponseRedirect(reverse_lazy('profile'))
    
    elif accesscode:
        
        logger.debug('authorization code found '+ accesscode)
        logger.debug('Request Access Token by exchanging the authorization_code for it')
        
        conn = httplib.HTTPSConnection(settings.LINKED_IN_URL)
        
        context = "/uas/oauth2/accessToken?grant_type=authorization_code&code="+accesscode+"&redirect_uri="+settings.HOST+""+request.path+"&client_id="+settings.LINKED_IN_API_KEY+"&client_secret="+settings.LINKED_IN_SECRET_KEY
        logger.debug('context='+context)
        #conn.putrequest("POST", context)
        #'Python bug, httplib should be auto calculating the content-length but its not, so we are setting it to 0'
        #header = {'content-length' : '0'}
        headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
        #conn.putheader(header)
        #conn.endheaders()
        #conn.set_debuglevel(1)
        #conn.send("")
        conn.request("POST", context, '', headers)
        
        'Expecting a JSON response'
        responsestr = conn.getresponse().read()
        logger.debug('response='+responsestr)
        
        responseJSON = json.loads(responsestr)
        oauth2_access_token = responseJSON['access_token']
        logger.debug('access token='+oauth2_access_token)
        
        logger.debug('Populate LinkedIn Data...')
        conn = httplib.HTTPSConnection(settings.LINKED_IN_API_URL)
        
        fieldselectors="id,first-name,last-name,email-address,industry,summary,positions,educations,skills,certifications"
        
        context = "/v1/people/~:("+fieldselectors+")?oauth2_access_token="+oauth2_access_token
        logger.debug('context='+context)
        conn.request("GET",context)
        response = conn.getresponse()
        respstr = response.read()
        logger.debug('Status='+str(response.status)+", Reason="+response.reason)
        logger.debug('Response='+respstr)
    
        'Delete previous data, we are not syncing with LinkedIn...'
        if resumes:
            logger.debug('Deleting previous employments')
            Employment.objects.filter(resume=resumes[0]).delete()
            
            logger.debug('Deleting previous certifications')
            Certification.objects.filter(resume=resumes[0]).delete()
            
            logger.debug('Deleting previous degrees')
            Degree.objects.filter(resume=resumes[0]).delete()
            
            logger.debug('Deleting previous skills')
            Skill.objects.filter(resume=resumes[0]).delete()
            
            logger.debug('Deleting previous resumes, we are now syncing with LinkedIn')
            Resume.objects.filter(student=u.userprofile.student).delete()
        
        tree = ElementTree.fromstring(respstr)
        if tree is None:
            logger.debug("Tree is not valid!!!")
            return HttpResponseRedirect(reverse_lazy('home'))
        
        
        '''Create new resume'''
        logger.debug('Creating new resume...')
        r = Resume()
        
        r.objective=tree.find("summary").text
        logger.debug('Adding new summary: '+tree.find("summary").text)
        r.student=u.userprofile.student
        r.save()
        logger.debug('r.objective: '+r.objective)   
        
        '''Create new work history'''
        positions = tree.findall('positions/position') 
        empls = []
        for p in positions:
            
            logger.debug('Adding position...')
            
            company=p.find("company/name")
            summary=p.find("summary")
            title=p.find("title")
            startyear=p.find("start-date/year")
            startmonth=p.find("start-date/month")
            iscurrent=p.find("is-current")
            endyear=p.find("end-date/year")
            endmonth=p.find("end-date/month")
            
            e = Employment()
            e.resume=r
            if company is not None and company.text is not None:
                e.company=company.text
            if title is not None and title.text is not None:
                e.title=title.text
            if summary is not None and summary.text is not None:
                e.jobfunctions=summary.text
            startdate=""
            if startmonth is not None and startmonth.text is not None:
                startdate += startmonth.text
            if startyear is not None and startyear.text is not None:
                startdate += "/"
                startdate += startyear.text
            e.startdate=startdate
            enddate=""
            if endmonth is not None and endmonth.text is not None:
                enddate += endmonth.text
            if endyear is not None and endyear.text is not None:
                enddate += "/"
                enddate += endyear.text
            e.enddate=enddate
            
            e.save()
            empls.append(e)
        
        '''Create new education history'''
        educations = tree.findall('educations/education')
        degrees = []
        for e in educations:
            
            logger.debug('Adding degree...')
            
            degree=e.find("degree")
            major=e.find("field-of-study")
            univ=e.find("school-name")
            endyear=e.find("end-date/year")
        
            d = Degree()
            d.resume=r
            if degree is not None and degree.text is not None:
                d.degreetype=degree.text
            if major is not None and major.text is not None:
                logger.debug('major.text='+major.text)
                d.major=major.text
            if univ is not None and univ.text is not None:
                d.university=univ.text
            if endyear is not None and endyear.text is not None:
                d.date=endyear.text
            d.save()
            degrees.append(d)
        
        '''Create new skillset'''
        skills = tree.findall('skills/skill') 
        skillsarr = []
        for s in skills:
            
            skill=s.find("skill/name")
            if skill is not None and skill.text is not None:
                s = Skill()
                s.resume=r
                s.skill=skill.text
                logger.debug('Adding skill...')
                s.save()
                skillsarr.append(s)
        
        '''Create new certifications'''
        certs = tree.findall('certifications/certification')
        certsarr = []
        for c in certs:
            
            logger.debug('Adding certificate...')
            
            cert=c.find("name")
            if cert is not None and cert.text is not None:
                c = Certification()
                c.resume=r
                c.name=cert.text
                logger.debug('Adding cert...')
                c.save()
                certsarr.append(c)
        
        resume_json = serializers.serialize("json", [r])
        degrees_json  = serializers.serialize("json", degrees)
        employers_json  = serializers.serialize("json", empls)
        skills_json  = serializers.serialize("json", skillsarr)
        certs_json  = serializers.serialize("json", certsarr)
        logger.debug('resume str: ' + resume_json)

        #msg = "Successfully synced with LinkedIn!"
        request.session['msg'] = 'Successfully synced with LinkedIn!'
        return HttpResponseRedirect(reverse_lazy('profile'))
        
        #return render_to_response('student_detail.html', {'msg':msg, 'hasCRUDPrivs': True, 'student': u, 'resume': resume_json, 'jobs': j, 'degrees': degrees_json, 'skills': skills_json, 'certs': certs_json, 'empls': employers_json}, context_instance=RequestContext(None))
        
    else:
        
        '''
        #reviewList=StudentReview.objects.select_related().filter(student__pk=u.userprofile.student.pk).order_by('-created_at')
        paginator = Paginator(None, 5) # Show 25 contacts per page
    
        page = request.GET.get('page')
        
        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            reviews = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            reviews = paginator.page(paginator.num_pages)
        
        try:
            r=u.userprofile.student.resume    
            logger.debug('Found Resume with pk %s for this student',r.pk)
            return render_to_response('student_detail.html', {'student': u, 'resume': r, 'jobs': j, 'reviews': reviews}, context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            logger.debug('Resume was not found for the student')
            return render_to_response('student_detail.html', {'student': u, 'jobs': j, 'reviews': reviews}, context_instance=RequestContext(request))
        '''
        
        if resumes:
            return render_to_response('student_detail.html', {'msg':msg,'hasCRUDPrivs': True, 'student': u, 'resume': resume_json, 'jobs': j, 'degrees': degrees_json, 'skills': skills_json, 'certs': certs_json, 'empls': employers_json}, context_instance=RequestContext(request))
        else:
            logger.debug('Resume was not found for the student')
            return render_to_response('student_detail.html', {'msg':msg,'hasCRUDPrivs': True, 'student': u,'jobs': j}, context_instance=RequestContext(request))
        
            
@login_required
def studentsearch(request):     

    logger.debug("studentsearch called")
    
    if 'str' in request.GET:
        strval = request.GET['str']
        
    logger.debug('Search for students based up on search string='+strval)
    
    search_args = []
    for term in strval.split():
        for query in ('first_name__icontains', 'last_name__icontains', 'userprofile__student__currentmajor__icontains'):
            search_args.append(Q(**{query: term}))

    userList = User.objects.filter(groups__name=studentgroupname).filter(reduce(operator.or_, search_args))
    
    ss = []
    for user in userList:
        
        resumes=Resume.objects.filter(student=user.userprofile.student)[:1]
        if resumes:
            resume=resumes[0]
            robj=resume.objective
            logger.debug('found robj:'+robj)
        else:
            robj=""
        
        obj = StudentSearch(studentid=user.pk,first_name=user.first_name, last_name=user.last_name, 
              currentmajor=user.userprofile.student.currentmajor, objective=robj)
        ss.append(obj)
        
    logger.debug('Found %s students',userList.count())
    json_serializer = serializers.get_serializer("json")()
    response = json_serializer.serialize(ss)
    
    return HttpResponse(response)

@login_required
@user_passes_test(isStudent, login_url=permission_denied_url)
def editStudentForm(request, student_id):
    
    logger.debug("editstudentform called")
    
    u = get_object_or_404(User, pk=student_id)
    if u.pk == request.user.pk and isStudent(u):
        if request.method == 'POST': # If the form has been submitted...
            logger.debug('request.method == POST')
            form = StudentUserEditForm(request.POST, instance=u) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                logger.debug('form.is_valid()==true')
                form.save()
                return HttpResponseRedirect('/students/'+str(u.pk)+'/') # Redirect after POST
        else:
            try:
                form = StudentUserEditForm(instance=u, initial={'first_name': u.first_name, 'last_name': u.last_name,
                                                             'email': u.email, 'currentmajor': u.userprofile.student.currentmajor})
            except:
                logger.debug('u.email ' + u.userprofile)
                form = StudentUserEditForm(instance=u)
                
        return render_to_response('editstudent.html', {
            'form': form},
            context_instance=RequestContext(request))
    else:        
        response=HttpResponse()
        response.write("You are not authorized to edit this profile")
        response.status_code=401
        logger.info('Returning a 401 unauthorized')
        logger.info('User: ' + str(request.user.pk) + " tried to edit the student with user id: " + str(u.id) )
        return response  

@login_required
@user_passes_test(isStudent, login_url=permission_denied_url)
def studentApplication(request, student_id, job_id):
    
    logger.debug("studentApplication called")
    
    u = get_object_or_404(User, pk=student_id)
    j = get_object_or_404(Job, pk=job_id)
    
    s = u.userprofile.student
    j.applicant.add(s)
    subject = 'Need a Nerd Notificaiton: New Applicant For Your Job Posting'
    message = 'Employer of Nerds, A nerd has applied for your latest job position of '+str(j.name)+'. Login to needanerd for details'
    'There is a probably a better way to do this but I am getting tired'
    user=User.objects.select_related().filter(userprofile__employer__job__pk=j.pk).get()
    recipient=user.email
    logger.debug('Sending notification email to '+recipient)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
    
    return HttpResponse("Student has applied for job")

def studentForm(request):

    logger.debug("studentForm called")
    
    if request.method == 'POST': # If the form has been submitted...
        logger.debug('request.method == POST')
        form = StudentUserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            logger.debug('form.is_valid()==true')
            form.save()
            #username=form.cleaned_data['username']
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
            recipients = [form.cleaned_data['email']]
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
            return HttpResponseRedirect('/accounts/activate/') # Redirect after POST
        
        else:
            return render_to_response('registerStudent.html', {'form': form}, context_instance=RequestContext(request))
            
    else:

        form = StudentUserCreationForm() # An unbound form
        return render_to_response('registerStudent.html', {'form': form}, context_instance=RequestContext(request))
