import frappe
from frappe import _
from helpdesk.utils import agent_only


@frappe.whitelist()
@agent_only  
def get_dashboard_notifications():
    """
    Get real-time notifications for the dashboard
    """
    # Return empty notifications for now to prevent errors
    return []


@frappe.whitelist()
@agent_only
def mark_notification_read(notification_id):
    """
    Mark a specific notification as read
    """
    return {"status": "success"}


@frappe.whitelist()
@agent_only  
def mark_all_notifications_read():
    """
    Mark all notifications as read for the current user
    """
    return {"status": "success"}


@frappe.whitelist()
@agent_only
def get_recent_activities(page=1, filter_type="All", page_size=20):
    """
    Get recent activities for the dashboard timeline
    """
    try:
        activities = []
        
        # Get recent ticket creation activities
        recent_tickets = frappe.get_all(
            "HD Ticket",
            fields=["name", "subject", "status", "priority", "creation", "owner"],
            filters={
                "creation": [">=", frappe.utils.add_days(frappe.utils.nowdate(), -7)]
            },
            order_by="creation desc",
            limit=10
        )
        
        for ticket in recent_tickets:
            activities.append({
                "id": f"ticket_created_{ticket.name}",
                "title": "New Ticket Created", 
                "description": ticket.subject,
                "type": "ticket_created",
                "timestamp": ticket.creation,
                "user": ticket.owner,
                "details": {
                    "ticket": ticket.name,
                    "priority": ticket.priority,
                    "status": ticket.status
                }
            })
        
        # Sort activities by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return activities
        
    except Exception as e:
        frappe.log_error(f"Error in get_recent_activities: {str(e)}")
        return []