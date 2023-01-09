from celery import shared_task
from .models import StoryModel
from datetime import datetime, timedelta

@shared_task
def checkexpdate():
    expired_date = datetime.now() - timedelta(minutes=1)
    expired_stories = StoryModel.objects.filter(posted__lt=expired_date)#lt less than or equal
    expired_stories.update(expired=True)
    expired_stories.save()
    print("Updated")

@shared_task
def deleteexpiredstories():
    StoryModel.objects.filter(expired=True).delete()