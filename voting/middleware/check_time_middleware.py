from django.http import HttpResponse
from ..models import Voting
from django.utils import timezone

class CheckTimeMiddleware():

    def __init__(self,get_response):
        self._get_response = get_response

    def __call__(self, request):
        now=timezone.now()
        votings=Voting.objects.filter(completed=False)
        for vote in votings:
            if now >= vote.date_finish:
                vote.completed=True
                vote.save()
        response = self._get_response(request)
        return response