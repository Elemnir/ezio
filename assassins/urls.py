from django.conf.urls import patterns, include, url

urlpatterns = patterns("ezio.assassins.views"
    , url(r"^assassins$",           "index")
    , url(r"^assassins/panel$",     "panel")
    , url(r"^assassins/report$",    "report")
)
