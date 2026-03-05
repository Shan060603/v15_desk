import frappe
from frappe import _
from frappe.desk.desktop import Workspace

# Default icon mapping for common workspaces
DEFAULT_ICONS = {
    "home": "fa-home",
    "accounting": "fa-book",
    "payables": "fa-arrow-left",
    "receivables": "fa-arrow-right",
    "recruitment": "fa-user-tie",
    "buying": "fa-shopping-cart",
    "selling": "fa-store",
    "financial": "fa-chart-line",
    "financial reports": "fa-file-pdf",
    "hrms": "fa-users",
    "hr": "fa-handshake",
    "stock": "fa-boxes",
    "assets": "fa-building",
    "crm": "fa-phone",
    "quality": "fa-check-circle",
    "payroll": "fa-money-bill",
    "salary payout": "fa-wallet",
    "projects": "fa-project-diagram",
    "tools": "fa-wrench",
    "support": "fa-headset",
    "utilities": "fa-cog",
    "loans": "fa-university",
    "leaves": "fa-calendar",
    "website": "fa-globe",
    "website workspace": "fa-globe",
    "build": "fa-cube",
    "manufacturing": "fa-industry",
    "erpnext": "fa-briefcase",
    "erpnext settings": "fa-sliders-h",
    "erp settings": "fa-sliders-h",
    "integrations": "fa-link",
    "erpnext integrations": "fa-plug",
    "setup": "fa-sliders-h",
    "users": "fa-user-circle",
    "expense claims": "fa-receipt",
    "employee lifecycle": "fa-user",
    "shift & attendance": "fa-clock",
    "shift and attendance": "fa-clock",
    "performance": "fa-star",
    "dashboard": "fa-tachometer-alt",
    "welcome workspace": "fa-star",
    "welcome": "fa-star",
}

@frappe.whitelist()
def get_desktop_data():
    # Use correct filters based on Frappe's workspace filtering logic
    workspaces = frappe.get_all("Workspace", 
        filters={
            "public": 1,
            "is_hidden": 0,
            "restrict_to_domain": ["in", [None] + frappe.get_active_domains()],
            "module": ["not in", frappe.get_cached_doc("User", frappe.session.user).get_blocked_modules() + ["Dummy Module"]]
        }, 
        fields=["name", "label", "icon", "indicator_color", "module"],
        order_by="sequence_id asc"
    )
    
    allowed_workspaces = []
    
    for ws in workspaces:
        # Permission check: Only show what the user is allowed to see
        try:
            workspace = Workspace(ws, True)  # True for minimal mode
            if workspace.is_permitted():
                # Get icon - use database value or fallback to default
                icon = ws.get('icon') or ''
                icon = icon.strip() if isinstance(icon, str) else ''
                
                # If no icon or empty, get default based on label/name
                if not icon:
                    icon = get_default_icon(ws.get('label', ''), ws.get('name', ''))
                else:
                    # Ensure icon has fa- prefix if it doesn't already
                    if not icon.startswith('fa-') and not icon.startswith('fa '):
                        icon = f"fa-{icon}"
                
                ws['icon'] = icon
                
                # We fetch the notification count (mocking the red badge logic)
                ws['open_count'] = get_notification_count(ws.name)
                allowed_workspaces.append(ws)
        except frappe.PermissionError:
            continue
            
    return allowed_workspaces

def get_default_icon(label, name):
    """Get default icon for a workspace based on label or name"""
    search_text = f"{label} {name}".lower()
    
    # Check for direct matches first
    for key, icon in DEFAULT_ICONS.items():
        if key == label.lower() or key == name.lower():
            return icon
    
    # Check for partial matches (single word keywords)
    for key, icon in DEFAULT_ICONS.items():
        if key in search_text:
            return icon
    
    # If no match found, use appropriate icon based on keywords
    if any(word in search_text for word in ['home', 'welcome', 'dashboard']):
        return 'fa-home'
    elif any(word in search_text for word in ['account', 'finance', 'payment', 'invoice']):
        return 'fa-book'
    elif any(word in search_text for word in ['buy', 'purchase', 'vendor', 'supplier']):
        return 'fa-shopping-cart'
    elif any(word in search_text for word in ['sell', 'sales', 'customer', 'quote']):
        return 'fa-store'
    elif any(word in search_text for word in ['stock', 'inventory', 'item', 'warehouse']):
        return 'fa-boxes'
    elif any(word in search_text for word in ['hr', 'human', 'employee', 'recruit']):
        return 'fa-user-tie'
    elif any(word in search_text for word in ['project', 'task']):
        return 'fa-project-diagram'
    elif any(word in search_text for word in ['crm', 'lead', 'opportunity', 'contact']):
        return 'fa-phone'
    elif any(word in search_text for word in ['report', 'dashboard', 'analytics']):
        return 'fa-chart-line'
    elif any(word in search_text for word in ['setting', 'config', 'setup']):
        return 'fa-cog'
    elif any(word in search_text for word in ['tool', 'integration', 'api']):
        return 'fa-wrench'
    elif any(word in search_text for word in ['user', 'people', 'team', 'group']):
        return 'fa-users'
    elif any(word in search_text for word in ['build', 'deploy', 'website']):
        return 'fa-cube'
    
    # Default fallback
    return 'fa-th-large'

def get_notification_count(workspace_name):
    # Example: Show notification count for specific modules
    # This can be expanded to count real documents (e.g., Open Leads)
    if workspace_name == "CRM":
        return frappe.db.count("Lead", {"status": "Open"})
    return 0