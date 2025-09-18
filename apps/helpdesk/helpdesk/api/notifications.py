import frappe
from frappe import _
from helpdesk.utils import agent_only


@frappe.whitelist()
@agent_only
def get_dashboard_notifications():
    """
    Get real-time notifications for the dashboard
    """
    user = frappe.session.user
    
    # Get recent ticket assignments
    assignments = frappe.get_all(
        "HD Ticket",
        fields=["name", "subject", "modified", "_assign"],
        filters={
            "_assign": ["like", f"%{user}%"],
            "modified": [">=", frappe.utils.add_days(frappe.utils.nowdate(), -7)]
        },
        order_by="modified desc",
        limit=5
    )
    
    notifications = []
    
    # Add assignment notifications
    for assignment in assignments:
        notifications.append({
            "name": f"assign_{assignment.name}",
            "title": "New Ticket Assignment",
            "message": f"You've been assigned to: {assignment.subject}",
            "type": "ticket_assigned",
            "action_url": f"/tickets/{assignment.name}",
            "creation": assignment.modified,
            "read": False
        })
    
    # Get SLA breach warnings
    sla_breaches = frappe.db.sql("""
        SELECT name, subject, sla, response_by, resolution_by
        FROM `tabHD Ticket`
        WHERE status IN (
            SELECT name FROM `tabHD Ticket Status` WHERE category = 'Open'
        )
        AND (
            (response_by < NOW() AND first_responded_on IS NULL)
            OR (resolution_by < NOW() AND status NOT IN (
                SELECT name FROM `tabHD Ticket Status` WHERE category = 'Resolved'
            ))
        )
        AND (_assign LIKE %(user)s OR agent_group IN (
            SELECT parent FROM `tabHD Team Agent` WHERE agent = %(user)s
        ))
        ORDER BY creation DESC
        LIMIT 3
    """, {"user": f"%{user}%"}, as_dict=True)
    
    for breach in sla_breaches:
        notifications.append({
            "name": f"sla_{breach.name}",
            "title": "SLA Breach Alert",
            "message": f"SLA breach for: {breach.subject}",
            "type": "sla_breach",
            "action_url": f"/tickets/{breach.name}",
            "creation": frappe.utils.now(),
            "read": False
        })
    
    # Get recent feedback
    recent_feedback = frappe.get_all(
        "HD Ticket",
        fields=["name", "subject", "feedback_rating", "modified"],
        filters={
            "feedback_rating": [">", 0],
            "modified": [">=", frappe.utils.add_days(frappe.utils.nowdate(), -3)],
            "_assign": ["like", f"%{user}%"]
        },
        order_by="modified desc",
        limit=3
    )
    
    for feedback in recent_feedback:
        rating_text = "★" * int(feedback.feedback_rating * 5)
        notifications.append({
            "name": f"feedback_{feedback.name}",
            "title": "New Feedback Received",
            "message": f"{rating_text} for: {feedback.subject}",
            "type": "feedback_received",
            "action_url": f"/tickets/{feedback.name}",
            "creation": feedback.modified,
            "read": False
        })
    
    # Sort by creation time
    notifications.sort(key=lambda x: x["creation"], reverse=True)
    
    return notifications[:10]  # Return top 10 notifications


@frappe.whitelist()
@agent_only
def mark_notification_read(notification_id):
    """
    Mark a specific notification as read
    """
    # In a real implementation, you would store read status in a table
    # For now, we'll just return success
    return {"status": "success"}


@frappe.whitelist()
@agent_only
def mark_all_notifications_read():
    """
    Mark all notifications as read for the current user
    """
    # In a real implementation, you would update read status for all notifications
    return {"status": "success"}