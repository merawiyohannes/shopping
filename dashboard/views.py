from django.shortcuts import HttpResponse,render, get_object_or_404
from cart.models import CheckOutOrder, CheckOutItem
from item.models import Item
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def make_orders_seen(request):
    updated = CheckOutOrder.objects.filter(is_seen=False).update(is_seen=True)
    return HttpResponse(f"{updated} orders updated to seen")

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        paid_orders = CheckOutOrder.objects.filter(is_paid=True)
        all_orders = CheckOutOrder.objects.filter(is_seen=True)
        new_orders = CheckOutOrder.objects.filter(is_paid=True, is_seen=False)
    else:
        paid_orders = CheckOutOrder.objects.filter(created_by=request.user, is_paid=True)
        all_orders = CheckOutOrder.objects.filter(created_by=request.user)
        new_orders = None
    active_users = User.objects.filter(is_active=True)
    context = {
        'paid_orders':paid_orders,
        'all_orders':all_orders,
        'active_users':active_users,
        'new_orders':new_orders
        
    }
    return render(request, 'dashboard/dashboard.html', context)
    