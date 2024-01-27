from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from userprofile.services import edit_user_settings


@login_required()
def view_profile(request):
    return render(request, 'userprofile/profile.html')


def save_user_settings(request, user_id: int) -> HttpResponse | HttpResponseBadRequest:
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            edit_user_settings(user_id, request)
            return HttpResponse("Success!")
        else:
            return HttpResponse("Request method is not a POST")
    else:
        return HttpResponseBadRequest('Invalid request')



