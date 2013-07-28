from django.conf.urls import patterns, include, url

urlpatterns = patterns("assassins.views"
    , url(r"^assassins/$",                       "index")
    , url(r"^assassins/report/$",                "report")
    , url(r"^assassins/view_target/$",           "view_target")
    , url(r"^assassins/leaderboard/$",           "leaderboard")
    , url(r"^assassins/news/archive/$",          "news_archive")
    , url(r"^assassins/news/(?P<news_id>\d+)/$", "news_detail")
)
