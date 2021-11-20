from accounts.models import UserProfile

def add_variable_to_context(request):
    ''' Makes profile a global variable so I can access avatars from nav '''
    if request.user.is_authenticated:
        user = request.user
        profile = UserProfile.objects.get(pk=user.pk)
        return {
            'profile': profile,
        }
    return {}
