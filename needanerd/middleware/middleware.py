from django.conf import settings
from django import http
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.core.urlresolvers import RegexURLResolver
import logging
import sys

logger = logging.getLogger('NeedANerd.custom')


class NerdSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    

    def resolver(self, request):
        """
        Returns a RegexURLResolver for the request's urlconf.
    
        If the request does not have a urlconf object, then the default of
        settings.ROOT_URLCONF is used.
        """
        urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
        return RegexURLResolver(r'^/', urlconf)

    def process_exception(self, request, exception):
        # Get the exception info now, in case another exception is thrown later.
        if isinstance(exception, http.Http404):
            logger.debug('processing exception throwing a 404')
            return self.handle_404(request, exception)
        else:
            logger.debug('processing exception throwing a 500')
            return self.handle_500(request, exception)


    def handle_404(self, request, exception):
        if settings.DEBUG:
            logger.debug('DEBUG=true')
            from django.views import debug
            return debug.technical_404_response(request, exception)
        else:
            logger.debug('DEBUG=false')
            callback, param_dict = self.resolver(request).resolve404()
            return callback(request, **param_dict)


    def handle_500(self, request, exception):
        exc_info = sys.exc_info()
        if settings.DEBUG:
            logger.debug('DEBUG=true')
            return self.debug_500_response(request, exception, exc_info)
        else:
            logger.debug('DEBUG=false')
            self.log_exception(request, exception, exc_info)
            return self.production_500_response(request, exception, exc_info)


    def debug_500_response(self, request, exception, exc_info):
        from django.views import debug
        return debug.technical_500_response(request, *exc_info)
    

    def production_500_response(self, request, exception, exc_info):
        '''Return an HttpResponse that displays a friendly error message.'''
        callback, param_dict = self.resolver(request).resolve500()
        return callback(request, **param_dict)
