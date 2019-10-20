from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .models import DashCompany

def company_article_list(request):
    return render(request, 'finance/plotly.html', {})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        articles = dict()
        for company in DashCompany.objects.all():
            if company.articles > 0:
                articles[company.name] = company.articles

        articles = sorted(articles.items(), key=lambda x: x[1])
        articles = dict(articles)

        data = {
            "article_labels": articles.keys(),
            "article_data": articles.values(),
        }
        return Response(data)
