from django.urls import path
from .views import *


urlpatterns = [
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-requests/send/', FriendRequestCreateView.as_view(), name='friend-request-send'),
    path('friend-requests/accept/<int:pk>/', FriendRequestAcceptView.as_view(), name='friend-request-accept'),
    path('friend-requests/reject/<int:pk>/', FriendRequestRejectView.as_view(), name='friend-request-reject'),
    path('friend-requests/accepted/', AcceptedFriendRequestListView.as_view(), name='pending-friend-requests'),
    path('friend-requests/pending/', PendingFriendRequestListView.as_view(), name='pending-friend-requests'),
]