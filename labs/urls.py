from django.urls import path

from .views import user_home, user_data, user_stats, user_wastes, \
    user_wastes_create, user_wastes_update, user_wastes_delete, \
    user_wastes_bookmark, user_bookmarked_waste_use, \
    user_bookmarked_waste_delete, user_data_update

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
    path('meus_residuos/bookmark/create/<int:waste_id>/',
         user_bookmarked_waste_use, name='use_bookmarked_waste'),
    path('meus_residuos/bookmark/delete/<int:bwaste_id>/',
         user_bookmarked_waste_delete, name='delete_bookmarked_waste'),
]
