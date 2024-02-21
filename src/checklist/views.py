from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.models import User
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer, UserSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404

# _____________________________________________ JWT


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# _____________________________________________ User


class RegisterView(APIView):
    def post(self, request):
        try:
            User.objects.create_user(
                username=request.data["username"], password=request.data["password"]
            )
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "User might already exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UsersMethods(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# _____________________________________________ Category


class CategoriesMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(owner=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class CategoryMethods(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, categoryId):
        category = get_object_or_404(Category, pk=categoryId)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, categoryId):
        category = get_object_or_404(Category, pk=categoryId)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryTasksMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, categoryId):
        category = get_object_or_404(Category, pk=categoryId)
        tasks = Task.objects.filter(owner=request.user, category=category)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# _____________________________________________ Task


class TasksMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        categoryId = request.query_params["categoryId"]
        category = get_object_or_404(Category, pk=categoryId)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, category=category)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskMethods(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, taskId):
        task = get_object_or_404(Task, pk=taskId)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, taskId):
        task = get_object_or_404(Task, pk=taskId)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
