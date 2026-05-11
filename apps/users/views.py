from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username  = request.data.get('username')
        email     = request.data.get('email')
        password  = request.data.get('password')
        password2 = request.data.get('password2')
        role      = request.data.get('role', 'buyer')

        if not username or not email or not password:
            return Response(
                {"error": "All fields required"},
                status=status.HTTP_400_BAD_REQUEST)

        if password != password2:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username = username,
            email    = email,
            password = password,
            role     = role
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access' : str(refresh.access_token),
            'refresh': str(refresh),
            'user'   : {
                'id'      : user.id,
                'username': user.username,
                'email'   : user.email,
                'role'    : user.role,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email    = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response(
                {"error": "Email and password required"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED)

        if not user_obj.check_password(password):
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED)

        if not user_obj.is_active:
            return Response(
                {"error": "Account is disabled"},
                status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user_obj)
        return Response({
            'access' : str(refresh.access_token),
            'refresh': str(refresh),
            'user'   : {
                'id'      : user_obj.id,
                'username': user_obj.username,
                'email'   : user_obj.email,
                'role'    : user_obj.role,
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Logged out successfully.'},
                status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(
                {'error': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class   = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class BecomeSellerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role == 'seller':
            return Response(
                {'message': 'Already a seller', 'role': 'seller'},
                status=status.HTTP_200_OK)

        # set role to seller
        user.role = 'seller'
        user.save()

        # create SellerProfile if not exists — THIS IS THE KEY FIX
        from apps.products.models import SellerProfile
        shop_name = request.data.get('shop_name', user.username + "'s Shop")

        seller_profile, created = SellerProfile.objects.get_or_create(
            user=user,
            defaults={'shop_name': shop_name}
        )

        # if already exists but shop_name was sent, update it
        if not created and request.data.get('shop_name'):
            seller_profile.shop_name = shop_name
            seller_profile.save()

        return Response({
            'message'  : 'You are now a seller!',
            'role'     : user.role,
            'shop_name': seller_profile.shop_name,
        }, status=status.HTTP_200_OK)
