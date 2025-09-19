import frappe
from frappe import _

from helpdesk.utils import agent_only


@frappe.whitelist()
@agent_only
def get_dashboard_data(dashboard_type, filters=None):
    """
    Get dashboard data based on the type and date range.
    """
    user = frappe.session.user
    is_manager = "Agent Manager" in frappe.get_roles(user)

    if not is_manager and (filters.get("agent") != user or filters.get("team")):
        frappe.throw(
            _("You are not allowed to view this dashboard data."),
            frappe.PermissionError,
        )
        return

    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None
    team = filters.get("team") if filters else None
    agent = filters.get("agent") if filters else None

    if agent == "@me":
        agent = frappe.session.user

    if not from_date:
        from_date = frappe.utils.add_days(frappe.utils.nowdate(), -30)
    if not to_date:
        to_date = frappe.utils.nowdate()

    _filters = frappe._dict(
        from_date=from_date,
        to_date=to_date,
        team=team,
        agent=agent,
    )
    conds = ""
    if _filters.team:
        conds += f" AND agent_group='{_filters.team}'"

    if _filters.agent:
        conds += f" AND JSON_SEARCH(_assign, 'one', '{_filters.agent}') IS NOT NULL"

    open_statuses = tuple(
        frappe.get_all(
            "HD Ticket Status",
            filters={"category": "Open"},
            pluck="name",
        )
    )
    resolved_statuses = tuple(
        frappe.get_all(
            "HD Ticket Status",
            filters={"category": "Resolved"},
            pluck="name",
        )
    )

    if dashboard_type == "number_card":
        return get_number_card_data(from_date, to_date, conds, resolved_statuses)
    elif dashboard_type == "master":
        return get_master_dashboard_data(
            from_date, to_date, _filters.team, _filters.agent
        )
    elif dashboard_type == "trend":
        return get_trend_data(
            from_date, to_date, conds, open_statuses, resolved_statuses
        )


def get_number_card_data(from_date, to_date, conds="", resolved_statuses=None):
    """
    Get number card data for the dashboard.
    """

    ticket_chart_data = get_ticket_count(from_date, to_date, conds)
    sla_fulfilled_count = get_sla_fulfilled_count(
        from_date, to_date, conds, resolved_statuses
    )
    avg_first_response_time = get_avg_first_response_time(from_date, to_date, conds)
    avg_resolution_time = get_avg_resolution_time(
        from_date, to_date, conds, resolved_statuses
    )
    avg_feedback_score = get_avg_feedback_score(from_date, to_date, conds)

    return [
        ticket_chart_data,
        sla_fulfilled_count,
        avg_first_response_time,
        avg_resolution_time,
        avg_feedback_score,
    ]


def get_ticket_count(from_date, to_date, conds="", return_result=False):
    """
    Get ticket data for the dashboard.
    """
    diff = frappe.utils.date_diff(to_date, from_date)
    if diff == 0:
        diff = 1

    result = frappe.db.sql(
        f"""
		SELECT
            COUNT(CASE
                WHEN creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
                {conds}
                THEN name
                ELSE NULL
            END) as current_month_tickets,

            COUNT(CASE
                WHEN creation >= %(prev_from_date)s AND creation < %(from_date)s 
                {conds}
                THEN name
                ELSE NULL
            END) as prev_month_tickets
		FROM `tabHD Ticket` # noqa: W604
    """,
        {
            "from_date": from_date,
            "to_date": to_date,
            "prev_from_date": frappe.utils.add_days(from_date, -diff),
        },
        as_dict=1,
    )

    if return_result:
        return result

    current_month_tickets = result[0].current_month_tickets or 0
    prev_month_tickets = result[0].prev_month_tickets or 0

    delta_in_percentage = (
        (current_month_tickets - prev_month_tickets) / prev_month_tickets * 100
        if prev_month_tickets
        else 0
    )

    return {
        "title": "Tickets",
        "value": current_month_tickets,
        "delta": delta_in_percentage,
        "deltaSuffix": "%",
        "negativeIsBetter": True,
        "tooltip": "Total number of tickets created",
    }


def get_sla_fulfilled_count(from_date, to_date, conds="", resolved_statuses=None):
    """
    Get the percent of SLA tickets fulfilled for the dashboard.
    """
    diff = frappe.utils.date_diff(to_date, from_date)
    if diff == 0:
        diff = 1

    result = frappe.db.sql(
        f"""
        SELECT 
            COUNT(CASE 
                WHEN creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY) AND agreement_status = 'Fulfilled'
                {conds}
                THEN name
                ELSE NULL
            END) as current_month_fulfilled,
            COUNT(CASE 
                WHEN creation >= %(prev_from_date)s AND creation < %(from_date)s AND agreement_status = 'Fulfilled'
                {conds}
                THEN name 
                ELSE NULL
            END) as prev_month_fulfilled
        FROM `tabHD Ticket` # noqa: W604
    """,
        {
            "from_date": from_date,
            "to_date": to_date,
            "prev_from_date": frappe.utils.add_days(from_date, -diff),
        },
        as_dict=1,
    )

    current_month_fulfilled = result[0].current_month_fulfilled or 0
    prev_month_fulfilled = result[0].prev_month_fulfilled or 0

    # Only these tickets should be counted
    conds += f" AND status in {resolved_statuses}"

    ticket_count = (
        get_ticket_count(from_date, to_date, conds, True)[0] if len(result) > 0 else 1
    )

    current_month_fulfilled_percentage = (
        current_month_fulfilled / ticket_count.current_month_tickets * 100
        if ticket_count.current_month_tickets
        else 0
    )
    prev_month_fulfilled_percentage = (
        prev_month_fulfilled / ticket_count.prev_month_tickets * 100
        if ticket_count.prev_month_tickets
        else 0
    )
    delta_in_percentage = (
        current_month_fulfilled_percentage - prev_month_fulfilled_percentage
    )
    return {
        "title": "% SLA Fulfilled",
        "value": current_month_fulfilled_percentage,
        "suffix": "%",
        "delta": delta_in_percentage,
        "deltaSuffix": "%",
        "tooltip": "% of tickets created that were resolved within SLA",
    }


def get_avg_first_response_time(from_date, to_date, conds=""):
    """
    first_response_time is the time taken to first respond to a ticket.
    Get average first response time for the dashboard.
    """
    diff = frappe.utils.date_diff(to_date, from_date)
    if diff == 0:
        diff = 1

    result = frappe.db.sql(
        f"""
        SELECT 
            AVG(CASE 
                WHEN creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY) AND first_responded_on IS NOT NULL
                {conds}
                THEN first_response_time / 3600
                ELSE NULL
            END) as current_month_avg,
            AVG(CASE 
                When creation >= %(prev_from_date)s AND creation < %(from_date)s AND first_responded_on IS NOT NULL
                {conds}
                THEN first_response_time / 3600
                ELSE NULL
            END) as prev_month_avg
        FROM `tabHD Ticket` # noqa: W604
    """,
        {
            "from_date": from_date,
            "to_date": to_date,
            "prev_from_date": frappe.utils.add_days(from_date, -diff),
        },
        as_dict=1,
    )

    current_month_avg = result[0].current_month_avg or 0
    prev_month_avg = result[0].prev_month_avg or 0

    delta = current_month_avg - prev_month_avg if prev_month_avg else 0

    return {
        "title": "Avg. First Response",
        "value": current_month_avg,
        "suffix": " hrs",
        "delta": delta,
        "deltaSuffix": " hrs",
        "negativeIsBetter": True,
        "tooltip": "Avg. time taken to first respond to a ticket",
    }


def get_avg_resolution_time(from_date, to_date, conds="", resolved_statuses=None):
    """
    Get average resolution time for the dashboard.
    """
    diff = frappe.utils.date_diff(to_date, from_date)
    if diff == 0:
        diff = 1

    result = frappe.db.sql(
        f"""
        SELECT 
            AVG(CASE 
                WHEN status in {resolved_statuses} AND creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
                {conds}
                THEN CEIL(resolution_time / 86400)
                ELSE NULL
            END) as current_month_avg,
            AVG(CASE 
                When status in {resolved_statuses} AND creation >= %(prev_from_date)s AND creation < %(from_date)s
                {conds}
                THEN CEIL(resolution_time / 86400)
                ELSE NULL
            END) as prev_month_avg
        FROM `tabHD Ticket` # noqa: W604
    """,
        {
            "from_date": from_date,
            "to_date": to_date,
            "prev_from_date": frappe.utils.add_days(from_date, -diff),
        },
        as_dict=1,
    )
    current_month_avg = result[0].current_month_avg or 0
    prev_month_avg = result[0].prev_month_avg or 0

    delta = current_month_avg - prev_month_avg if prev_month_avg else 0
    return {
        "title": "Avg. Resolution",
        "value": current_month_avg,
        "suffix": " days",
        "delta": delta,
        "deltaSuffix": " days",
        "negativeIsBetter": True,
        "tooltip": "Avg. time taken to resolve a ticket",
    }


def get_avg_feedback_score(from_date, to_date, conds=""):
    """
    Get average feedback score for the dashboard.
    """
    diff = frappe.utils.date_diff(to_date, from_date)
    if diff == 0:
        diff = 1

    result = frappe.db.sql(
        f"""
        SELECT 
            AVG(CASE 
                WHEN creation >= %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY) AND feedback_rating > 0
                {conds}
                THEN feedback_rating 
                ELSE NULL
            END) as current_month_avg,
            AVG(CASE 
                WHEN creation >= %(prev_from_date)s AND creation < %(from_date)s AND feedback_rating > 0 
                {conds}
                THEN feedback_rating 
                ELSE NULL
            END) as prev_month_avg
        FROM `tabHD Ticket` # noqa: W604
    """,
        {
            "from_date": from_date,
            "to_date": to_date,
            "prev_from_date": frappe.utils.add_days(from_date, -diff),
        },
        as_dict=1,
    )

    current_month_avg = result[0].current_month_avg or 0
    prev_month_avg = result[0].prev_month_avg or 0

    delta = current_month_avg - prev_month_avg

    return {
        "title": "Avg. Feedback Rating",
        "value": current_month_avg * 5,
        "suffix": "/5",
        "delta": delta * 5,
        "deltaSuffix": " stars",
        "tooltip": "Avg. feedback rating for the tickets resolved",
    }


def get_master_dashboard_data(from_date, to_date, team=None, agent=None):
    filters = {
        "creation": ["between", [from_date, to_date]],
    }
    if team:
        filters["agent_group"] = team
    if agent:
        filters["_assign"] = ["like", f"%{agent}%"]
    team_data = get_team_chart_data(from_date, to_date, filters)
    ticket_type_data = get_ticket_type_chart_data(from_date, to_date, filters)
    ticket_priority_data = get_ticket_priority_chart_data(from_date, to_date, filters)
    ticket_channel_data = get_ticket_channel_chart_data(from_date, to_date, filters)

    return [team_data, ticket_type_data, ticket_priority_data, ticket_channel_data]


def get_team_chart_data(from_date, to_date, filters=None):
    """
    Get team chart data for the dashboard.
    """
    result = frappe.get_all(
        "HD Ticket",
        fields=["agent_group as team", "count(name) as count"],
        filters=filters,
        group_by="agent_group",
        order_by="count desc",
    )
    for r in result:
        if not r.team:
            r.team = "No Team"

    if len(result) < 7:
        return get_pie_chart_config(
            result,
            "Tickets by Team",
            "Percentage of Total Tickets by Team",
            "team",
            "count",
        )
    else:
        return get_bar_chart_config(
            result,
            "Tickets by Team",
            "Total Tickets by Team",
            {"key": "team", "type": "category", "title": "Team", "timeGrain": "day"},
            "Tickets",
            [{"name": "count", "type": "bar"}],
        )


def get_ticket_type_chart_data(from_date, to_date, filters=None):
    """
    Get ticket type chart data for the dashboard.
    """
    result = frappe.get_all(
        "HD Ticket",
        fields=["ticket_type as type", "count(name) as count"],
        filters=filters,
        group_by="ticket_type",
        order_by="count desc",
    )
    # based on length show different chart, if len greater than 5 then show pie chart else bar chart
    if len(result) < 7:
        return get_pie_chart_config(
            result,
            "Tickets by Type",
            "Percentage of Total Tickets by Type",
            "type",
            "count",
        )
    else:
        return get_bar_chart_config(
            result,
            "Tickets by Type",
            "Total Tickets by Type",
            {"key": "type", "type": "category", "title": "Type", "timeGrain": "day"},
            "Tickets",
            [{"name": "count", "type": "bar"}],
        )


def get_ticket_priority_chart_data(from_date, to_date, filters=None):
    """
    Get ticket priority chart data for the dashboard.
    """
    result = frappe.get_all(
        "HD Ticket",
        fields=["priority as priority", "count(name) as count"],
        filters=filters,
        group_by="priority",
        order_by="count desc",
    )
    # based on length show different chart, if len greater than 5 then show pie chart else bar chart
    if len(result) < 7:
        return get_pie_chart_config(
            result,
            "Tickets by Priority",
            "Percentage of Total Tickets by Priority",
            "priority",
            "count",
        )
    else:
        return get_bar_chart_config(
            result,
            "Tickets by Priority",
            "Total Tickets by Priority",
            {
                "key": "priority",
                "type": "category",
                "title": "Priority",
                "timeGrain": "day",
            },
            "Tickets",
            [{"name": "count", "type": "bar"}],
        )


def get_ticket_channel_chart_data(from_date, to_date, filters=None):
    """
    Get ticket channel chart data for the dashboard.
    """
    result = frappe.get_all(
        "HD Ticket",
        fields=["via_customer_portal as channel ", "count(name) as count"],
        filters=filters,
        group_by="via_customer_portal",
        order_by="via_customer_portal desc",
    )

    for row in result:
        row.channel = "Portal" if row.channel == 1 else "Email"

    return get_pie_chart_config(
        result,
        "Tickets by Channel",
        "Percentage of Total Tickets by Channel",
        "channel",
        "count",
    )


def get_trend_data(
    from_date, to_date, conds="", open_statuses=None, resolved_statuses=None
):
    """
    Get trend data for the dashboard.
    """

    ticket_trend_data = get_ticket_trend_data(
        from_date, to_date, conds, open_statuses, resolved_statuses
    )
    feedback_trend_data = get_feedback_trend_data(from_date, to_date, conds)

    return [
        ticket_trend_data,
        feedback_trend_data,
    ]


def get_ticket_trend_data(
    from_date, to_date, conds="", open_statuses=None, resolved_statuses=None
):
    """
    Trend data for tickets in the dashboard. Ticket trend +SLA fulfilled
    """
    if len(open_statuses) == 1:
        open_statuses = f"('{open_statuses[0]}')"
    result = frappe.db.sql(
        f"""
            SELECT 
                DATE(creation) as date,
                COUNT(CASE WHEN status in {open_statuses} THEN name END) as open,
                COUNT(CASE WHEN status in {resolved_statuses} THEN name END) as closed,
                COUNT(CASE WHEN agreement_status = 'Fulfilled' THEN name END) as SLA_fulfilled
            FROM `tabHD Ticket` # noqa: W604
            WHERE creation > %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            {conds}
            GROUP BY DATE(creation)
            ORDER BY DATE(creation)
        """,
        {
            "from_date": from_date,
            "to_date": to_date,
        },
        as_dict=1,
    )
    avg_tickets = get_avg_tickets_per_day(from_date, to_date, conds)
    subtitle = f"Average tickets per day is around {avg_tickets:.0f}"
    return get_bar_chart_config(
        result,
        "Ticket Trend",
        subtitle,
        {"key": "date", "type": "time", "title": "Date", "timeGrain": "day"},
        "Tickets",
        [
            {"name": "closed", "type": "bar"},
            {"name": "open", "type": "bar"},
            {
                "name": "SLA_fulfilled",
                "type": "line",
                "showDataPoints": True,
                "axis": "y2",
            },
        ],
        stacked=True,
        y2Axis={
            "title": "% SLA",
            "yMin": 0,
            "yMax": 100,
        },
    )


def get_feedback_trend_data(from_date, to_date, conds=""):
    """
    Get feedback trend data for the dashboard.
    """
    result = frappe.db.sql(
        f"""
        SELECT 
            DATE(creation) as date,
            AVG(CASE WHEN feedback_rating > 0 THEN feedback_rating END) * 5 as rating,
            COUNT(CASE WHEN feedback_rating > 0 THEN name END) as rated_tickets
        FROM `tabHD Ticket` # noqa: W604
        WHERE 
            creation > %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            {conds}
        GROUP BY DATE(creation)
        ORDER BY DATE(creation)
    """,
        {
            "from_date": from_date,
            "to_date": to_date,
        },
        as_dict=1,
    )

    avg_rating_result = frappe.db.sql(
        f"""
        SELECT 
            AVG(feedback_rating) * 5 as avg_rating
        FROM `tabHD Ticket` # noqa: W604
        WHERE 
            creation BETWEEN %(from_date)s AND DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            {conds}
            AND feedback_rating > 0
    """,
        {
            "from_date": from_date,
            "to_date": to_date,
        },
        pluck=True,
    )
    avg_rating = avg_rating_result[0] if avg_rating_result[0] else 0

    subtitle = f"Average feedback rating per day is around {avg_rating:.1f} stars"

    return get_bar_chart_config(
        result,
        "Feedback Trend",
        subtitle,
        {"key": "date", "type": "time", "title": "Date", "timeGrain": "day"},
        "Rated Tickets",
        [
            {"name": "rated_tickets", "type": "bar"},
            {
                "name": "rating",
                "type": "line",
                "showDataPoints": True,
                "axis": "y2",
                "color": "#48BB74",
            },
        ],
        y2Axis={
            "title": "Rating",
            "yMin": 0,
            "yMax": 5,
        },
    )


def get_pie_chart_config(data, title, subtitle, categoryColumn, valueColumn):
    return {
        "type": "pie",
        "data": data,
        "title": title,
        "subtitle": subtitle,
        "categoryColumn": categoryColumn,
        "valueColumn": valueColumn,
    }


def get_bar_chart_config(
    data, title, subtitle, xAxisConfig, yAxisTitle, series, **kwargs
):
    return {
        "type": "axis",
        "data": data,
        "title": title,
        "subtitle": subtitle,
        "xAxis": xAxisConfig,
        "yAxis": {"title": yAxisTitle},
        "series": series,
        **kwargs,
    }


def get_conditions_from_filters(filters):
    """
    Get conditions from filters.
    """
    conditions = [
        f" AND creation between '{filters['from_date']}' and '{filters['to_date']}'"
    ]

    if filters.get("team"):
        conditions.append(f"agent_group = '{filters['team']}'")
    if filters.get("agent"):
        conditions.append(f"owner = '{filters['agent']}'")

    return " AND ".join(conditions) if conditions else ""


def get_avg_tickets_per_day(from_date, to_date, conds=""):
    """
    Get average tickets per day for the dashboard.
    """
    result = frappe.db.sql(
        f"""
            SELECT 
                COUNT(name) as total_tickets,
                DATEDIFF(DATE_ADD(%(to_date)s, INTERVAL 1 DAY), %(from_date)s) as days
            FROM `tabHD Ticket` # noqa: W604
            WHERE creation > %(from_date)s AND creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
            {conds}
        """,
        {
            "from_date": from_date,
            "to_date": to_date,
        },
        as_dict=1,
    )

    total_tickets = result[0].total_tickets or 0
    days = result[0].days or 1  # Avoid division by zero

    avg_tickets_per_day = total_tickets / days

    return avg_tickets_per_day


@frappe.whitelist()
@agent_only
def get_quick_action_counts():
    """
    Get counts for quick action filters in dashboard
    """
    user = frappe.session.user
    is_manager = "Agent Manager" in frappe.get_roles(user)
    
    # My tickets count
    my_tickets = frappe.db.count(
        "HD Ticket",
        filters={
            "_assign": ["like", f"%{user}%"],
            "status": ["in", frappe.get_all("HD Ticket Status", filters={"category": "Open"}, pluck="name")]
        }
    )
    
    # Team tickets count (if manager)
    team_tickets = 0
    if is_manager:
        team_tickets = frappe.db.count(
            "HD Ticket",
            filters={
                "agent_group": ["in", frappe.get_all("HD Team Member", filters={"user": user}, pluck="parent")],
                "status": ["in", frappe.get_all("HD Ticket Status", filters={"category": "Open"}, pluck="name")]
            }
        )
    
    # High priority tickets
    high_priority = frappe.db.count(
        "HD Ticket",
        filters={
            "priority": "High",
            "status": ["in", frappe.get_all("HD Ticket Status", filters={"category": "Open"}, pluck="name")]
        }
    )
    
    # Overdue tickets
    overdue = frappe.db.sql("""
        SELECT COUNT(name) as count
        FROM `tabHD Ticket`
        WHERE status IN (
            SELECT name FROM `tabHD Ticket Status` WHERE category = 'Open'
        )
        AND (
            (response_by < NOW() AND first_responded_on IS NULL)
            OR (resolution_by < NOW())
        )
    """, as_dict=True)[0].count
    
    # Unassigned tickets
    unassigned = frappe.db.count(
        "HD Ticket",
        filters={
            "_assign": ["is", "not set"],
            "status": ["in", frappe.get_all("HD Ticket Status", filters={"category": "Open"}, pluck="name")]
        }
    )
    
    # Pending feedback
    pending_feedback = frappe.db.count(
        "HD Ticket",
        filters={
            "status": "Waiting for Customer"
        }
    )
    
    return {
        "my_tickets": my_tickets,
        "team_tickets": team_tickets,
        "high_priority": high_priority,
        "overdue": overdue,
        "unassigned": unassigned,
        "pending_feedback": pending_feedback
    }


@frappe.whitelist()
@agent_only
def schedule_dashboard_report(schedule):
    """Persist dashboard scheduling preferences for the current user."""
    if not schedule:
        frappe.throw(_("Schedule details are required."))

    parsed = frappe.parse_json(schedule)
    parsed["updated_at"] = frappe.utils.now()

    key = f"helpdesk_dashboard_schedule::{frappe.session.user}"
    frappe.db.set_default(key, frappe.as_json(parsed))

    return {"status": "success"}


@frappe.whitelist()
@agent_only
def get_dashboard_schedule():
    """Fetch persisted dashboard scheduling preferences."""
    key = f"helpdesk_dashboard_schedule::{frappe.session.user}"
    stored = frappe.db.get_default(key)

    schedule = None
    if stored:
        try:
            schedule = frappe.parse_json(stored)
        except Exception:
            schedule = None

    return {"schedule": schedule}


@frappe.whitelist()
@agent_only
def get_performance_overview(filters=None):
    """
    Get performance overview metrics
    """
    from_date = filters.get("from_date") if filters else frappe.utils.add_days(frappe.utils.nowdate(), -30)
    to_date = filters.get("to_date") if filters else frappe.utils.nowdate()
    
    # Calculate previous period for comparison
    period_diff = frappe.utils.date_diff(to_date, from_date)
    prev_from_date = frappe.utils.add_days(from_date, -period_diff)
    prev_to_date = from_date
    
    # Current period metrics
    current_response_time = get_avg_first_response_time(from_date, to_date)
    current_resolution_rate = get_resolution_rate(from_date, to_date)
    current_csat = get_avg_feedback_score(from_date, to_date)
    
    # Previous period metrics
    prev_response_time = get_avg_first_response_time(prev_from_date, prev_to_date)
    prev_resolution_rate = get_resolution_rate(prev_from_date, prev_to_date)
    prev_csat = get_avg_feedback_score(prev_from_date, prev_to_date)
    
    # Calculate trends
    response_time_trend = calculate_trend(current_response_time.get("value", 0), prev_response_time.get("value", 0))
    resolution_rate_trend = calculate_trend(current_resolution_rate, prev_resolution_rate)
    csat_trend = calculate_trend(current_csat.get("value", 0), prev_csat.get("value", 0))
    
    return {
        "avg_response_time": round(current_response_time.get("value", 0), 1),
        "resolution_rate": round(current_resolution_rate, 1),
        "csat_score": round(current_csat.get("value", 0), 1),
        "response_time_trend": response_time_trend,
        "resolution_rate_trend": resolution_rate_trend,
        "csat_trend": csat_trend
    }


def get_resolution_rate(from_date, to_date):
    """Get resolution rate percentage"""
    total_tickets = frappe.db.count("HD Ticket", filters={
        "creation": ["between", [from_date, to_date]]
    })
    
    resolved_tickets = frappe.db.count("HD Ticket", filters={
        "creation": ["between", [from_date, to_date]],
        "status": ["in", frappe.get_all("HD Ticket Status", filters={"category": "Resolved"}, pluck="name")]
    })
    
    return (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0


def calculate_trend(current, previous):
    """Calculate percentage change between current and previous values"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


@frappe.whitelist()
@agent_only
def get_agent_performance_chart(filters=None):
    """
    Get agent performance chart data
    """
    from_date = filters.get("from_date") if filters else frappe.utils.add_days(frappe.utils.nowdate(), -30)
    to_date = filters.get("to_date") if filters else frappe.utils.nowdate()
    
    result = frappe.db.sql("""
        SELECT 
            JSON_UNQUOTE(JSON_EXTRACT(_assign, '$[0]')) as agent,
            COUNT(name) as tickets_handled,
            AVG(CASE WHEN first_response_time IS NOT NULL THEN first_response_time / 3600 END) as avg_response_time,
            AVG(CASE WHEN feedback_rating > 0 THEN feedback_rating * 5 END) as avg_rating
        FROM `tabHD Ticket`
        WHERE creation BETWEEN %(from_date)s AND %(to_date)s
        AND _assign IS NOT NULL
        AND _assign != '[]'
        GROUP BY JSON_UNQUOTE(JSON_EXTRACT(_assign, '$[0]'))
        ORDER BY tickets_handled DESC
        LIMIT 10
    """, {"from_date": from_date, "to_date": to_date}, as_dict=True)
    
    return {
        "type": "axis",
        "data": result,
        "title": "Agent Performance Comparison",
        "subtitle": "Tickets handled by each agent",
        "xAxis": {"key": "agent", "type": "category", "title": "Agent"},
        "yAxis": {"title": "Tickets Handled"},
        "series": [{"name": "tickets_handled", "type": "bar"}]
    }


@frappe.whitelist()
@agent_only
def get_ticket_velocity_chart(filters=None):
    """
    Get ticket velocity chart showing created vs resolved over time
    """
    from_date = filters.get("from_date") if filters else frappe.utils.add_days(frappe.utils.nowdate(), -30)
    to_date = filters.get("to_date") if filters else frappe.utils.nowdate()
    
    result = frappe.db.sql("""
        SELECT 
            DATE(creation) as date,
            COUNT(name) as created,
            COUNT(CASE WHEN status IN (
                SELECT name FROM `tabHD Ticket Status` WHERE category = 'Resolved'
            ) THEN name END) as resolved
        FROM `tabHD Ticket`
        WHERE creation BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY DATE(creation)
        ORDER BY DATE(creation)
    """, {"from_date": from_date, "to_date": to_date}, as_dict=True)
    
    return {
        "type": "axis",
        "data": result,
        "title": "Ticket Velocity",
        "subtitle": "Tickets created vs resolved over time",
        "xAxis": {"key": "date", "type": "datetime", "title": "Date"},
        "yAxis": {"title": "Number of Tickets"},
        "series": [
            {"name": "created", "type": "line"},
            {"name": "resolved", "type": "line"}
        ]
    }


@frappe.whitelist()
@agent_only
def get_team_performance(filters=None):
    """
    Get team performance data for managers
    """
    user = frappe.session.user
    is_manager = "Agent Manager" in frappe.get_roles(user)
    
    if not is_manager:
        frappe.throw(_("You don't have permission to view team performance."))
    
    from_date = filters.get("from_date") if filters else frappe.utils.add_days(frappe.utils.nowdate(), -30)
    to_date = filters.get("to_date") if filters else frappe.utils.nowdate()
    
    result = frappe.db.sql("""
        SELECT 
            JSON_UNQUOTE(JSON_EXTRACT(t._assign, '$[0]')) as agent,
            u.full_name,
            COUNT(t.name) as tickets_resolved,
            AVG(CASE WHEN t.first_response_time IS NOT NULL THEN t.first_response_time / 3600 END) as avg_response_time,
            AVG(CASE WHEN t.feedback_rating > 0 THEN t.feedback_rating * 5 END) as csat_score,
            (COUNT(CASE WHEN t.agreement_status = 'Fulfilled' THEN t.name END) / COUNT(t.name) * 100) as sla_compliance
        FROM `tabHD Ticket` t
        LEFT JOIN `tabUser` u ON u.name = JSON_UNQUOTE(JSON_EXTRACT(t._assign, '$[0]'))
        WHERE t.creation BETWEEN %(from_date)s AND %(to_date)s
        AND t._assign IS NOT NULL
        AND t._assign != '[]'
        AND t.status IN (
            SELECT name FROM `tabHD Ticket Status` WHERE category = 'Resolved'
        )
        GROUP BY JSON_UNQUOTE(JSON_EXTRACT(t._assign, '$[0]')), u.full_name
        ORDER BY tickets_resolved DESC
    """, {"from_date": from_date, "to_date": to_date}, as_dict=True)
    
    return result


@frappe.whitelist()
@agent_only
def get_recent_activities(page=1, filter_type="All", page_size=20):
    """
    Get recent activities for the dashboard timeline
    """
    user = frappe.session.user
    is_manager = "Agent Manager" in frappe.get_roles(user)
    
    activities = []
    
    # Get recent ticket creation activities
    try:
        recent_tickets = frappe.get_all(
            "HD Ticket",
            fields=["name", "subject", "status", "priority", "creation", "owner", "_assign"],
            filters={
                "creation": [">=", frappe.utils.add_days(frappe.utils.nowdate(), -7)]
            },
            order_by="creation desc",
            limit=int(page_size) // 2
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
    except Exception as e:
        frappe.log_error(f"Error fetching recent tickets: {str(e)}")
    
    # Get recent status changes (simplified approach)
    try:
        recent_updates = frappe.db.sql("""
            SELECT 
                name,
                subject,
                status,
                priority,
                modified,
                modified_by
            FROM `tabHD Ticket`
            WHERE modified >= %(from_date)s
            AND modified != creation
            ORDER BY modified DESC
            LIMIT %(limit)s
        """, {
            "from_date": frappe.utils.add_days(frappe.utils.nowdate(), -3),
            "limit": int(page_size) // 2
        }, as_dict=True)
        
        for update in recent_updates:
            activities.append({
                "id": f"ticket_updated_{update.name}_{update.modified}",
                "title": "Ticket Updated",
                "description": f"Status changed for: {update.subject}",
                "type": "ticket_update",
                "timestamp": update.modified,
                "user": update.modified_by,
                "details": {
                    "ticket": update.name,
                    "status": update.status,
                    "priority": update.priority
                }
            })
    except Exception as e:
        frappe.log_error(f"Error fetching ticket updates: {str(e)}")
    
    # Sort activities by timestamp
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Filter by type if specified
    if filter_type != "All":
        activities = [a for a in activities if a["type"] == filter_type]
    
    return activities[:int(page_size)]


@frappe.whitelist()
def get_dashboard_notifications():
    """Get notifications for the dashboard"""
    user = frappe.session.user
    
    # Get unassigned tickets (no assignment)
    unassigned_count = frappe.db.count('HD Ticket', {
        '_assign': ['is', 'not set'],
        'status': ['not in', ['Closed', 'Resolved']]
    })
    
    # Get overdue tickets
    overdue_count = frappe.db.count('HD Ticket', {
        'status': ['not in', ['Closed', 'Resolved']],
        'resolution_by': ['<', frappe.utils.now()]
    })
    
    # Get new tickets assigned to user (in the last 24 hours)
    new_tickets = frappe.db.count('HD Ticket', {
        '_assign': ['like', f'%{user}%'],
        'status': 'Open',
        'modified': ['>', frappe.utils.add_to_date(frappe.utils.now(), hours=-24)]
    })
    
    notifications = []
    
    if unassigned_count > 0:
        notifications.append({
            'id': 'unassigned',
            'title': f'{unassigned_count} Unassigned Tickets',
            'message': 'These tickets need assignment',
            'type': 'warning',
            'timestamp': frappe.utils.now(),
            'action': 'View Tickets'
        })
    
    if overdue_count > 0:
        notifications.append({
            'id': 'overdue',
            'title': f'{overdue_count} Overdue Tickets',
            'message': 'These tickets are past their due date',
            'type': 'error',
            'timestamp': frappe.utils.now(),
            'action': 'Review Tickets'
        })
    
    if new_tickets > 0:
        notifications.append({
            'id': 'new_assigned',
            'title': f'{new_tickets} New Tickets Assigned',
            'message': 'You have new tickets to work on',
            'type': 'info',
            'timestamp': frappe.utils.now(),
            'action': 'View My Tickets'
        })
    
    return notifications


@frappe.whitelist()
def get_quick_action_counts():
    """Get counts for quick action buttons"""
    user = frappe.session.user
    
    # Get open status names
    open_statuses = frappe.get_all("HD Ticket Status", 
                                  filters={"category": "Open"}, 
                                  pluck="name")
    
    return {
        'my_tickets': frappe.db.count('HD Ticket', {
            '_assign': ['like', f'%{user}%'],
            'status': ['in', open_statuses]
        }),
        'unassigned': frappe.db.count('HD Ticket', {
            '_assign': ['is', 'not set'],
            'status': ['in', open_statuses]
        }),
        'urgent': frappe.db.count('HD Ticket', {
            'priority': 'High', 
            'status': ['in', open_statuses]
        }),
        'overdue': frappe.db.count('HD Ticket', {
            'status': ['in', open_statuses],
            'resolution_by': ['<', frappe.utils.now()]
        })
    }
    
