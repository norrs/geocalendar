from django import forms
from django.utils.translation import ugettext_lazy as _

class EntryKeywordVerify(forms.Form):
    id = "geocal_keyword_verify_for_entry"
    keyword = forms.CharField("keyword", required=True, label=_("Keyword"))

    def clean(self):
        if (self._errors):
            return
        return self.cleaned_data