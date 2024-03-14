from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Topic, Answer, Question, Word
from .serializers import TopicSerializer, AnswerSerializer, QuestionSerializer, WordSerializer
from rest_framework.authentication import TokenAuthentication 
from django.db.models import Q


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.filter(user__is_staff=True)
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

class UserWordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()
        topic_id = self.request.query_params.get('topic_id', None)
        word_id = self.request.query_params.get('word_id', None)

        if topic_id is not None:
            queryset = queryset.filter(topic_id=topic_id)
        elif word_id is not None:
            queryset = queryset.filter(id=word_id)

        return queryset


class UserTopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsOwnerOrAdmin]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(Q(user=user) | Q(subscribers=user))
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        topic = get_object_or_404(Topic, pk=pk)
        topic.subscribers.add(request.user)
        topic.save()
        return Response({'status': 'subscribed'}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            return Response({'detail': 'У вас нет прав для редактирования этой темы.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            return Response({'detail': 'У вас нет прав для редактирования этой темы.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        topic = get_object_or_404(Topic, pk=pk)
        topic.subscribers.remove(request.user)
        topic.save()
        return Response({'status': 'unsubscribed'}, status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user in instance.subscribers.all():
            instance.subscribers.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.filter(user__is_staff=True)
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]


class AnswerUserViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.filter(user__is_staff=True)
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        topic_id = self.request.query_params.get('question_id', None)
        
        if topic_id is not None:
            question = get_object_or_404(Question, pk=topic_id)
            return Answer.objects.filter(question=question, user=user)
        else:
            return Answer.objects.filter(user=user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(user__is_staff=True)
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    # def get_queryset(self):
    #     return Question.objects.all()


    

class QuestionUserViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(user__is_staff=True)
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        topic_id = self.request.query_params.get('topic_id', None)
        
        if topic_id is not None:
            # Фильтрация вопросов по теме и пользователю
            topic = get_object_or_404(Topic, pk=topic_id)
            return Question.objects.filter(topic=topic, user=user)
        else:
            # Если 'topic_id' не предоставлен, возвращаем все вопросы текущего пользователя
            return Question.objects.filter(user=user)