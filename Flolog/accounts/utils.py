import shortuuid

def generate_referral_code():
    return shortuuid.ShortUUID().random(length=10)