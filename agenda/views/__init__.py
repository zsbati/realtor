from agenda.main_views import dashboard, reports, visit_list, visit_detail, visit_create, visit_edit, visit_delete, export_visits_to_excel
from .contract_views import contract_list, contract_detail, contract_create, contract_edit, contract_delete, export_contracts_to_excel

__all__ = [
    'dashboard', 'reports', 'visit_list', 'visit_detail', 
    'visit_create', 'visit_edit', 'visit_delete', 'export_visits_to_excel',
    'contract_list', 'contract_detail', 'contract_create', 'contract_edit',
    'contract_delete', 'export_contracts_to_excel'
]
