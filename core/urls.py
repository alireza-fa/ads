from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    path('accounts/register/company/', views.UserCompanyCreateView.as_view(), name='register-company'),
    path('accounts/register/influ/', views.UserInfluCreateView.as_view(), name='register-influ'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    #
    path('influ/', views.InfluListView.as_view(), name='influ-list'),
    #
    path('contact/create/', views.ContactView.as_view(), name='contact-create'),
    path('contact_us/create/', views.ContactUsCreateView.as_view(), name='contact-us-create'),
    #
    path('payment/<int:influ_id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('payment/buy/<int:influ_id>/', views.PaymentBuyView.as_view(), name='payment-buy'),
    #
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
