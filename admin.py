from django.contrib import admin
from .models import Department,Designation,ITCoordinator,ContractStaff,Station,EmployeeDirectory,Location,AssetType,Asset,AssetIssuance,Ticket,Engineer,MISForm,MISField,MISSubmission
from .models import Contract

# Register your models here.

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(ITCoordinator)
admin.site.register(ContractStaff)
admin.site.register(Station)
admin.site.register(Contract)
admin.site.register(EmployeeDirectory)
admin.site.register(Location)
admin.site.register(AssetType)
admin.site.register(Asset)
admin.site.register(AssetIssuance)
admin.site.register(Ticket)
admin.site.register(MISForm)
admin.site.register(MISField)
admin.site.register(MISSubmission)

  
    
@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'mobile', 'email', 'is_active')
    list_filter = ('is_active', 'designation')
    search_fields = ('name', 'designation', 'email', 'mobile')


from django.contrib import admin
from .models import UserProfile, Station


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'station', 'is_rhqwr')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "station":
            kwargs["queryset"] = Station.objects.filter(userprofile__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

        