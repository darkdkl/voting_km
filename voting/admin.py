from django.contrib import admin
from django.utils.safestring import mark_safe
from .middleware.current_user import get_current_user
from .models import Voting,Persona
# Register your models here.

admin.site.register(Persona)

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):

    def export_to_xls(self, obj):
        print(obj.id)
        print(get_current_user())
        return mark_safe('<button>XLS</button>')

    list_display = ('name', 'date_start', 'date_finish', 'early_count',
                    'completed',"export_to_xls")