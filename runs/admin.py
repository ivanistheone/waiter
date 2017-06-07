from django.contrib import admin

from .models import ContentChannel, ContentChannelRun, ChannelRunLog, ChannelRunEvent


@admin.register(ContentChannel)
class ContentChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_id', 'name', 'version', 'source_id', 'source_domain', 'user_registered_by')
    search_fields = ['name', 'source_domain']



class ChannelRunLogInline(admin.StackedInline): # TabularInline):
    model = ChannelRunLog
    extra = 0

class ChannelRunEventInline(admin.TabularInline):
    model = ChannelRunEvent
    list_display = ('id', 'chef_name', 'run_id', 'timestamp', 'kind')

@admin.register(ContentChannelRun)
class ContentChannelRunAdmin(admin.ModelAdmin):
    inlines = [ChannelRunLogInline, ChannelRunEventInline]
    list_display = ('run_id', 'state', 'channel_id', 'chef_name', 'runlog', 'started', 'finished')

