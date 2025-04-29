from rest_framework.decorators import api_view
from rest_framework.response import Response
from myinfo.client import MyInfoPersonalClientV4
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework import status

@api_view(['GET'])
def singpass_auth(request):
    oauth_state = get_random_string(length=16)
    callback_url = settings.FRONTEND_CALLBACK_URL

    client = MyInfoPersonalClientV4()
    res = client.get_authorise_url(oauth_state, callback_url)

    return Response({"url-redirect": res, "oauth_state": oauth_state})

@api_view(['GET'])
def singpass_auth_callback(request):
    auth_code = request.query_params.get('code')
    oauth_state = request.query_params.get('oauth_state')

    if not auth_code:
        return Response(
            {"error": "Authorization code not provided."},
            status=status.HTTP_400_BAD_REQUEST
        )
    callback_url = settings.FRONTEND_CALLBACK_URL
    person_data = MyInfoPersonalClientV4().retrieve_resource(auth_code, oauth_state, callback_url)
    return Response({"person_data": person_data})
