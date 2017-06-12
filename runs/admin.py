from django.contrib import admin

from .models import ContentChannel, ContentChannelRun, ChannelRunStage


@admin.register(ContentChannel)
class ContentChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_id', 'name', 'version', 'source_id', 'source_domain',
                    'registered_by_user', 'default_content_server', 'created_at')
    search_fields = ['name', 'source_domain']



class ChannelRunStageInline(admin.TabularInline):
    model = ChannelRunStage
    list_display = ('id', 'name', 'started', 'finished', 'duration')

@admin.register(ContentChannelRun)
class ContentChannelRunAdmin(admin.ModelAdmin):
    def channel_id(self, obj):
        return obj.channel.channel_id
    inlines = [ChannelRunStageInline, ]
    list_display = ('run_id', 'channel_id', 'chef_name', 'created_at')

