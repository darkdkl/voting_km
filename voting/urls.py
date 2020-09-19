from django.urls import path
from . import views

urlpatterns = [
    path("", views.ActiveVotingView.as_view(),name="active_voting"),
    path("votes/complete", views.CompleteVotingView.as_view(),name="voting_complete"),
    path("votes/<str:slug>", views.voting_detail,name="voting_detail"),
]