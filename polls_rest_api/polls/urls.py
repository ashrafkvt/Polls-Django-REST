from django.urls import path
from .apiviews import PollList, PollDetail,\
      ChoiceList, CreateVote, UserCreate

urlpatterns = [
    path("polls/", PollList.as_view(), name="polls_list"),
    path("polls/<int:poll_id>/", PollDetail.as_view(), name="polls_detail"),
    path("polls/<int:pk>/choices", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
]