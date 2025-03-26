from django.shortcuts import render
from item.models import Item, Category
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def detail_view(request, pk):
    item = Item.objects.get(pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)
    context = {
        "item":item,
        "related_items":related_items
    }

    return render(request, 'core/detail.html', context)


def home_view(request):
    month = datetime.now().strftime("%B")
    to_day = datetime.now().strftime("%d")
    to_day = int(to_day)
    dates = [to_day, to_day - 1, to_day - 2]
    new_items = []
    print(request.user)
    
    
    items = Item.objects.filter(is_sold=False).order_by("-created_at")
    for item in items:
        if item.created_at.strftime("%B") == month and int(item.created_at.strftime("%d")) in dates:
            new_items.append(item)
    paginator = Paginator(items, 8)
    page_number = request.GET.get("page")
    page_items = paginator.get_page(page_number)
    
    context = {
        "items":items,
        "new_items":new_items,
        "page_items":page_items,
        }
    return render(request, 'core/home.html', context)
