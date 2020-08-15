from django.urls import path
from .views import IntroEval, QuestionListView, TestResultView
urlpatterns = [
    path('/intro',IntroEval.as_view()),
    path('/question', QuestionListView.as_view()),
    path('/result', TestResultView.as_view()),
]
