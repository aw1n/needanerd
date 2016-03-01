#from django.core.context_processors import csrf
#from django.core.paginator import Paginator, InvalidPage, EmptyPage
#from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.core.urlresolvers import reverse_lazy
from django.core import serializers
from resume.models import *
#from django.db.models import Q 
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from needanerd.views import isStudent
from needanerd.urls import permission_denied_url
#from django.utils import timezone
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import datetime, random, sha
#import groups, urls
#import operator


# Get an instance of a logger
logger = logging.getLogger('NeedANerd.custom')

@login_required
def hasResumeCRUDPriv(request, resume_id):
    
    r = get_object_or_404(Resume, pk=resume_id)
    u = get_object_or_404(User, pk=request.user.pk)
    
    logger.debug('Found user: ' + u.username)
    
    try:
        r1=Resume.objects.filter(student=u.userprofile.student).select_related()[0]
        if isStudent(u) == False:
            logger.debug('UNAUTHORIZED: This user is not a student')
            if r1.pk != r.pk:
                logger.debug('r1.pk='+r1.pk+",r.pk="+r.pk)
                return HttpResponseForbidden()

    except:
        logger.debug('r.pk='+str(r.pk) +'!='+str(u.userprofile.student.resume.pk))
        return HttpResponseServerError()
    
    logger.debug('authorized update called');
    return True
    
'''
@login_required
@user_passes_test(isStudent, login_url=permission_denied_url)
def deleteResume(request, resume_id):
    
    logger.debug("Delete Resume")
    u = get_object_or_404(User, pk=request.user.pk)
    r = get_object_or_404(Resume, pk=resume_id)
    if u.pk == request.user.pk:
        logger.debug('Deleting resume '+str(r.pk))
        r.delete()
        logger.debug('Redirecting to profile')
        return HttpResponseRedirect('/resumes/'+str(r.pk)+'/') # Redirect after POST
        
    else:        
        response=HttpResponse()
        response.write("You are not authorized to edit this profile")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response  
'''

@login_required
@require_http_methods(["POST"])
def createDegree(request, resume_id):
    
    if hasResumeCRUDPriv(request, resume_id):
        
        r = get_object_or_404(Resume, pk=resume_id)
        d = Degree()
        d.resume=r
        d.degreetype=request.POST["degreetype"]
        d.major=request.POST["major"]
        d.university=request.POST["university"]
        d.date=request.POST["date"]
        d.gpa=request.POST["gpa"]
        d.honors=request.POST["honors"]
        d.save()
        
        response = serializers.serialize("json", [d])
        return HttpResponse(response, mimetype='application/json')
    
    else:
        
        response=HttpResponse()
        response.write("You are not authorized to make this change")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response

@login_required
@require_http_methods(["DELETE"])
def deleteDegree(request, resume_id, degree_id):
    
    logger.debug("Delete Degree")
    
    if hasResumeCRUDPriv(request, resume_id):
        
        degrees=Degree.objects.select_related().filter(resume__pk=resume_id)
        d = get_object_or_404(Degree, pk=degree_id)
        
        if d in degrees:
            logger.debug('Deleting degree '+str(d.pk))
            d.delete()
            return HttpResponse("OK")
            #logger.debug('Redirecting to profile')
            #return HttpResponseRedirect(reverse_lazy('profile'))        
          
    response=HttpResponse()
    response.write("You are not authorized to make this change")
    response.status_code=401
    logger.debug('Returning a 401 unauthorized')
    return response

@login_required
@require_http_methods(["POST"])
def createWorkHistory(request, resume_id):
    
    if hasResumeCRUDPriv(request, resume_id):
        
        r = get_object_or_404(Resume, pk=resume_id)
        e = Employment()
        e.resume=r
        e.company=request.POST["company"]
        e.title=request.POST["title"]
        e.startdate=request.POST["startdate"]
        e.enddate=request.POST["enddate"]
        e.jobfunctions=request.POST["jobfunctions"]
        e.save()
    
        response = serializers.serialize("json", [e])
        return HttpResponse(response, mimetype='application/json')

    else:
        
        response=HttpResponse()
        response.write("You are not authorized to make this change")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response


@login_required
@require_http_methods(["DELETE"])
def deleteWorkHistory(request, resume_id, empl_id):
    
    logger.debug("Delete Work History")
    
    if hasResumeCRUDPriv(request, resume_id):
        
        employers=Employment.objects.filter(resume__pk=resume_id)
        e = get_object_or_404(Employment, pk=empl_id)
        
        if e in employers:
            logger.debug('Deleting work history '+str(e.pk))
            e.delete()
            return HttpResponse("OK")
            #logger.debug('Redirecting to profile')
            #return HttpResponseRedirect(reverse_lazy('profile'))        
          
    response=HttpResponse()
    response.write("You are not authorized to make this change")
    response.status_code=401
    logger.debug('Returning a 401 unauthorized')
    return response

@login_required
@require_http_methods(["POST"])
def createSkill(request, resume_id):
    
    if hasResumeCRUDPriv(request, resume_id):
        
        r = get_object_or_404(Resume, pk=resume_id)
        s = Skill()
        s.resume=r
        s.skill=request.POST["skill"]
        s.save()
        
        response = serializers.serialize("json", [s])
        return HttpResponse(response, mimetype='application/json')

    else:
        
        response=HttpResponse()
        response.write("You are not authorized to make this change")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response
    
@login_required
@require_http_methods(["DELETE"])
def deleteSkill(request, resume_id, skill_id):
    
    logger.debug("Delete Skill")
    
    if hasResumeCRUDPriv(request, resume_id):
        
        skills=Skill.objects.filter(resume__pk=resume_id)
        s = get_object_or_404(Skill, pk=skill_id)
        
        if s in skills:
            logger.debug('Deleting Skill '+str(s.pk))
            s.delete()
            return HttpResponse("OK")
            #logger.debug('Redirecting to profile')
            #return HttpResponseRedirect(reverse_lazy('profile'))        
          
    response=HttpResponse()
    response.write("You are not authorized to make this change")
    response.status_code=401
    logger.debug('Returning a 401 unauthorized')
    return response

    
@login_required
@require_http_methods(["POST"])
def createCert(request, resume_id):
    
    if hasResumeCRUDPriv(request, resume_id):
        
        r = get_object_or_404(Resume, pk=resume_id)
        c = Certification()
        c.resume= r
        c.name=request.POST["name"]
        c.authority=request.POST["authority"]
        c.licnumber=request.POST["licnumber"]
        c.url=request.POST["url"]
        c.expdate=request.POST["expdate"]
        c.neverexp=request.POST["neverexp"]
        c.save()
        
        response = serializers.serialize("json", [c])
        return HttpResponse(response, mimetype='application/json')

    else:
        
        response=HttpResponse()
        response.write("You are not authorized to make this change")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response

@login_required
@require_http_methods(["DELETE"])
def deleteCert(request, resume_id, cert_id):
    
    logger.debug("Delete Cert")
    
    if hasResumeCRUDPriv(request, resume_id):
        
        certs=Certification.objects.filter(resume__pk=resume_id)
        c = get_object_or_404(Certification, pk=cert_id)
        
        if c in certs:
            logger.debug('Deleting Cert '+str(c.pk))
            c.delete()
            return HttpResponse("OK")
            #logger.debug('Redirecting to profile')
            #return HttpResponseRedirect(reverse_lazy('profile'))        
          
    response=HttpResponse()
    response.write("You are not authorized to make this change")
    response.status_code=401
    logger.debug('Returning a 401 unauthorized')
    return response

    
@login_required
@require_http_methods(["POST"])
def updateResume(request, resume_id):
    
    logger.debug('updateResume called');
    
    if hasResumeCRUDPriv(request, resume_id):
        
        r = get_object_or_404(Resume, pk=resume_id)
        field_name = request.POST["fieldname"]
        field_value = request.POST["fieldval"]
    
        logger.debug('Update for fieldname='+field_name+", fieldval="+field_value)
    
        try:
            Resume._meta.get_field(field_name)
        except Resume.FieldDoesNotExist:
            logger.debug('Exception thrown: field does not exist')
            # return something to indicate the field doesn't exist
            response = 'USER_FIELD_ERROR'
            return HttpResponseServerError(response)
        
        setattr(r, field_name, field_value)
        r.save()
        
        response = serializers.serialize("json", [r])
        
        return HttpResponse(response, mimetype='application/json')
    
    else:
        
        response=HttpResponse()
        response.write("You are not authorized to make this change")
        response.status_code=401
        logger.debug('Returning a 401 unauthorized')
        return response
