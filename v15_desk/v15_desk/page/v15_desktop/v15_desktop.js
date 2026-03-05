frappe.pages['v15_desktop'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Desktop'),
        single_column: true
    });

    // 1. UI Cleanup: Remove purple overrides and hide sidebar
    // We reset colors to allow the CSS to take over for a clean light theme
    $('.layout-side-section').hide();
    $('.page-head').hide();
    $('.navbar').css('background-color', ''); // Resetting navbar to standard v15 white
    
    $('.layout-main-section').css({
        'padding-top': '0',
        'max-width': '100%',
        'background-color': '#f4f5f7' // Matches the light gray in our CSS
    });

    // 2. Setup Container
    $(wrapper).find(".layout-main-section").empty().append(`
        <div class="v15-desk-container">
            <div id="v15-grid" class="v15-grid"></div>
        </div>
    `);

    // 3. Load Desktop Data
    frappe.call({
        method: "v15_desk.v15_desk.page.v15_desktop.v15_desktop.get_desktop_data",
        callback: function(r) {
            if (r.message) {
                const grid = $(wrapper).find("#v15-grid");
                grid.empty(); 

                r.message.forEach(m => {
                    // Handle notifications
                    let badge_val = m.open_count > 99 ? '99+' : m.open_count;
                    let badge = m.open_count > 0 ? `<div class="v15-badge">${badge_val}</div>` : '';
                    
                    // Icon logic: Use the pre-formatted string from our Python script
                    // This ensures icons like 'Home' or 'Accounting' finally appear
                    let icon_class = m.icon || 'fa fa-th-large';
                    
                    // Construct Icon Card
                    let card = $(`
                        <div class="v15-card" title="${__(m.label)}">
                            <div class="v15-icon-wrapper">
                                <i class="${icon_class}"></i>
                                ${badge}
                            </div>
                            <div class="v15-text">${__(m.label)}</div>
                        </div>
                    `).appendTo(grid);

                    // Navigation logic
                    card.on('click', () => {
                        frappe.set_route('Workspaces', m.name);
                    });
                });
            }
        }
    });
};