from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("AUTH backend called with:", email, password)
        try:
            user = UserModel.objects.get(email=email)
            print("User found:", user.email)
        except UserModel.DoesNotExist:
            print("No user with email")
            return None

        if user.check_password(password):
            print("Password match")
        else:
            print("Password mismatch")

        if self.user_can_authenticate(user):
            print("User can authenticate")
            return user
        else:
            print("User cannot authenticate (inactive?)")
            return None