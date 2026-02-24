from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# VALIDATORS FOR DATE , CONTACT NUMBER 
def validate_future_date_not_allowed(value):
    if value and value > timezone.now().date():
        raise ValidationError("Future date is not allowed.")


phone_validator = RegexValidator(
    regex=r'^[0-9]{10,15}$',
    message="Enter a valid contact number (10–15 digits)."
)




 # Department
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


# Designation
class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

# Station
class Station(models.Model):
    name = models.CharField(max_length=150, unique=True, null=True, blank=True)
    location = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

# Location
class Location(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='locations', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.station.name if self.station else 'No Station'})"

# Assettype
class AssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



# USER PROFILE
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    station = models.OneToOneField(Station, on_delete=models.SET_NULL, null=True, blank=True)
    is_rhqwr = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



# IT COORDINATOR
class ITCoordinator(models.Model):
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    department_name = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(null=True)
    contact_number = models.CharField(max_length=15, null=True, validators=[phone_validator])
    apd_name = models.CharField(max_length=100, null=True)
    apd_contact_number = models.CharField(max_length=15, null=True, validators=[phone_validator])
    apd_email_address = models.EmailField(null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.station})"



# CONTRACT STAFF
class ContractStaff(models.Model):
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    contractor_name = models.CharField(max_length=100)
    contract_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    department_name = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=200, null=True)
    contact_number = models.CharField(max_length=15, validators=[phone_validator])
    email = models.EmailField()

    def __str__(self):
        return self.name



# CONTRACT
class Contract(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    description_of_contract = models.CharField(max_length=255)
    contractor_name = models.CharField(max_length=255)
    contractor_address = models.TextField()
    contract_person = models.CharField(max_length=100)
    contract_person_email = models.EmailField()
    contract_number = models.CharField(max_length=100, unique=True)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.contract_number} ({self.contractor_name})"



# EMPLOYEE DIRECTORY
class EmployeeDirectory(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    direct_line_phone = models.CharField(max_length=20, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True, validators=[phone_validator])
    official_email = models.EmailField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.designation or 'No Designation'})"



# ASSET
class Asset(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="station_assets", null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location_assets", null=True, blank=True)
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True, blank=True, related_name="assets")
    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    date_of_purchase = models.DateField(null=True, blank=True, validators=[validate_future_date_not_allowed])
    aai_asset_code = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return f"{self.asset_type or 'Asset'} - {self.serial_number or 'NoSN'}"



# ASSET ISSUANCE
class AssetIssuance(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True, blank=True)

    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100)

    aai_asset_code = models.CharField(max_length=100, null=True, blank=True)

    issued_status = models.CharField(
        max_length=20,
        choices=[("user", "Issued"), ("stock", "Returned")],
        default="user"
    )

    user_name = models.CharField(max_length=255, null=True, blank=True)
    user_department = models.CharField(max_length=255, null=True, blank=True)
    user_designation = models.CharField(max_length=255, null=True, blank=True)
    user_extension = models.CharField(max_length=50, null=True, blank=True)

    date_of_issue = models.DateField(null=True, blank=True, validators=[validate_future_date_not_allowed])
    date_of_return = models.DateField(null=True, blank=True, validators=[validate_future_date_not_allowed])

    remarks = models.TextField(null=True, blank=True)
    return_remarks = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.serial_number} - {self.issued_status}"



# ENGINEER
class Engineer(models.Model):
    name = models.CharField(max_length=255)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True, validators=[phone_validator])
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'station')

    def __str__(self):
        return f"{self.name} ({self.station})"




# TICKETS 
from django.core.exceptions import ValidationError
from django.utils import timezone


class Ticket(models.Model):

    URGENCY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    ]

    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('moderate', 'Moderate'),
        ('minor', 'Minor'),
    ]

    CATEGORY_CHOICES = [
        ('desktop_hardware', 'Desktop Hardware'),
        ('email', 'Email'),
        ('internet', 'Internet'),
        ('network', 'Network'),
        ('os', 'Operating System'),
    ]

    ticket_number = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)

    requester = models.ForeignKey(
        EmployeeDirectory,
        on_delete=models.PROTECT,
        related_name='tickets'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )

    assigned_engineer = models.ForeignKey(
        Engineer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    description = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)

    closed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='closed_tickets'
    )

    
    call_time = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    # SYSTEM
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id} - {self.subject}"

   
    # VALIDATIONS
   

    def clean(self):
        

        #  Future call time not allowed
        if self.call_time and self.call_time > timezone.now():
            raise ValidationError({
                'call_time': "Call time cannot be in the future."
            })
        #  Future closed time not allowed
        if self.closed_at and self.closed_at > timezone.now():
            raise ValidationError({
                'closed_at': "Resolution time cannot be in the future."
            })

        #  Resolution before call time
        if self.call_time and self.closed_at:
            if self.closed_at < self.call_time:
                raise ValidationError({
                    'closed_at': "Resolution time cannot be before call time."
                })

        #  Closed ticket must have resolution text
        if self.closed_at and not self.resolution:
            raise ValidationError({
                'resolution': "Resolution is mandatory before closing the ticket."
            })

    # DERIVED PROPERTIES
    

    @property
    def status(self):
        return "Closed" if self.closed_at else "Open"

    @property
    def resolution_time(self):
        
        if self.call_time and self.closed_at:
            diff = self.closed_at - self.call_time
            total_minutes = int(diff.total_seconds() // 60)

            hours = total_minutes // 60
            minutes = total_minutes % 60

            if hours > 0:
                return f"{hours}h {minutes}m"
            return f"{minutes}m"
        return "—"


# MIS FORM

from django.db import models
from django.contrib.auth.models import User

class MISForm(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True,blank=True)
    

    def __str__(self):
        return self.name

 # MIS FORM DYNAMIC FIELDS 

class MISField(models.Model):
    form = models.ForeignKey(MISForm, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=50)

    def __str__(self):
        return self.label


# MIS SUBMISSION

class MISSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('editable', 'Editable'),
        ('approved', 'Approved'),
    ]

    form = models.ForeignKey(MISForm, on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='submitted'
    )
    edit_allowed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='mis_edit_allowed_by'
    )
    edit_allowed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['form', 'station'],
                name='unique_form_station_submission'
            )
        ]

    def __str__(self):
        return f"{self.form.name} - {self.station}"

