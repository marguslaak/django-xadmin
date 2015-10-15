from django.conf.urls import patterns, include, url
from xadmin import autodiscover
import xadmin

autodiscover()


urlpatterns = patterns('',
    # url(r'^view_base/', include('view_base.urls')),
    url(r'^xadmin/', include(xadmin.site.urls)),
)