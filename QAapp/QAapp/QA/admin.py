from django.contrib import admin

# Register your models here.
from QA.models import User,Answer,Question,Questionans
from QA.forms import AnswerForm,QuestionForm

#class AnswerAdmin(admin.ModelAdmin):
#  form = AnswerForm
#  fieldsets = (
#    (None, {'fields': ('answer', 'Question')}),
#  )

#class QuestionAdmin(admin.ModelAdmin):
#  form = QuestionForm
#  fieldsets = (
#    (None, {'fields': ('question', 'User')}),
#  )
  
  


admin.site.register(User)
admin.site.register(Answer)#,AnswerAdmin
admin.site.register(Question)#,QuestionAdmin
admin.site.register(Questionans)
