from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from stats.views import evaluate_wastes, user_stats

urlpatterns = [
    path('evaluate/<str:queryset_ids>/', evaluate_wastes,
         name='evaluate_wastes'),
    # reverse( ) causes circular import error
    path('', RedirectView.as_view(url=reverse_lazy('admin:index')),
         name='admin_index'),
    path('minhas_estatisticas/', user_stats, name='user_stats'),
]
