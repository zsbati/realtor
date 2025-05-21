from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def status_badge(status, status_display):
    """
    Returns a Bootstrap badge for visit status
    Usage: {% status_badge status status.get_status_display %}
    """
    status_classes = {
        'scheduled': 'bg-secondary',
        'completed': 'bg-success',
        'cancelled': 'bg-danger',
        'forgotten': 'bg-warning',
    }
    
    badge_class = status_classes.get(status, 'bg-secondary')
    return format_html(
        '<span class="badge {}" data-status="{}">{}</span>',
        badge_class,
        status,
        status_display
    )

@register.simple_tag
def action_buttons(visit, detail_url_name='agenda:visit_detail', 
                 edit_url_name='agenda:visit_edit', delete_url_name='agenda:visit_delete'):
    """
    Returns action buttons for a visit
    Usage: {% action_buttons visit %}
    """
    buttons = [
        format_html(
            '<a href="{}" class="btn btn-sm btn-info me-1" title="Ver detalhes">',
            reverse(detail_url_name, args=[visit.pk])
        ),
        '<i class="fas fa-eye"></i>',
        '</a>',
        
        format_html(
            '<a href="{}" class="btn btn-sm btn-warning me-1" title="Editar">',
            reverse(edit_url_name, args=[visit.pk])
        ),
        '<i class="fas fa-edit"></i>',
        '</a>',
        
        format_html(
            '<a href="{}" class="btn btn-sm btn-danger" title="Eliminar" ' +
            'onclick="return confirm(\'Tem a certeza que quer eliminar esta visita?\')">',
            reverse(delete_url_name, args=[visit.pk])
        ),
        '<i class="fas fa-trash"></i>',
        '</a>'
    ]
    
    return format_html(''.join(buttons))
