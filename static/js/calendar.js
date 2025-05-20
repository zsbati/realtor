document.addEventListener('DOMContentLoaded', function() {
    // Initialize the calendar when the DOM is fully loaded
    if (document.getElementById('calendar')) {
        initializeCalendar();
    }
});

function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    
    // Initialize the calendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        },
        buttonText: {
            today: 'Hoje',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia',
            list: 'Lista'
        },
        firstDay: 1, // Start the week on Monday
        height: 'auto',
        contentHeight: 'auto',
        aspectRatio: 1.5,
        nowIndicator: true,
        navLinks: true,
        dayMaxEventRows: 2,
        dayMaxEvents: 3,
        events: {
            url: '/api/visits/calendar/',
            failure: function() {
                console.error('Error loading events');
            }
        },
        loading: function(isLoading) {
            const loadingEl = document.getElementById('loading');
            if (loadingEl) {
                loadingEl.style.display = isLoading ? 'flex' : 'none';
            }
        },
        eventClick: function(info) {
            // When an event is clicked, redirect to the visit detail page
            if (info.event.url) {
                info.jsEvent.preventDefault();
                window.location.href = info.event.url;
            }
        },
        eventContent: function(arg) {
            // Customize how events are displayed
            let timeText = '';
            if (arg.event.start) {
                timeText = arg.event.start.toLocaleTimeString('pt-BR', { 
                    hour: '2-digit', 
                    minute: '2-digit',
                    hour12: false
                }) + ' ';
            }
            
            const title = document.createElement('div');
            title.className = 'fc-event-main';
            title.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-${getEventIcon(arg.event.extendedProps.visit_type)} me-1"></i>
                    <div class="text-truncate" style="max-width: 100%;">
                        <div class="fw-bold text-truncate" style="max-width: 100%;">${arg.event.title}</div>
                        <small class="text-white-50 d-block text-truncate" style="font-size: 0.7em;">
                            ${timeText}${arg.event.extendedProps.address || ''}
                        </small>
                    </div>
                </div>
            `;
            return { domNodes: [title] };
        },
        dateClick: function(info) {
            // When a date is clicked, redirect to create a new visit
            const date = info.date;
            const formattedDate = date.toISOString().split('T')[0];
            window.location.href = `/visit/new/?date=${formattedDate}`;
        },
        eventClassNames: function(arg) {
            // Add custom class based on visit type
            return ['fc-event-' + arg.event.extendedProps.visit_type];
        },
        eventDidMount: function(arg) {
            // Add tooltip for events
            if (arg.event.extendedProps.description) {
                new bootstrap.Tooltip(arg.el, {
                    title: arg.event.extendedProps.description,
                    placement: 'top',
                    trigger: 'hover',
                    container: 'body'
                });
            }
        }
    });

    // Render the calendar
    calendar.render();
    
    // Handle window resize
    window.addEventListener('resize', function() {
        calendar.updateSize();
    });
}

function getEventIcon(visitType) {
    // Return appropriate icon based on visit type
    switch(visitType) {
        case 'visit':
            return 'home';
        case 'phone':
            return 'phone';
        case 'email':
            return 'envelope';
        default:
            return 'calendar';
    }
}
