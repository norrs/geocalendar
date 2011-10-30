import calendar
from datetime import datetime
from filebrowser.fields import FileBrowseField
from django.db import models

from django.utils.translation import ugettext_lazy as _

class CalendarEntry(models.Model):
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), help_text=_("Check out <a href='http://daringfireball.net/projects/markdown/basics'>this link</a> for how to use markdown syntax"))
    entry_date = models.DateField(_("entry_date"))
    keyword = models.CharField(_("keyword"), max_length=30)
    picture = FileBrowseField("picture", directory="documents/", max_length=500, extensions=['.jpg', '.jpeg', '.png', '.gif'])

    def __unicode__(self):
        return self.title
