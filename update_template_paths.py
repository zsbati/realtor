import os
import re

def update_template_paths():
    # Directory containing the template files
    template_dir = os.path.join('agenda', 'templates', 'agenda')
    
    # Files to update
    template_files = [
        'dashboard.html',
        'visit_list.html',
        'visit_detail.html',
        'visit_form.html',
        'reports.html',
        'login.html',
        'logout.html',
        'contract_list.html',
        'contract_detail.html',
        'contract_form.html',
        'contract_confirm_delete.html',
        os.path.join('registration', 'password_change.html')
    ]
    
    # Update each template file
    for template_file in template_files:
        file_path = os.path.join(template_dir, template_file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update the extends tag to use the correct path
            updated_content = re.sub(
                r"{%\s*extends\s*['\"]base\.html['\"]\s*%}",
                '{% extends \'agenda/base.html\' %}',
                content
            )
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {file_path}")
        else:
            print(f"File not found: {file_path}")

if __name__ == '__main__':
    update_template_paths()
