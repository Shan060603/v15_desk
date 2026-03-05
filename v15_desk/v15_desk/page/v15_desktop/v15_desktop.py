import frappe
from frappe import _
from frappe.desk.desktop import Workspace

# Standard mapping to ensure modules always have a fallback icon
DEFAULT_ICONS = {
    "home": "fa-getting-started",
    "accounting": "fa-calculator",
    "payables": "fa-arrow-left",
    "recruitment": "fa-user-plus",
    "receivables": "fa-arrow-right",
    "buying": "fa-shopping-cart",
    "selling": "fa-tag",
    "stock": "fa-box",
    "assets": "fa-city",
    "crm": "fa-handshake",
    "projects": "fa-rocket",
    "tools": "fa-calendar-alt",
    "support": "fa-exclamation-circle",
    "setup": "fa-sliders-h",
    "hr": "fa-users",
    "payroll": "fa-money-check-alt",
    "manufacturing": "fa-tools",
    "website": "fa-globe",
    "pos": "fa-credit-card",
    "data import": "fa-cloud-upload-alt",
    "learn": "fa-video",
}

@frappe.whitelist()
def get_desktop_data():
    workspaces = frappe.get_all("Workspace", 
        filters={
            "public": 1,
            "is_hidden": 0,
            "restrict_to_domain": ["in", [None] + frappe.get_active_domains()],
        }, 
        fields=["name", "label", "icon", "indicator_color", "module", "sequence_id"],
        order_by="sequence_id asc"
    )
    
    blocked_modules = frappe.get_cached_doc("User", frappe.session.user).get_blocked_modules()
    allowed_workspaces = []
    
    for ws in workspaces:
        if ws.module in blocked_modules:
            continue

        try:
            if frappe.has_permission("Workspace", doc=ws.name):
                # 1. Get raw icon or find a default
                raw_icon = ws.get('icon') or get_default_icon(ws.get('label', ''), ws.get('name', ''))
                
                # 2. Force full FontAwesome class string (e.g., "fa fa-home")
                # This fixes the "blank icons" issue seen in your previous screenshot
                if not raw_icon.startswith('fa '):
                    if raw_icon.startswith('fa-'):
                        ws['icon'] = f"fa {raw_icon}"
                    else:
                        ws['icon'] = f"fa fa-{raw_icon}"
                else:
                    ws['icon'] = raw_icon

                ws['open_count'] = get_notification_count(ws.name)
                allowed_workspaces.append(ws)
        except Exception:
            continue
            
    return allowed_workspaces

def get_default_icon(label, name):
    search_text = f"{label} {name}".lower()
    for key, icon in DEFAULT_ICONS.items():
        if key in search_text:
            return icon
    return 'fa-th-large'

def get_notification_count(workspace_name):
    if workspace_name == "CRM":
        return frappe.db.count("Lead", {"status": "Open"})
    elif workspace_name == "Selling":
        return frappe.db.count("Sales Order", {"status": "To Deliver and Bill"})
    return 0