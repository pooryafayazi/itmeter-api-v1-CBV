from django.contrib import admin
from .models import *
# Register your models here.

from django_summernote.admin import SummernoteModelAdmin

class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ['name', 'email', 'creator', 'created_date']
    list_filter = ['email', 'creator']
    search_fields = ['name', 'message']

class NewsAdmin(SummernoteModelAdmin):
    date_hierarchy = 'published_date'
    empty_value_display = "-empty-"    
    verbose_name_plural = 'News'
    #fields = [ "title"]
    #exclude = ["birth_date"]
    list_display = ["short_title","author", "status",'published_date']
    list_filter =  ["status",'published_date',"author",]
    #ordering = ['-created_date']
    search_fields = ["title", "'content"]

    summernote_fields = ('content',)
    def short_title(self, obj):
        return obj.title[:45]+ "..."
    short_title.short_description = 'title'

class NewsCommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    #fields = [ "title"]
    #exclude = ["birth_date"]
    list_display = ["name","news", "approved","created_date",'updated_date']
    list_filter =  ["news",'updated_date',"approved",]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter)
admin.site.register(News, NewsAdmin)
admin.site.register(Topic)
admin.site.register(newsComment, NewsCommentAdmin)
