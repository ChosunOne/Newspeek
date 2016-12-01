from django.conf.urls import include, url

from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

import news.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', news.views.index, name='index'),
]
