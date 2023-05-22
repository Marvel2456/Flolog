import shortuuid
from .models import Activity

def generate_referral_code():
    return shortuuid.ShortUUID().random(length=10)


def log_activity(user, action):
    activity = Activity(user=user, action=action)
    activity.save()