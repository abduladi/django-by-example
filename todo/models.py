from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.db import models
from django.contrib import admin

class DateTime(models.Model):
    list_display = ["datetime"]
    inlines = [ItemInline]
    datetime = models.DateTimeField(auto_now_add=True)

    def response_add(self, request, obj, post_url_continue="../%s/"):
        """Determines the HttpResponse for the add_view stage. """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = "Item(s) were added successfully."
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + " " + 
                    "You may edit it again below."
                    )
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse(
                    '<script type="text/javascript">',
                    'opener.dismissAddAnotherPopup(window, "%s", "%s");'
                    '</script>' % (escape(pj_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_
                ("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

    def __unicode__(self):
        return unicode(self.datetime)

class Item(models.Model):
    name = models.CharField(max_length=60)
    created = models.ForeignKey(DateTime)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    done = models.BooleanField(default=False)

class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "created", "done"]
    search_fields = ["name"]

class ItemInline(admin.TabularInline):
    model = Item

class DateAdmin(admin.ModelAdmin):
    list_display = ["datetime"]
    inlines = [ItemInline]

admin.site.register(DateTime, DateAdmin)
admin.site.register(Item, ItemAdmin)
