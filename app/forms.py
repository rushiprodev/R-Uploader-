from django import forms
from .models import Resume

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

JOB_CITY_CHOICES = [
    ('Delhi', 'Delhi'),
    ('Mumbai', 'Mumbai'),
    ('Pune', 'Pune'),
    ('Bangalore', 'Bangalore'),
    ('Hyderabad', 'Hyderabad'),
    ('Chennai', 'Chennai'),
    ('Kolkata', 'Kolkata'),
]

class ResumeForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    job_city = forms.MultipleChoiceField(
        choices=JOB_CITY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Preferred Job Locations"
    )

    class Meta:
        model = Resume
        fields = [
            'id', 'name', 'dob', 'gender', 'locality', 'city', 'pin',
            'state', 'mobile', 'email', 'job_city', 'profile_image', 'my_file'
        ]

        labels = {
            'id': 'Candidate ID',
            'name': 'Full Name',
            'dob': 'Date of Birth',
            'gender': 'Gender',
            'locality': 'Locality',
            'city': 'City',
            'pin': 'PIN Code',
            'state': 'State',
            'mobile': 'Mobile Number',
            'email': 'Email Address',
            'job_city': 'Preferred Job Locations',
            'profile_image': 'Profile Image',
            'my_file': 'Resume File (PDF/DOC)',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'pin': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'job_city' is overridden above using MultipleChoiceField
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'my_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_job_city(self):
        # Convert selected values list into comma-separated string for storage
        selected_cities = self.cleaned_data.get('job_city', [])
        return ', '.join(selected_cities)
