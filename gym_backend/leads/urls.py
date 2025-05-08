# gym_backend/leads/urls.py

from django.urls import path
from .views import create_lead  # Only import create_lead

urlpatterns = [
    # No path for a general homepage here, only the API endpoint
    path('api/create-lead/', create_lead, name='create_lead'), # Ensure 'name' is consistent if used elsewhere
]