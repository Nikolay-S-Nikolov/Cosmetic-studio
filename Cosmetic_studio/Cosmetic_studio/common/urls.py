from django.urls import path, include

from Cosmetic_studio.common.views import IndexView, about, blog, contact, TeamMemberCardCreateView, AdvCardCreateView, \
    AdvCardUpdateView, AdvCardDeleteView, TeamMemberCardUpdateView, TeamMemberCardDeleteView, TeamMemberDetailsView, \
    ABoutMeDetailsView

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('about-me/', ABoutMeDetailsView.as_view(), name='about_me'),
    path('team/', include([
        path('create-member-card/', TeamMemberCardCreateView.as_view(), name='create_team_member'),
        path('<int:pk>/', include([
            path('details-team-member/', TeamMemberDetailsView.as_view(), name='details_team_member'),
            path('update-team-member/', TeamMemberCardUpdateView.as_view(), name='update_team_member'),
            path('delete-team-member/', TeamMemberCardDeleteView.as_view(), name='delete_team_member'),
        ])),
    ])),
    path('adv/', include([
        path('create-adv-card/', AdvCardCreateView.as_view(), name='create_adv_card'),
        path('<int:pk>/', include([
            path('update-adv-card/', AdvCardUpdateView.as_view(), name='update_adv_card'),
            path('delete-adv-card/', AdvCardDeleteView.as_view(), name='delete_adv_card'),
        ])),
    ])),
    path('about/', about, name='about'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
)
