from .models import Profile


def profile(request):
    """Expone el perfil en todas las plantillas."""
    return {"profile": Profile.objects.first()}
