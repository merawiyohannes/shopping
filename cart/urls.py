from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/count', views.cart_count, name="cart_count"),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>', views.remove_cart_item, name='remove_cart'),
    path('cart/increaseQuantity/<int:item_id>', views.increase_quantity, name='increase_view'),
    path('cart/decreaseQuantity/<int:item_id>', views.decrease_quantity, name='decrease_view'),
    path('cart/checkOut', views.check_out, name='checkout_view'),
    path('cart/confirmCheckout/<int:order_id>', views.confirm_checkout, name='confirm_checkout'),
    path('cart/chapaView/<int:order_id>/<str:total>', views.chapa_payment, name='chapa_view'),
    path('cart/notification', views.chapa_notification, name='notification'),
    path('order/unseen/', views.unseen_orders_count, name='unseen_orders_view')
    
    
]
