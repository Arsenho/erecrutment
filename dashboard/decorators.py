import functools
from functools import wraps

from rest_framework import status, generics
from rest_framework.response import Response

from joboffer.models import Offer


def check_offer_id(view_function):
    @wraps(view_function)
    def _wrapped(self, request, *args, **kwargs):
        if 'offer_id' in request.GET:
            print("id_offer ok")
            try:
                offer_id = int(request.GET['offer_id'])
                offer = Offer.objects.get(id=offer_id)
                # print(offer.applicants.all())
                kwargs['offer'] = offer
                return view_function(self, request, *args, **kwargs)
            except ValueError:
                return Response(
                    data={'message': "offer id must be an integer"},
                    status=status.HTTP_404_NOT_FOUND
                )
                # print("l'id d'une offre doit etre un entier")
            except Offer.DoesNotExist:
                return Response(
                    data={'message': "Cette offre n'existe pas !"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                data={'message': "Aucun paramettre <<offer_id>> recu !"},
                status=status.HTTP_404_NOT_FOUND
            )
    return _wrapped
