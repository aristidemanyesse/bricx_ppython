from django.contrib.auth import authenticate, login

def verify_password(request, password):
    user = authenticate(request, username=request.user.username, password=password)
    return user is not None