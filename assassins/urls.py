from django.conf.urls import patterns, include, url

urlpatterns = patterns("assassins.views"
    , url(r"^assassins/$",              "index")
    , url(r"^assassins/report/$",       "report")
    , url(r"^assassins/view_target/$",  "view_target")
)
