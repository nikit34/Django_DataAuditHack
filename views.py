from django.shortcuts import render

# Create your views here.

from .models import Company, Owner, CompanyInstance, Genre

from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    num_companys = Company.objects.all().count()
    num_instances = CompanyInstance.objects.all().count()
    num_instances_available = CompanyInstance.objects.filter(status__exact='a').count()
    num_owners = Owner.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'index.html', context={
        'num_companys': num_companys,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_owners':num_owners,
        'num_visits': num_visits},
    )


from django.views import generic


class CompanyListView(generic.ListView):
    model = Company
    paginate_by = 5


class CompanyDetailView(generic.DetailView):
    model = Company


from django.contrib.auth.mixins import LoginRequiredMixin


class CompanyListView(generic.ListView):
    model = Company
    paginate_by = 5


class CompanyDetailView(generic.DetailView):
    model = Company


class OwnerListView(generic.ListView):
    model = Owner
    paginate_by = 5


class OwnerDetailView(generic.DetailView):
    model = Owner


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedCompanysByUserListView(LoginRequiredMixin, generic.ListView):
    model = CompanyInstance
    template_name = 'catalog/companyinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return CompanyInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedCompanysAllListView(PermissionRequiredMixin, generic.ListView):
    model = CompanyInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/companyinstance_list_borrowed_all.html'
    paginate_by = 5

    def get_queryset(self):
        return CompanyInstance.objects.filter(status__exact='o').order_by('due_back')


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required
from .forms import RenewCompanyForm


@permission_required('catalog.can_mark_returned')
def renew_company_librarian(request, pk):
    company_instance = get_object_or_404(CompanyInstance, pk=pk)

    if request.method == 'POST':
        form = RenewCompanyForm(request.POST)
        if form.is_valid():
            company_instance.due_back = form.cleaned_data['renewal_date']
            company_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewCompanyForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'company_instance': company_instance,
    }

    return render(request, 'catalog/company_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Owner


class OwnerCreate(PermissionRequiredMixin, CreateView):
    model = Owner
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    permission_required = 'catalog.can_mark_returned'


class OwnerUpdate(PermissionRequiredMixin, UpdateView):
    model = Owner
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class OwnerDelete(PermissionRequiredMixin, DeleteView):
    model = Owner
    success_url = reverse_lazy('owners')
    permission_required = 'catalog.can_mark_returned'


class CompanyCreate(PermissionRequiredMixin, CreateView):
    model = Company
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class CompanyUpdate(PermissionRequiredMixin, UpdateView):
    model = Company
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class CompanyDelete(PermissionRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('companys')
    permission_required = 'catalog.can_mark_returned'


def graph(request):
    datasplit = ChartData()
    id_company = []
    numbers_company = []
    for i in range(len(datasplit.get(request).data)):
        id_company.append(datasplit.get(request).data[i][0])
        numbers_company.append(datasplit.get(request).data[i][1])
    dict_data = {'id': id_company, 'num': numbers_company}
    return render(request, 'graph.html', context=dict_data)

class ChartData(APIView):
    def get(self, request, format=None):
        articles = dict()
        # i = 0
        for company in Company.objects.all():
            articles[company.title] = company.numbers
            # i += 1

        articles = sorted(articles.items(), key=lambda x: x[1])
        return Response(articles)
