from django.urls import path
from . import views

app_name = 'Ecommerce'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('toggleactivate/<int:item_id>/',views.toggleactivate, name='toggleactivate'),
    path('edit_item/<int:item_id>/',views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('stock_summary/', views.stock_summary, name='stock_summary'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('investment/', views.investment, name='investment'),
    path('transaction_log/', views.transaction_log, name='transaction_log'),
    path('profile/', views.profile, name='profile'),
    path('mpesa_deposit/', views.mpesa_deposit, name='mpesa_deposit'),

    # path('mpesa/' ,views.getAccessToken, name='mpesa'),
    # path('mpesa/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    #
    # # register, confirmation, validation and callback urls
    # path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    # path('c2b/confirmation', views.confirmation, name="confirmation"),
    # path('c2b/validation', views.validation, name="validation"),
    # path('c2b/callback', views.call_back, name="call_back"),

]

# path('checkout/', views.CheckoutView.as_view(), name='checkout'),
# path('OrderSummary/', views.OrderSummary.as_view(), name='order_summary'),
# path('product/<slug>/', views.ProductView.as_view(), name='product'),
# path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
# path('a-s-t-t-c/<slug>/', views.add_single_item_to_cart, name='add_single_item_to_cart'),
# path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
# path('r-i-f-c/<slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
# path('payment/', views.PaymentView.as_view(), name='payment'),
