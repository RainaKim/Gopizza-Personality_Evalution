from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.id) + text_type(timestamp)) 

user_activation_token = UserActivationTokenGenerator()
