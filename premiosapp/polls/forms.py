# First form not empty and can not be deleted
from django.forms.models import BaseInlineFormSet    

class RequiredInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        if i < 2:
            form.empty_permitted = False
        return form
