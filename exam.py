from ask.models import Profile
profiles = Profile.objects.all()
for profile in profiles:
    print(profile.user.username)