import json

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import *
from user.models import UserQuestion
from user.utils import is_active

class QuestionListView(View):
    def get(self,request):
        questions = Question.objects.select_related('section').all().order_by('section_id')
        result = [{
            'id'        : ques.id,
            'question'  : ques.content,
            'section'   : ques.section.name
        } for ques in questions]
        return JsonResponse({'data' : result}, status = 200)

class TestResultView(View):
    @is_active
    def post(self,request):
        user_id = request.user.id
        data    = json.loads(request.body)
        result  = data['data']
        for ques in result:
            UserQuestion.objects.create(
                user_id     = user_id,
                question_id = ques['id'],
                point       = int(ques['point'])
            )
        return HttpResponse(status = 200)

    
    def get(self,reqeust):
        user        = request.user
        responses   = None
        if user.auth.name == 'Applicant':
            responses = UserQuestion.objects.select_related('question','user').filter(user_id = user.id).order_by('user_id')
        elif user.auth.name == 'Head_of_Dept':
            users       = User.objects.filter(department_id = user.department.id)
            responses   = UserQuestion.objects.select_related('question','user').filter(
                user_id__in = User.objects.filter(department_id = user.department.id).values_list('id', flat = True)
            ).order_by('user_id')
        else:
            responses = UserQuestion.objects.select_related('question','user').all().order_by('user_id')
        result = [{
                'user'      : res.user.name,
                'section'   : res.question.section,
                'id'        : res.question.id,
                'question'  : res.question.content,
                'response'  : res.point
            } for res in responses]
        return JsonResponse({'data' : result}, status = 200)

class IntroEval(View):
    def get(self,request):
        introductions   = Introduction.objects.all()
        notices         = Notice.objects.all()
        intro_list      = [introduction.content for introduction in introductions]
        notice_list     = [notice.content for notice in notices]
        return JsonResponse({ 'intro' : intro_list, 'notice' : notice_list },status = 200)

