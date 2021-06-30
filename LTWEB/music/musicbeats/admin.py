from django.contrib import admin
from .models import Song,WatchLater,History,Channel
# Register your models here.

admin.site.register(Song),
admin.site.register(WatchLater),
admin.site.register(History),
admin.site.register(Channel),
