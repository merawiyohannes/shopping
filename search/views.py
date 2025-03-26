from django.shortcuts import render
from item.models import Item, Category
from django.core.paginator import Paginator

def search_view(request):
    filter_by = request.GET.get('filter')
    search_query = request.GET.get('search')
    
    items = Item.objects.filter(is_sold=False)
    
    if search_query:
        if filter_by == "category":
            items = items.filter(category__name__icontains=search_query)
        elif filter_by == 'item_name':
            items = items.filter(name__icontains=search_query)
        elif filter_by == 'max_price_range':
            try:
                max_price = int(search_query)
                items = items.filter(price__lte=max_price)
            except ValueError:
                items = Item.objects.none()
                
    paginator = Paginator(items, 4)
    page_number = request.GET.get('page')
    page_items = paginator.get_page(page_number)
    
    
    context = {
        "items":items,
        "value":search_query,
        'page_items':page_items
    }
    
    
    return render(request, "search/search.html", context)