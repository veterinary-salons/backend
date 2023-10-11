from rest_framework_simplejwt.tokens import AccessToken

from core.constants import Limits


class RecoveryAccessToken(AccessToken):
    lifetime = Limits.RECOVERY_ACCESS_TOKEN_LIFETIME