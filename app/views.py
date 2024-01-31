from django.shortcuts import render
from .forms import MarkSheetForm
from .models import MarkSheet
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import Response
from .serializer import StudentSerializer, dynamic_serializer
from rest_framework.permissions import IsAuthenticated

# Render the index page with an empty MarkSheetForm
def index(request):
    marksheet_form = MarkSheetForm()
    return render(request, 'index.html', {'marksheet_form': marksheet_form})

# Render the page for displaying student data
def displaystudentdatapage(request):
    return render(request, 'studentdata.html')

# Save marksheet data submitted through a form
def save_marksheet(request):
    if request.method == 'POST':
        form = MarkSheetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Mark sheet saved successfully.'})
        else:
            return JsonResponse({'message': 'Error in form submission.'}, status=400)
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

# Fetch and return paginated marksheet data for DataTables
def fetch_marksheets(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')

    columns = ['student_name', 'roll_no', 'subject1_score', 'subject2_score', 'subject3_score', 'subject4_score', 'subject5_score', 'student_class']

    order_by = columns[order_column]
    if order_dir == 'desc':
        order_by = '-' + order_by
    marksheets = MarkSheet.objects.all().order_by(order_by)[start:start + length]
    total_records = MarkSheet.objects.all().count()

    data = [{'student_name': sheet.student_name,
             'roll_no': sheet.roll_no,
             'subject1_score': sheet.subject1_score,
             'subject2_score': sheet.subject2_score,
             'subject3_score': sheet.subject3_score,
             'subject4_score': sheet.subject4_score,
             'subject5_score': sheet.subject5_score,
             'student_class': sheet.student_class} for sheet in marksheets]

    response_data = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data,
    }

    return JsonResponse(response_data)

# API view for user registration
class RegisterUser(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User(username = username)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'status' : "success",
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        })

# API view for fetching student data
class GetStudents(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            class_filter = request.query_params.get('class', None)
            data_selection = request.query_params.get('data', None)

            if class_filter:
                student_details = MarkSheet.objects.filter(student_class=class_filter)
                serializer = StudentSerializer(student_details, many=True)
                return Response({'status': 'success', 'data': serializer.data})

            if data_selection:
                students = MarkSheet.objects.all()
                data = data_selection.split(',')
                all_fields = []
                for i in data:
                    if i == 'name':
                        all_fields.append('student_name')
                    if i == 'roll':
                        all_fields.append('roll_no')
                    if i == 'score total':
                        all_fields.append('total_marks')
                    if i == 'class':
                        all_fields.append('student_class')

                DynamicSerializer = dynamic_serializer(all_fields)
                serializer = DynamicSerializer(students, many=True)
                return Response({'status': 'success', 'data': serializer.data})
            
            students = MarkSheet.objects.all().order_by('-total_marks')
            serializer = StudentSerializer(students, many=True)
            return Response({'data': serializer.data})

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)})