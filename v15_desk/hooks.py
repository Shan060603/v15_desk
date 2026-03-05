app_name = "v15_desk"
app_title = "v15 Desk"
app_publisher = "Shan Marion Silveo"
app_description = "A v15 desk version of the one from v11"
app_email = "shan.silveo@gmail.com"
app_license = "mit"

# Includes in <head>
# ------------------

# We MUST include the JS and CSS globally so the redirect and purple theme 
# can be applied effectively.
app_include_css = [
    "/assets/frappe/css/fonts/fontawesome/font-awesome.min.css",
    "/assets/v15_desk/css/v15_desktop.css"
]
app_include_js = [
    "/assets/v15_desk/js/desk_redirect.js"
]

# Home Pages
# ----------

# website user home page (by Role)
# This tells Frappe where to send the user after login
role_home_page = {
    "System User": "v15_desktop"
}

# This overrides the default "Home" icon in the sidebar
app_home_page = "v15_desktop"

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True