from django.contrib import admin

from .models import Question, Choice
from .forms import RequiredInlineFormSet


# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    exclude = ['votes']
    extra = 2
    formset = RequiredInlineFormSet # or AtLeastOneFormSet

class QuestionAdmin(admin.ModelAdmin):
    fields= ["pub_date", "question_text"]
    inlines = [
        ChoiceInline,
    ]
    list_display = ("question_text","pub_date", "was_published_recently") 
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)