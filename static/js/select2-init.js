// Initialize Select2 for all select elements
$(document).ready(function() {
    $('select').select2({
        theme: 'bootstrap-5',
        width: '100%'
    });

    // Handle visit detail page links
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('a[href*="visit_detail"]').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                // Simply redirect to the visit detail page
                window.location.href = this.href;
            });
        });
    });
});
