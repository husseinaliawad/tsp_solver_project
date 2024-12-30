from django import forms

class TSPForm(forms.Form):
    locations = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter locations, e.g., A, B, C'}),
        label='Locations',
        max_length=200
    )
    distances = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter distance matrix'}),
        label='Distance Matrix',
        max_length=1000
    )

    def clean(self):
        cleaned_data = super().clean()
        locations = cleaned_data.get('locations', '').split(',')
        distances = cleaned_data.get('distances', '').strip().splitlines()

        if len(locations) > 10:
            raise forms.ValidationError("You can only enter up to 10 locations.")
        if len(distances) != len(locations):
            raise forms.ValidationError("Matrix rows must match the number of locations.")
        for row in distances:
            if len(row.split(',')) != len(locations):
                raise forms.ValidationError("Matrix columns must match the number of locations.")

        return cleaned_data
