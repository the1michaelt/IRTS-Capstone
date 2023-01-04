from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .serializers import MyTokenObtainPairSerializer, RegistrationSerializer, PersonObjectSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from student_courses.serializers import StudentCourseSerializer
from courses.serializers import CourseSerializer
from courses.serializers import CourseSerializer
from student_courses.models import StudentCourse, User
from courses.models import Course
from .models import User
User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def directory_of_students(request):
    """/api/auth/student_directory/  These are students with classes. GET users with courses
    """
    students = User.objects.all().filter(is_student=True)
    serializer = PersonObjectSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def grad_ready_candidates(request):
    """/api/auth/candidates/  students to be filtered by credits_received >=128 && gpa >=3
    """
    candidates = User.objects.filter(grad_ready=True)
    serializer = PersonObjectSerializer(candidates, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])   
def put_individual_graduation_eligibility(request, user_id):
    """api/auth/individual_graduation_eligibility/
    UPDATES grad_ready, GPA, semester, credits_earned
    """   
    student_object = User.objects.get(id=user_id)

    graded_courses = StudentCourse.objects.filter(user_id=user_id).exclude(grade_received=0)
    sum_of_grades = 0
    for grade in graded_courses:
        sum_of_grades += grade.grade_received
    gpa = sum_of_grades/len(graded_courses)

    passed_courses = StudentCourse.objects.filter(user_id=user_id).exclude(credits_received=0)
    sum_of_credits = 0
    for passed_course in passed_courses:
        sum_of_credits += passed_course.credits_received
        semester=(sum_of_credits//16)+1

    student_object.semester = semester
    student_object.credits_earned = sum_of_credits
    student_object.gpa = gpa   
    
    if (sum_of_credits >= 128 and gpa >= 3):
        student_object.grad_ready = True
        print('student_gpa', gpa)
        print('TRUE (4) sum_of_credits', sum_of_credits)
        print('TRUE (4) is grad_ready', student_object.grad_ready)

    else:
        student_object.grad_ready = False
        print('student_gpa', gpa)
        print('ELSE (0) sum_of_credits', sum_of_credits)
        print('ELSE (0) is grad ready', student_object.grad_ready)
        print('student object', student_object)
        print('student object #', student_object.id)
        print('ELSE (0) is student', student_object.is_student)

    student_object.grad_ready
    student_object.save()

    serializer = PersonObjectSerializer(student_object)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def put_calculate_semester_by_credits(request, user_id):
    """api/auth/put_calculate_semester_by_credits/<int:user_id>/

    PUT into AUTH/USER semester
    """    
    student_object = User.objects.get(id=user_id)

    passed_courses = StudentCourse.objects.filter(user_id=user_id).exclude(credits_received=0)
    sum_of_credits = 0
    semester = 0
    for passed_course in passed_courses:
        sum_of_credits += passed_course.credits_received
        semester=(sum_of_credits//16)+1

    student_object.semester = semester


    try:
        serializer = PersonObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(semester=semester)
        print('users_courses', passed_courses)
        print('sum_of_credits', sum_of_credits)
        print('POST INTO SEMESTER: current_semester', semester)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        print('EXCEPT users_courses', passed_courses)
        print('EXCEPT sum_of_credits', sum_of_credits)
        print('EXCEPT POST INTO SEMESTER: current_semester', semester)
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])  
def sum_credits_earned(request, user_id):
    """api/auth/sum_credits_earned/
    """   
    student_object = User.objects.get(id=user_id)

    credits_accumulated = get_object_or_404(User, pk=user_id)
    credits_accumulated.credits_earned=request.data['credits_earned']
    try:
        serializer = PersonObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student_object.credits_earned)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])   
def gpa_earned(request, user_id):
    """api/auth/put_gpa/<int:user_id>/', #stores GPA to DB
    """   
    calculated_gpa = get_object_or_404(User, pk=user_id)
    calculated_gpa.gpa=request.data['gpa']
    try:
        serializer = PersonObjectSerializer(calculated_gpa)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])   
def current_semester(request, user_id):
    """api/auth/put_semester/<int:user_id>/', #stores semester to DB
    """   
    student_semester = get_object_or_404(User, pk=user_id)
    student_semester.semester=request.data['semester']
    try:
        # student_semester.save()
        serializer = PersonObjectSerializer(student_semester)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])   
def grad_status(request, user_id):
    """api/auth/put_grad_status/<int:user_id>/' #stores grad status to DB
    """   
    status_is_a_graduate = get_object_or_404(User, pk=user_id)
    status_is_a_graduate.grad_ready=request.data['grad_ready']
    try:
        status_is_a_graduate.save()
        serializer = PersonObjectSerializer(status_is_a_graduate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])   
def student_status(request, user_id):
    """api/auth/post_student_status/<int:user_id>/' #stores student status to DB
    """   
    is_current_student = get_object_or_404(User, pk=user_id)
    is_current_student.is_student=request.data['is_student']
    try:
        is_current_student.save()
        serializer = PersonObjectSerializer(is_current_student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

