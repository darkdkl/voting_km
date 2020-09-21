import json

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        voting = Voting.objects.filter(completed=False)
        leaders_voting = [['Лидеры', 'Голоса', ],
                          ['Нет активных голосований', 0]
                          ]
        if voting:
            all_data_raw = [[[f'{one_voting.name}/ {person.last_name}',
                                    person.votes.filter(voting=one_voting).count()]
                                    for person in one_voting.persons.all()]
                                    for one_voting in voting]
            leaders_voting=[max(data, key=lambda item: item[1])
                            for data in all_data_raw]
            leaders_voting.insert(0, ['Лидеры', 'Голоса', ])

        context["table_data"] = json.dumps(leaders_voting)
        return context

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
            votes,_=persona.votes.get_or_create(voting=voting)
            context.append({
               "id":persona.id,
               "first_name":persona.first_name,
               "surname":persona.surname,
               "last_name":persona.last_name,
               "photo":persona.photo.url,
               "age":persona.age,
               "bio":persona.bio,
               "votes":votes.votes_count,
                })
        if voting.completed:

            context=sorted(context, key=lambda x: x['votes'],reverse=True)
            context[0]['victory']=True
            voting.winner=f'{context[0].get("first_name")} ' \
                          f'{context[0].get("surname")} ' \
                          f'{context[0].get("last_name")}'
            voting.save()
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
        voting = persona.votings.get(name=slug)
        votes, _ = Votes.objects.get_or_create(voting=voting, persona=persona)
        if 0 < voting.early_count <= votes.votes_count :
            voting.completed = True
            voting.save()
        else:
            votes.votes_count += 1
            votes.save()
        return redirect(reverse('voting_detail', kwargs={"slug": slug}))
