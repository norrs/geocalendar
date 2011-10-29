from django.conf.urls.defaults import patterns, url
import settings

urlpatterns = patterns('geocal.views',
    url(r'^$', 'list_events_year_and_month_links', name='geocal'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'events_month', name='geocal_events_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>)\d{1,2}/$', 'events_day', name='geocal_events_day'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

