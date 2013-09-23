from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns(''
    # url(r'^$', 'ezio.views.home', name='home'),
    , url(r'^accounts/login/$', login)
    , url(r'^accounts/logout/$', logout)
    
    , url(r"", include('assassins.urls'))

    , url(r'^admin/', include(admin.site.urls))
)
