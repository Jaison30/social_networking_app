from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache


class FriendRequestRateThrottle(SimpleRateThrottle):
    rate = '3/minute'  # Set the desired rate limit

    def get_cache_key(self, request, view):
        return view.__class__.__name__
