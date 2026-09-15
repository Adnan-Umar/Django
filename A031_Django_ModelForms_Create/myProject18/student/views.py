from django.shortcuts import render
from .forms import StudentForm

# Create your views here.
def student_create(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'student_success.html')  # Redirect to a success page or another view
    else:
        form = StudentForm()

    return render(request, 'student_form.html', {'form': form})