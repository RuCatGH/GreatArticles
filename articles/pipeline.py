from userprofile.models import CustomUser


def get_account_info(backend, strategy, details, response,
                     user=None, *args, **kwargs):
    url, name, email = None, None, None
    if backend.name == 'google-oauth2':
        name = response['name']
        url = response['picture']
        email = response['email']
        # ext = url.split('.')[-1]
    if backend.name == 'vk-oauth2':
        name = response['first_name'] + ' ' + response['last_name']
        url = response['user_photo']
        email = response['email']
    if url:
        if not CustomUser.objects.filter(avatar=url).exists():
            user.avatar = url
            user.nickname = name
            user.email = email
            user.save()
