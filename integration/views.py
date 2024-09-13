import json
import hmac
import hashlib
import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        secret = settings.GITHUB_WEBHOOK_SECRET
        received_signature = request.headers.get('X-Hub-Signature-256')
        body = request.body

        # Validate the webhook request
        expected_signature = 'sha256=' + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(received_signature, expected_signature):
            return HttpResponse('Invalid signature', status=400)

        payload = json.loads(body)

        # Check if the event is a new issue
        if payload.get('action') == 'opened':
            issue = payload['issue']
            create_asana_task(issue)

        return JsonResponse({'message': 'Event received'}, status=200)

    return HttpResponse(status=405)

def create_asana_task(issue):
    url = "https://app.asana.com/api/1.0/tasks"
    headers = {
        "Authorization": f"Bearer {settings.ASANA_PERSONAL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "data": {
        "workspace": settings.ASANA_WORKSPACE_GID,  # Workspace GID, https://app.asana.com/api/1.0/workspaces
        "name": issue['title'],
        "notes": f"Issue Description: {issue['body']}\nTask ID(Issue URL): {issue['html_url']}",
        "assignee": "me",   # Can only be email, GID or me
        # "assignee": issue['user']['login'],
        "projects": settings.ASANA_PROJECT_GID # Project GID
    }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Task created successfully in Asana")
    else:
        print("Failed to create task:", response.json())
