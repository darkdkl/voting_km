from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from .models import Voting,Votes,Persona
from django.utils import timezone



class ActiveVotingView(ListView):
    template_name = 'voting/index.html'
    def get_queryset(self):
        queryset=Voting.objects.filter(completed=False)
        return queryset

class CompleteVotingView(ListView):
    template_name = 'voting/complete.html'
    def get_queryset(self):
        queryset=Voting.objects.filter(completed=True)
        return queryset


def voting_detail(request, slug):
    if request.method == 'GET':
        voting=Voting.objects.get(name=slug)
        persons=voting.persons.all()
        context=[]
        for persona in persons:
           context.append({
               "id":persona.id,
               "first_name":persona.first_name,
               "surname":persona.surname,
               "last_name":persona.last_name,
               "photo":persona.photo.url,
               "age":persona.age,
               "bio":persona.bio,
               "votes":persona.votes.filter(voting=voting).count(),
                })
        if voting.completed:
            context=sorted(context, key=lambda x: x['votes'],reverse=True)
            context[0]['victory']=True
        timl=voting.date_finish-timezone.now()
        ds, hs, min = timl.days, timl.seconds // 3600, timl.seconds // 60 % 60
        return render(request,
                      'voting/voting.html', {
                              "context":context,
                              "voting_completed":voting.completed,
                              "time_lost":f"Дней:{ds},Часов:{hs},Минут:{min}"})

    if request.method == 'POST':
        persona_id = request.POST.get("pers_id")
        persona=Persona.objects.get(id=persona_id)
        slug =(lambda path:path.split('/')[-1])(request.path)
        voting = Voting.objects.get(name=slug)
        count_votes=persona.votes.filter(voting=voting).count()
        if 0 < voting.early_count <= count_votes:
            voting.completed=True
            voting.save()
        else:
            Votes.objects.create(voting=voting,persona=persona)
        return redirect(reverse('voting_detail', kwargs={"slug": slug}))
