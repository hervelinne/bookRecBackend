from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        # Set the user ID in the payload using the correct field name
        token.payload[api_settings.USER_ID_CLAIM] = str(user._id)

        return token

    def get_user_id(self):
        return str(self.payload.get(api_settings.USER_ID_CLAIM, ''))

    def verify(self):
        super().verify()

        if api_settings.USER_ID_CLAIM not in self.payload:
            raise ValueError(_('Token has no user_id claim'))

        # Handle the case where jti_hex might be None
        if self.payload['jti_hex'] is None:
            self.payload['jti_hex'] = generate_unique_jti_hex()

def generate_unique_jti_hex():
    # Implement a function to generate a unique jti_hex
    # This can involve using a library or creating a unique string based on some criteria
    pass
