from django.urls import path

from .views import user_home, user_data, user_stats, user_wastes, \
    user_wastes_create, user_wastes_update, user_wastes_delete, \
    user_wastes_duplicate, user_wastes_ask_removal, \
    user_data_update, user_wastes_bookmark

urlpatterns = [
    path('user/', user_home, name='user_home'),
    path('meus_dados/', user_data, name='user_data'),
    path('meus_dados/update/', user_data_update, name='update_data'),
    path('minhas_estatisticas/', user_stats, name='user_stats'),
    path('meus_residuos/', user_wastes, name='user_wastes'),
    path('meus_residuos/create/', user_wastes_create, name='create_waste'),
    path('meus_residuos/update/<int:waste_id>/', user_wastes_update,
         name='update_waste'),
    path('meus_residuos/delete/<int:waste_id>/', user_wastes_delete,
         name='delete_waste'),
    path('meus_residuos/bookmark/<int:waste_id>/', user_wastes_bookmark,
         name='bookmark_waste'),
    path('meus_residuos/duplicate/<int:waste_id>/', user_wastes_duplicate,
         name='duplicate_waste'),
    path('meus_residuos/ask_removal/<int:waste_id>/', user_wastes_ask_removal,
         name='ask_removal_waste'),
]
