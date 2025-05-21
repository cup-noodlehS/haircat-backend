"""
Example usage of the webhook functionality
"""

from general.webhooks import send_webhook


def notify_user_about_appointment(user_id, appointment_data):
    """
    Send a notification to a user about an appointment
    
    Args:
        user_id (str): The ID of the user to notify
        appointment_data (dict): Data about the appointment
    """
    event_name = "appointment_notification"
    data = {
        "appointment_id": appointment_data.get("id"),
        "title": "New Appointment",
        "message": f"You have a new appointment on {appointment_data.get('date')} at {appointment_data.get('time')}",
        "appointment_data": appointment_data
    }
    
    success = send_webhook(event_name, user_id, data)
    return success


def notify_user_about_message(user_id, sender_name, message_content):
    """
    Send a notification to a user about a new message
    
    Args:
        user_id (str): The ID of the user to notify
        sender_name (str): The name of the message sender
        message_content (str): The content of the message
    """
    event_name = "new_message"
    data = {
        "title": "New Message",
        "sender": sender_name,
        "message": message_content,
        "timestamp": "now"  # In a real app, use a proper timestamp
    }
    
    success = send_webhook(event_name, user_id, data)
    return success 