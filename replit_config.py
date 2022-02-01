import os
import requests

from getpass import getpass

PYCL_BASE_URL = os.getenv('PYCL_BASE_URL', 'https://api.pythonclassic.com')

def authenticate():
    email = os.getenv('PYCL_EMAIL')
    if not email:
        email = input('Email: ')
    password = os.getenv('PYCL_PASSWORD')
    if not password:
        password = getpass('Password: ')
    resp = requests.post(f'{PYCL_BASE_URL}/login', json={
        'email': email,
        'password': password
    })
    return resp.ok, resp.json()


def list_assessments(auth_token):
    resp = requests.get(
        f'{PYCL_BASE_URL}/assessment',
        headers={'Authorization': f'Bearer {auth_token}'})
    return resp.ok, resp.json()


def get_assessment(assessment_id, auth_token):
    resp = requests.get(
        f'{PYCL_BASE_URL}/assessment/{assessment_id}',
        headers={'Authorization': f'Bearer {auth_token}'})
    return resp.ok, resp.json()


def checkout_to_branch(local_branch):
    stream = os.popen(f'git checkout {local_branch}')
    return stream.read()


def update_replit_url(assessment_id, replit_url, auth_token):
    resp = requests.patch(
        f'{PYCL_BASE_URL}/assessment/{assessment_id}',
        json={'replit_url': replit_url},
        headers={'Authorization': f'Bearer {auth_token}'})
    return resp.ok, resp.json()


if __name__ == '__main__':
    authenticated = False
    while authenticated is False:
        authenticated, data = authenticate()
        if not authenticated:
            print(
                f'\n{data.get("message")}'
                '\n\nFailed to authenticate, try again:\n')

    auth_token = data.get('access_token')
    ok, data = list_assessments(auth_token)
    if not ok:
        print(f'Failed to get resources\n{data.get("message")}')
        exit()

    assessments = data['data']
    
    print(f'Select a project to import:\n')
    for i, item in enumerate(assessments):
        print(f'({i+1}) {item["topic"]}\n\t* {item["description"][:70]}')

    selected = False
    while not selected:
        project_number = input('Input exectly one digit: ')
        if not project_number.isnumeric():
            print(f'Not a valid numeric input: {project_number}')
            continue
        try:
            project = assessments[int(project_number)-1]
        except IndexError:
            print('Select a number from the list above')
            continue
        selected = True

    ok, data = get_assessment(project['id'], auth_token)
    if not ok:
        print(f'Failed to get resources\n{data.get("message")}')
        exit()

    assessment = data['data']
    feedback = assessment.get('feedback')
    if not feedback or not feedback['source_url']:
        print('This project is not ready to be imported. You need to complete all tasks and submit the result.')
        exit()
    try:
        local_branch = feedback['source_url'].split('tree/')[-1]
    except Exception:
        print(f'Failed to import project.')
        exit()

    output = checkout_to_branch(local_branch)

    if 'Your branch is up to date' not in output:
        print(f'Failed to switch to local git branch. {output}')
        exit()
    # update feedback with replit url
    repl_url = f'https://replit.com/@{os.environ["REPL_OWNER"]}/{os.environ["REPL_SLUG"]}'
    ok, data = update_replit_url(project['id'], repl_url, auth_token)
    if not ok:
        print(f'Failed to connect this repl to your pythonclassic account. {data.get("message")}')
