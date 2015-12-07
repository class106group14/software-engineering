from django.db.models.fields.related import ManyToManyRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from django import forms

from django.contrib import admin
                                                                
from QA.models import Answer, Question, User                     
                                                                
class AnswerForm(forms.ModelForm):                             
                                                                
  questions = forms.ModelMultipleChoiceField(                      
    Question.objects.all(),                                        
# Add this line to use the double list widget                  
#    widget=admin.widgets.FilteredSelectMultiple('Books', False),
    required=False,                                            
  ) 
     
  def __init__(self, *args, **kwargs):                         
    super(AnswerForm, self).__init__(*args, **kwargs)
    if self.instance.pk:
      #if this is not a new object, we load related books                                       
      self.initial['questions'] = self.instance.questions.values_list('pk', flat=True)
      rel = ManyToManyRel(Question)
      self.fields['questions'].widget = RelatedFieldWidgetWrapper(self.fields['questions'].widget, rel, admin.site)
   
  def save(self, *args, **kwargs):                             
    instance = super(AnswerForm, self).save(*args, **kwargs)   
    if instance.pk:
      for question in instance.questions.all():
        if question not in self.cleaned_data['questions']:            
          # we remove books which have been unselected 
          instance.questions.remove(question)
      for question in self.cleaned_data['questions']:                  
        if question not in instance.questions.all():                   
          # we add newly selected books
          instance.questions.add(question)      
    return instance

class QuestionForm(forms.ModelForm):                             
                                                                
  users = forms.ModelMultipleChoiceField(                      
    User.objects.all(),                                        
# Add this line to use the double list widget                  
#    widget=admin.widgets.FilteredSelectMultiple('Books', False),
    required=False,                                            
  ) 
     
  def __init__(self, *args, **kwargs):                         
    super(QuestionForm, self).__init__(*args, **kwargs)
    if self.instance.pk:
      #if this is not a new object, we load related books                                       
      self.initial['users'] = self.instance.users.values_list('pk', flat=True)
      rel = ManyToManyRel(User)
      self.fields['users'].widget = RelatedFieldWidgetWrapper(self.fields['users'].widget, rel, admin.site)

   
  def save(self, *args, **kwargs):                             
    instance = super(QuestionForm, self).save(*args, **kwargs)   
    if instance.pk:
      for user in instance.users.all():
        if user not in self.cleaned_data['users']:            
          # we remove books which have been unselected 
          instance.users.remove(user)
      for user in self.cleaned_data['users']:                  
        if user not in instance.users.all():                   
          # we add newly selected books
          instance.users.add(user)      
    return instance


class userForm(forms.Form):  
    password=forms.CharField()  
    newpassword=forms.CharField()   
      
    def clean(self):  
  
        cleaned_data = super(userForm, self).clean()    
        password= cleaned_data.get("password")  
        newpassword= cleaned_data.get("newpassword")  
        if password and newpassword:  
            if password!=newpassword:  
                msg = u"Not the same"  
                self._errors["newpassword"] = self.error_class([msg])  
        return cleaned_data  
 
    #captcha=CaptchaField()  from captcha.fields import CaptchaField
    

