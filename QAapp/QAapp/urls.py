from django.conf.urls import patterns, include, url
from QA.views import *

from django.contrib import admin
admin.autodiscover()


from QAapp import settings##

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'QAapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',login),
    url(r'^login/',login),
    url(r'^logout/',logout),
    url(r'^answer/',answer),
    url(r'^register/',register),
    url(r'^question/',question),
    url(r'^ques-ans/',quesans),
    url(r'^showanswer/',showanswer),
    url(r'^editanswer/',editanswer),
    url(r'^addanswer/',addanswer),
    url(r'^changeanswer/',changeanswer),
    url(r'^changeaddanswer/',changeaddanswer),
    url(r'^myanswer/',myanswer),
    url(r'^questionlist/',questionlist),
    url(r'^mquestionlist/',mquestionlist),
    url(r'^answerlist/',answerlist),
    url(r'^givescore/',givescore),
    url(r'^managepage/',managepage),
    url(r'^manageout/',manageout),
    url(r'^userlist/',userlist),
    url(r'^deluser/',deluser),
    url(r'^delquestion/',delquestion),
    url(r'^delanswer/',delanswer),
    (r'^Media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS,'show_indexes': True}),
)
