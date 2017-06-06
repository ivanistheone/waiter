from django.contrib import admin

from .models import ContentChannel, ContentChannelRun, RunLogFile, ChannelRunEvent


@admin.register(ContentChannel)
class ContentChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_id', 'name', 'version', 'source_id', 'source_domain', 'user_registered_by')
    search_fields = ['name', 'source_domain']



class RunLogFileInline(admin.StackedInline): # TabularInline):
    model = RunLogFile
    extra = 0

class ChannelRunEventInline(admin.TabularInline):
    model = ChannelRunEvent
    list_display = ('id', 'chef_name', 'run_id', 'timestamp', 'kind')

@admin.register(ContentChannelRun)
class ContentChannelRunAdmin(admin.ModelAdmin):
    inlines = [RunLogFileInline, ChannelRunEventInline]
    list_display = ('id', 'state', 'channel_id', 'chef_name', 'logfile', 'started', 'finished')

