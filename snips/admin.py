from django.contrib import admin
from .models import Classroom, Snipsheet, Snip

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_id', 'name', 'semester', 'school')

class SnipsheetAdmin(admin.ModelAdmin):
    list_display = ('snipsheet_id', 'classroom_id')

class SnipAdmin(admin.ModelAdmin):
    list_display = ('snip_id', 'student_id', 'snipsheet')

admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Snipsheet, SnipsheetAdmin)
admin.site.register(Snip, SnipAdmin)
