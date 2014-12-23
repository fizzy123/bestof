from django.conf.urls import patterns, url

from bestof import views

urlpatterns = patterns('bestof.views',
        url(r'^$', 'categories', name='categories'),
        url(r'^nominees/(?P<key>[^ \t\n\r\f\v/]+)$', 'nominees', name='nominees'),
        url(r'^judge/(?P<key>[^ \t\n\r\f\v/]+)$', 'judge', name='judge'),
        url(r'^compare/(?P<key>[^ \t\n\r\f\v/]+)$', 'compare', name='compare'),
)
