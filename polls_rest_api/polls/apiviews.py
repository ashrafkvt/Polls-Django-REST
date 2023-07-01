from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from .models import Poll, Choice
from  .serializers import PollSerializer, ChoiceSerializer, \
    VoteSerializer, UserSerializer

class PollList(generics.ListCreateAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveDestroyAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_url_kwarg = 'poll_id'

class ChoiceList(generics.ListCreateAPIView):

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    

class CreateVote(APIView):

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserCreate(generics.CreateAPIView):
    
    serializer_class = UserSerializer
