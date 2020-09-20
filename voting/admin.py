from django.contrib import admin
from django.utils.safestring import mark_safe

from .middleware.current_user import get_current_user
from .models import Voting, Persona
from .tasks import make_report
from django import forms


class VotingAdminForm(forms.ModelForm):
    def clean(self):
        super().clean()
        if self.data.get('_orderbutton'):
            make_report.delay(self.instance.id, get_current_user())


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    form = VotingAdminForm
    change_form_template = "add_button.html"

    list_display = ('name', 'date_start', 'date_finish', 'early_count',
                    'completed')
    readonly_fields = ['winner']


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    readonly_fields = ['photo_preview']

    def photo_preview(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width=200 height=200 />')
