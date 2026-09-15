from django.forms import ModelForm
from .models import Student

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email']  # Specify the fields you want to include in the form
        # fields = '__all__'

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError("Age must be 18 or older.")
        return age