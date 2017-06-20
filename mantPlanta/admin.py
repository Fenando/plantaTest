from django.contrib import admin
from mantPlanta import models
from mantPlanta.models import Mantencion
# Register your models here.

class MantencionAdmin(admin.ModelAdmin):
    list_display = ('equipos','realizada','id')

class AccionAdmin(admin.ModelAdmin):
    list_display = ('mantencion','id')

class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre','id')

class InfoAdmin(admin.ModelAdmin):
    list_display = ('nombre','id')

admin.site.register(models.Equipo)
admin.site.register(models.Area, AreaAdmin)

admin.site.register(models.Tipo)
admin.site.register(models.Informacion, InfoAdmin)
admin.site.register(models.Planta)
admin.site.register(models.Acciones,AccionAdmin)
admin.site.register(models.Comentario)

admin.site.register(Mantencion,MantencionAdmin)

