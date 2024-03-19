from django import forms

class SnipForm(forms.Form):
    snip_id = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Snip ID', 'class': 'form-control'}), max_length=11)
    student_id = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Student ID', 'class': 'form-control'}), max_length=100)

    def clean_snip_id(self):
        data = self.cleaned_data['snip_id']
        normalized_data = data.replace('-', '').lower()
        if len(normalized_data) != 9:
            raise forms.ValidationError("Ensure that the Snip ID is 9 characters long.")
        return normalized_data



