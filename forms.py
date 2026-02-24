from django import forms
from accounts.models import ITCoordinator,ContractStaff,Department,Designation

class ITCoordinatorForm(forms.ModelForm):
    Department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={"class":"form select w-full border rounded p-2"})
    )


    Designation = forms.ModelChoiceField(
        queryset=Designation.objects.all(),
        widget=forms.Select(attrs={"class":"form select w-full border rounded p-2"})
    )


    class Meta:
        model = ITCoordinator
        fields = ['station','name', 'department_name', 'designation', 'location', 'email', 'contact_number', 'employee_id']
        widgets = {
            'station': forms.TextInput(attrs={'class': 'w-full border rounded-1g p-2 focus:ring-2 focus:ring-blue-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-500'}),
            'department_name': forms.Select(attrs={'class': 'w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-500'}),
            'designation': forms.Select(attrs={'class': 'w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-500'}),
            'location': forms.TextInput(attrs={'class': 'w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-500'}),
            'contact_number': forms.TextInput(attrs={'class': 'w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-500'}),
            'employee_id': forms.TextInput(attrs={'class': 'w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-500'}),
        }


