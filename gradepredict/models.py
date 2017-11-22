from django.db import models
from django.forms import ModelForm, Textarea

# Create your models here.
class Input(models.Model):
    csvstr = models.TextField( verbose_name=u"CSV record for all test grades:", help_text=u"", null=True, blank=True)
    csvfile = models.FileField(upload_to='documents/', verbose_name=u"Upload your CSV file:", help_text=u"", null=True, blank=True)

    def __get_label(self, field):
        return text_type(self._meta.get_field(field).verbose_name)

    def __get_help_text(self, field):
        return text_type(self._meta.get_field(field).help_text)

    def csvstr_label(self):
        return self.__get_label('csvstr')

    def csvstr_help_text(self):
        return self.__get_help_text('csvstr')

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = '__all__'
