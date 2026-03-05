frappe.pages['v15_desktop'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Desktop'),
        single_column: true
    });

    // 1. UI Cleanup to match the v12 full-screen look
    // This hides the v15 sidebar and breadcrumbs to let the grid auto-adapt to full width
    $('.layout-side-section').hide();
    $('.page-head').hide();
    $('.layout-main-section').css('padding-top', '0');

    // 2. Setup the Main Container
    // We empty the section first to prevent duplicate grids on refresh
    $(wrapper).find(".layout-main-section").empty().append(`
        <div class="v15-desk-container">
            <div id="v15-grid" class="v15-grid"></div>
        </div>
    `);

    // 3. Load Data from the correct App namespace (v15_desk)
    frappe.call({
        // Updated method path to reflect your actual app name: v15_desk
        method: "v15_desk.v15_desk.page.v15_desktop.v15_desktop.get_desktop_data",
        callback: function(r) {
            if (r.message) {
                const grid = $(wrapper).find("#v15-grid");
                grid.empty(); // Safety clear

                r.message.forEach(m => {
                    // Badge logic for notifications (red dots)
                    let badge = m.open_count > 0 ? `<div class="v15-badge">${m.open_count}</div>` : '';
                    
                    // Fallback to a default blue if no color is defined in the Workspace
                    let icon_color = m.indicator_color || '#3498db';
                    
                    // Format icon - ensure proper Font Awesome format
                    let icon_class = m.icon || 'fa-th-large';
                    
                    // Clean up icon name
                    icon_class = icon_class.trim();
                    if (!icon_class.startsWith('fa-') && !icon_class.includes(' ')) {
                        icon_class = `fa-${icon_class}`;
                    }
                    
                    // Build proper Font Awesome class
                    let fa_class = 'fa ' + icon_class;
                    
                    // Construct the Icon Card
                    let card = $(`
                        <div class="v15-card" title="${__(m.label)}">
                            <div class="v15-icon-wrapper" style="background-color: ${icon_color}">
                                <i class="${fa_class}"></i>
                                ${badge}
                            </div>
                            <div class="v15-text">${__(m.label)}</div>
                        </div>
                    `).appendTo(grid);

                    // Routing to the actual Workspace on click
                    card.on('click', () => {
                        frappe.set_route('Workspaces', m.name);
                    });
                });
            }
        },
        error: function(r) {
            frappe.msgprint(__('Verify that the app "v15_desk" is installed and the python method exists.'));
        }
    });
};