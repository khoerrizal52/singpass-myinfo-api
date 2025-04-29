from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from myinfo.client import MyInfoPersonalClientV4
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def singpass_auth(request):
    user = request.user
    oauth_state = get_random_string(length=16)
    # Save the oauth_state to user
    user.oauth_state = oauth_state
    user.save(update_fields=['oauth_state'])

    callback_url = settings.FRONTEND_CALLBACK_URL

    client = MyInfoPersonalClientV4()
    res = client.get_authorise_url(oauth_state, callback_url)

    return Response({"url-redirect": res})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def singpass_auth_callback(request):
    auth_code = request.query_params.get('code')

    if not auth_code:
        return Response(
            {"error": "Authorization code not provided."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user  # Securely retrieved authenticated user
    oauth_state = getattr(user, 'oauth_state', None)

    callback_url = settings.FRONTEND_CALLBACK_URL
    person_data = MyInfoPersonalClientV4().retrieve_resource(auth_code, oauth_state, callback_url)
    return Response({"person_data": person_data})
