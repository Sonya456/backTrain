from django.contrib import admin
from .models import Topic, Question, Word, Answer#, UserProfile

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'user', 'added_at']
    filter_horizontal = ('subscribers',)  
admin.site.register(Question)
admin.site.register(Word)
admin.site.register(Answer)
# admin.site.register(UserProfile)
