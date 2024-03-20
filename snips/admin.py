from django.contrib import admin
from .models import Classroom, Snipsheet, Snip

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_id', 'name', 'semester', 'school')

class SnipsheetAdmin(admin.ModelAdmin):
    list_display = ('snipsheet_id', 'classroom_id')
    list_filter = ('classroom_id',)

class SnipAdmin(admin.ModelAdmin):
    list_display = ('snip_id', 'student_id', 'snipsheet', 'get_classroom_id')
    search_fields = ('student_id', 'snip_id')
    list_filter = ('snipsheet',)

    def get_classroom_id(self, obj):
        return obj.snipsheet.classroom.classroom_id
    get_classroom_id.short_description = 'Classroom ID'  # Sets column name

admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Snipsheet, SnipsheetAdmin)
admin.site.register(Snip, SnipAdmin)
