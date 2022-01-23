from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import product, Category



def all_products(request):
    """ A view to show all products, including sorting and search queries """

    Product = product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                Product = Product.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            Product = Product.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            Product = Product.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('Product'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            Product = Product.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': Product,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """A view to show individual product details """

    productsss = get_object_or_404(product, pk=product_id)

    context = {
        'product': productsss,
    }

    return render(request, 'products/product_detail.html', context)