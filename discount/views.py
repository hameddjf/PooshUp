from django.views.generic import ListView, DetailView
from .models import Discount


class DiscountListView(ListView):
    model = Discount
    template_name = 'discount/discount_list.html'
    context_object_name = 'discounts'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)


class DiscountDetailView(DetailView):
    model = Discount
    template_name = 'discount/discount_detail.html'
    context_object_name = 'discount'
