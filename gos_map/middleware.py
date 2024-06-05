from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('user_id') and request.path != '/login/':
            return redirect('login')
        response = self.get_response(request)
        return response
