from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Список исключений
        excluded_paths = [
            reverse('login'),  # путь к странице логина
            '/admin/',         # путь к админке
        ]

        # Проверка, находится ли текущий путь в списке исключений
        if not request.session.get('user_id') and not any(request.path.startswith(path) for path in excluded_paths):
            return redirect('login')

        response = self.get_response(request)
        return response
