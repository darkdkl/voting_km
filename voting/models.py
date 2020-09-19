from django.db import models
from django.urls import reverse

class Voting(models.Model):
    name = models.CharField(max_length=255,verbose_name="Название")
    date_start = models.DateTimeField(verbose_name="Дата начала")
    date_finish = models.DateTimeField(verbose_name="Дата завершения")
    early_count = models.IntegerField(default=0,verbose_name="Голоса для для победы")
    completed=models.BooleanField(default=False,verbose_name="Завершено")
    persons = models.ManyToManyField('Persona', related_name='votings')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Голосование"
        verbose_name_plural = "Голосования"

    def get_absolute_url(self):
        return reverse('voting_detail', kwargs={"slug": self.name})


class Votes(models.Model):
    voting = models.ForeignKey(Voting,on_delete=models.CASCADE)
    persona = models.ForeignKey("Persona",related_name="votes",
                                on_delete=models.CASCADE)


class Persona(models.Model):
    first_name = models.CharField(max_length=155,verbose_name="Имя")
    surname = models.CharField(max_length=155,verbose_name="Отчество")
    last_name = models.CharField(max_length=155,verbose_name="Фамилия")
    photo = models.ImageField(verbose_name="Фотография")
    age = models.IntegerField(verbose_name="Возраст")
    bio = models.TextField(verbose_name="Биография")

    def __str__(self):
        return f"{self.first_name} {self.surname} {self.last_name}"

    class Meta:
        verbose_name="Кандидат"
        verbose_name_plural = "Кандидаты"
