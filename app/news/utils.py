from django.shortcuts import redirect
from django.contrib import messages

class MyMixin(object):
    mixin_prop = ''

    def get_cookie_pands_self(self, s):
        if s.request.COOKIES.get('AuthPanda') == None or s.request.COOKIES.get('AuthPanda') == 'False':
            return 'redir'
        else:
            getLogCookies = {
                'auth': s.request.COOKIES.get('AuthPanda'), 
                'name': s.request.COOKIES.get('NamePanda')
            }
            return getLogCookies

    def save_in_view(self, s, f, message, redir):
        s.object = f.save()
        messages.success(s.request, message)
        return redirect(redir)