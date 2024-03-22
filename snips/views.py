from django.shortcuts import render, redirect
from .forms import SnipForm
from .models import Snip
import random

def ordinal_format(n):
    """
    Convert an integer into its ordinal representation.

    :param n: Integer to convert.
    :return: Ordinal number as a string.
    """
    return "%d%s" % (n, "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

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
                snip.claim_attempts += 1
                if snip.student_id:
                    message = 'Nice try, but this Snip has already been claimed. 😑'
                    form = SnipForm()  # Reset form
                else:
                    snip.student_id = student_id
                    # Access the classroom through the snip's snipsheet
                    classroom = snip.snipsheet.classroom
                    # Count how many Snips the student has in this classroom
                    previously_claimed_snips = Snip.objects.filter(snipsheet__classroom=classroom, student_id=student_id).count()
                    # Select emoji for this message
                    emoji = random.choice(['🎉', '👏', '🎈', '🥳', '😎', '🙌'])
                    # Update the success message to include the ordinal number and random emoji
                    message = f'Awesome, you have successfully claimed your {ordinal_format(previously_claimed_snips + 1)} Snip! {emoji}'
                    form = SnipForm()  # Reset form
                snip.save()
            except Snip.DoesNotExist:
                message = 'Sorry, this Snip does not exist. ☹️'
    else:
        # Initialize the form with GET data if present, or with no data if not
        form = SnipForm(initial=initial_data)

    context = {'form': form, 'message': message}
    return render(request, 'snips/home.html', context)
