from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre-mi/", views.about, name="about"),
    path("skills/", views.skills, name="skills"),
    path("proyectos/", views.projects, name="projects"),
    path("proyectos/<slug:slug>/", views.project_detail, name="project_detail"),
    path("experiencia/", views.experience, name="experience"),
    path("contacto/", views.contact, name="contact"),
    path("cv/", views.download_cv, name="cv_download"),
]
