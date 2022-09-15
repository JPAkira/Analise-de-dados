from rest_framework.views import APIView
from datamanager.models import AppleStore
from django.http import HttpResponse

class Top10CitacoesAPI(APIView):
    def get(self, request):
        applestore = AppleStore.objects.filter(prime_genre__in=["Music", "Book"]).order_by('-n_citacoes')[:10]
        for citacao in applestore:
            citacao.n_citacoes += 1
            citacao.save()
        return HttpResponse(applestore.values(), content_type="application/json")