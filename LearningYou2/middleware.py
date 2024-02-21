"""middleware Users profiles """
# Django
"""
from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    Pofile completecion middleware
    
    This make usensure that the theacher and 
    student have to complete the profile 
    
    def __init__(self, get_response):
        Middleware initialization.
        self.get_response = get_response

    def __call__(self, request):
        Code to be executed for each request before the view is called.
        if not request.user.is_anonymous:
            if not request.user.is_staff or request.user.is_Estudiante:
                profile = request.user.profile
                if not profile.picture or not profile.biography:
                    if request.path not in [reverse('update_profile'), reverse('logout')]:
                        return redirect('update_profile')

        response = self.get_response(request)
        return response   """