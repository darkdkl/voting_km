from votings_km.celery import app
from .models import Voting
from .service import send,make_xls

@app.task
def make_report(obj_id,user_email):
    voting=Voting.objects.get(id=obj_id)
    filename=make_xls(voting.get_winners,voting.name)
    send(user_email,filename,voting.name)



