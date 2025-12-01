from django.urls import path
from rest_framework import routers

from leads.views import ContactusViewset

router = routers.DefaultRouter()

urlpatterns = router.urls + [
    path(
        "contact_us/",
        ContactusViewset.as_view(
            {
                "post": "Contact",
            }
        ),
        name="Contact",
    ), ]
