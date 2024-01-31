from django.urls import path
from .views import index, save_marksheet, fetch_marksheets, RegisterUser, GetStudents, displaystudentdatapage
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', index, name='index'), # Home page
    path('save_marksheet/', save_marksheet, name='save_marksheet'),  # Save marksheet data
    path('fetch_marksheets/', fetch_marksheets, name='fetch_marksheets'),  # Fetch marksheet data for display
    path('student_table/', displaystudentdatapage, name='display_table'),  # Display student data table page
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint for JWT authentication
    
    path('registeruser/', RegisterUser.as_view(), name='register-user'),  # Register user endpoint
    path('getstudents/', GetStudents.as_view(), name='get-students'),  # Get list of students endpoint
]
