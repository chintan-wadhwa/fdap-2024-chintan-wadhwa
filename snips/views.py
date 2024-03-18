from django.shortcuts import render, redirect
from .forms import SnipForm
from .models import Snip

def home(request):
    message = None  # Initialize message variable
    initial_data = {}

    # Check if there's a snip_id in the GET request and use it to pre-populate the form
    snip_id = request.GET.get('snip_id')
    if snip_id:
        initial_data['snip_id'] = snip_id  # Add the snip_id to the form's initial data

    if request.method == 'POST':
        form = SnipForm(request.POST)
        if form.is_valid():
            snip_id = form.cleaned_data['snip_id']
            student_id = form.cleaned_data['student_id']
            try:
                snip = Snip.objects.get(snip_id=snip_id)
                if snip.student_id:
                    message = 'Nice try, but this Snip has already been claimed. :/'
                else:
                    snip.student_id = student_id
                    snip.save()
                    message = f'Awesome, you have successfully claimed this Snip: {snip_id}! :)'
                    form = SnipForm()  # Reset form
            except Snip.DoesNotExist:
                message = 'Sorry, this Snip does not exist. :('
    else:
        # Initialize the form with GET data if present, or with no data if not
        form = SnipForm(initial=initial_data)

    context = {'form': form, 'message': message}
    return render(request, 'snipcollect/home.html', context)
