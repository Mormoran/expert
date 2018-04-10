from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from django.views import defaults as default_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='expert/'), name='home'),
    # url(r'^about/$', TemplateView.as_view(template_name='pages/about.html')),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('impedans_expert.users.urls', namespace='users')),
    url(r'^expert_upload/', include('impedans_expert.expert_upload.urls', namespace='expert_upload')),
    url(r'^expert_documents/', include('impedans_expert.expert_documents.urls', namespace='expert_documents')),
    url(r'^expert/', include('impedans_expert.expert.urls')),
    url(r'^expert_import/', include('impedans_expert.expert_import.urls', namespace='expert_import')),
    url(r'^expert_algorithms/', include('impedans_expert.expert_algorithms.urls', namespace='expert_algorithms')),
    # Your stuff: custom urls includes go here
    url(r'^tellme/', include("tellme.urls")),
    url(r'^filer/', include('filer.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.FILES_URL, filer_root=settings.FILES_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
