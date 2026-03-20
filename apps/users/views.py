from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(request.data)  # 🔥 DEBUG (keep this for now)

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            return Response({"error": "User not found"})

        user = authenticate(username=username, password=password)

        if user:
            return Response({"status": "success"})
        else:
            return Response({"error": "Wrong password"})