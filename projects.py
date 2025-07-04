import json
import os
from datetime import datetime

PROJECTS_FILE = os.path.join('data', 'projects.json')

def load_projects():
    if not os.path.exists(PROJECTS_FILE):
        return []
    with open(PROJECTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_projects(projects):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

def input_date(prompt):
    while True:
        date_str = input(prompt + ' (YYYY-MM-DD): ').strip()
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print('Invalid date format. Please use YYYY-MM-DD.')

def create_project(user):
    print('\n--- Create Project ---')
    title = input('Title: ').strip()
    details = input('Details: ').strip()
    try:
        target = float(input('Total target (EGP): ').strip())
        if target <= 0:
            raise ValueError
    except ValueError:
        print('Target must be a positive number.')
        return
    start_date = input_date('Start date')
    end_date = input_date('End date')
    if end_date < start_date:
        print('End date must be after start date.')
        return
    projects = load_projects()
    project = {
        'id': len(projects) + 1,
        'owner': user['email'],
        'title': title,
        'details': details,
        'target': target,
        'start_date': str(start_date),
        'end_date': str(end_date)
    }
    projects.append(project)
    save_projects(projects)
    print('Project created successfully!')

def view_projects(user):
    print('\n--- All Projects ---')
    projects = load_projects()
    if not projects:
        print('No projects found.')
        return
    for p in projects:
        print(f"ID: {p['id']} | Title: {p['title']} | Owner: {p['owner']} | Target: {p['target']} EGP | {p['start_date']} to {p['end_date']}")
        print(f"  Details: {p['details']}")

def view_own_projects(user):
    print('\n--- Your Projects ---')
    projects = [p for p in load_projects() if p['owner'] == user['email']]
    if not projects:
        print('You have no projects.')
        return
    for p in projects:
        print(f"ID: {p['id']} | Title: {p['title']} | Target: {p['target']} EGP | {p['start_date']} to {p['end_date']}")
        print(f"  Details: {p['details']}")

def edit_project(user):
    view_own_projects(user)
    pid = input('Enter the ID of the project to edit: ').strip()
    projects = load_projects()
    for p in projects:
        if str(p['id']) == pid and p['owner'] == user['email']:
            print('Leave blank to keep current value.')
            title = input(f"Title [{p['title']}]: ").strip() or p['title']
            details = input(f"Details [{p['details']}]: ").strip() or p['details']
            try:
                target_input = input(f"Target [{p['target']}]: ").strip()
                target = float(target_input) if target_input else p['target']
                if target <= 0:
                    raise ValueError
            except ValueError:
                print('Target must be a positive number.')
                return
            start_input = input(f"Start date [{p['start_date']}]: ").strip()
            end_input = input(f"End date [{p['end_date']}]: ").strip()
            start_date = datetime.strptime(start_input, '%Y-%m-%d').date() if start_input else datetime.strptime(p['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(end_input, '%Y-%m-%d').date() if end_input else datetime.strptime(p['end_date'], '%Y-%m-%d').date()
            if end_date < start_date:
                print('End date must be after start date.')
                return
            p['title'] = title
            p['details'] = details
            p['target'] = target
            p['start_date'] = str(start_date)
            p['end_date'] = str(end_date)
            save_projects(projects)
            print('Project updated!')
            return
    print('Project not found or not owned by you.')

def delete_project(user):
    view_own_projects(user)
    pid = input('Enter the ID of the project to delete: ').strip()
    projects = load_projects()
    for i, p in enumerate(projects):
        if str(p['id']) == pid and p['owner'] == user['email']:
            del projects[i]
            save_projects(projects)
            print('Project deleted!')
            return
    print('Project not found or not owned by you.')

def search_projects_by_date():
    print('\n--- Search Projects by Date ---')
    date = input_date('Enter a date to search for')
    projects = load_projects()
    found = False
    for p in projects:
        start = datetime.strptime(p['start_date'], '%Y-%m-%d').date()
        end = datetime.strptime(p['end_date'], '%Y-%m-%d').date()
        if start <= date <= end:
            print(f"ID: {p['id']} | Title: {p['title']} | Owner: {p['owner']} | Target: {p['target']} EGP | {p['start_date']} to {p['end_date']}")
            print(f"  Details: {p['details']}")
            found = True
    if not found:
        print('No projects found for this date.')

def project_menu(user):
    while True:
        print(f"\n--- Project Menu ({user['email']}) ---")
        print('1. Create project')
        print('2. View all projects')
        print('3. View your projects')
        print('4. Edit your project')
        print('5. Delete your project')
        print('6. Search projects by date')
        print('7. Logout')
        choice = input('Select an option: ')
        if choice == '1':
            create_project(user)
        elif choice == '2':
            view_projects(user)
        elif choice == '3':
            view_own_projects(user)
        elif choice == '4':
            edit_project(user)
        elif choice == '5':
            delete_project(user)
        elif choice == '6':
            search_projects_by_date()
        elif choice == '7':
            print('Logging out...')
            break
        else:
            print('Invalid choice. Try again.') 