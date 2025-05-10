from django.db import migrations

def create_message_threads(apps, schema_editor):
    """
    Create AppointmentMessageThread for all existing Appointment instances
    that don't have one yet
    """
    Appointment = apps.get_model('hairstyle', 'Appointment')
    AppointmentMessageThread = apps.get_model('hairstyle', 'AppointmentMessageThread')
    
    # Get all appointments
    appointments = Appointment.objects.all()
    
    # Create message threads for appointments that don't have one
    for appointment in appointments:
        # Check if thread already exists
        if not AppointmentMessageThread.objects.filter(appointment=appointment).exists():
            AppointmentMessageThread.objects.create(appointment=appointment)


def reverse_migration(apps, schema_editor):
    """
    No need to do anything in reverse migration as message threads
    will be deleted automatically when appointments are deleted
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hairstyle', '0007_appointmentmessagethread_appointmentmessage_and_more'),
    ]

    operations = [
        migrations.RunPython(create_message_threads, reverse_migration),
    ] 