from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from decimal import Decimal
from django.contrib.auth import update_session_auth_hash





class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Set the new password
            pass1 = serializer.validated_data['password']
            pass2 = serializer.validated_data['conf_password']
            if pass1 != pass2:
                return Response({"error":"password does not match!"})
            user.set_password(serializer.validated_data['password'])
            # user.needs_password_change = False  # Mark that password has been changed
            user.save()

            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class UserInstallmentView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.select_related('chit_plan').get(id=request.user.id)
        chit_plan = user.chit_plan
        
        if not chit_plan:
            return Response({"error": "No chit plan assigned."}, status=status.HTTP_400_BAD_REQUEST)

        installment_amount = chit_plan.plan
        payment = Decimal(request.data.get('payment', 0))  # Convert payment to Decimal

        if payment <= 0:
            return Response({"error": "Payment amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total due amount (missed months + pending amount)
        total_due = user.missed_months * installment_amount + user.pending_amount
        remaining_payment = total_due - payment  # Both are now Decimal

        # Prevent overpayment
        if remaining_payment < 0:
            return Response({"error": "Overpayment is not allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # If payment covers all missed months
        if remaining_payment == 0:
            user.months_paid += user.missed_months
            user.missed_months = 0
            user.pending_amount = 0
        # If payment covers more than one month
        elif payment >= installment_amount:
            months_covered = payment // installment_amount
            user.months_paid += int(months_covered)
            user.pending_amount = payment % installment_amount
        # Partial payment
        else:
            user.pending_amount += payment

        # Update total amounts
        user.total_amount_paid += payment
        user.total_pending_amount = remaining_payment
        user.save()

        return Response({"message": "Installment payment processed successfully."}, status=status.HTTP_200_OK)


class UserView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Apply select_related to optimize chit_plan retrieval
        user = User.objects.select_related('chit_plan').get(id=request.user.id)
        user_serializer = UserSerializer(user).data
        return Response(user_serializer, status=status.HTTP_200_OK)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user_obj = authenticate(username=username, password=password)
        if user_obj:
            token, _ = Token.objects.get_or_create(user=user_obj)
            return Response({"message": "Login successful", "username": username, "token": str(token)}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


# class PaymentPagination(PageNumberPagination):
#     page_size = 10


# class UserPaymentList(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     pagination_class = PaymentPagination

#     def get(self, request):
#         payments = Payment.objects.filter(user=request.user).order_by('installment_number')
#         paginator = PaymentPagination()
#         result_page = paginator.paginate_queryset(payments, request)
#         serializer = PaymentSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

