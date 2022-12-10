from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def update_count(self):
        Product.objects.filter(id=self.object.product.id).update(count=self.object.product.count-1)

    def form_valid(self, form):
        self.object = form.save()
        prods = Product.objects.get(id=self.object.product.id)
        if (prods.count) <= 0:
            return HttpResponse(f'Ошибка: товаров больше не осталось! <a href="/">Главная</a>')
        else:
            PurchaseCreate.update_count(self)
            return HttpResponse(f'Спасибо за покупку! <a href="/">Главная</a>')