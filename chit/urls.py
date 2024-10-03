from django.urls import path
from .api import *

urlpatterns = [
    path('installment/', UserInstallmentView.as_view(), name='user_installment'),
    path('user/', UserView.as_view(), name='user_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    # path('payments/', UserPaymentList.as_view(), name='user_payments'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]

