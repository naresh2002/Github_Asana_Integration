# GitHub-Asana Integration

A Django-based service that integrates GitHub and Asana to automatically create tasks in Asana whenever a new issue is created in GitHub.  
The integration utilizes **GitHub Webhooks** to detect new issues and **Asana REST APIs** to create corresponding tasks in Asana.  

## Overview

The service listens for new issue events in GitHub via webhooks and creates tasks in Asana with details such as the issue title, description, URL, and creator. It ensures validation of incoming requests using a secret key to secure the webhook communication.

## Installation Requirements

1. **Django** and **Requests**  
    ```bash
    pip install django requests
    ```

2. **python-decouple** for managing environment variables securely.  
    ```bash
    pip install python-decouple
    ```

## How to Run This Project

### Step 1: Clone the Repository

1. Clone the repository to your local machine.  
    ```bash
    git clone https://github.com/naresh2002/github_asana_integration.git
    ```

2. Navigate to the project directory.  
    ```bash
    cd github_asana_integration
    ```

### Step 2: Configure Environment Variables

1. Create a `.env` file in the root directory and add the following configuration:  
    ```plaintext
    ASANA_PERSONAL_ACCESS_TOKEN={ASANA_PERSONAL_ACCESS_TOKEN}
    ASANA_WORKSPACE_GID={ASANA_WORKSPACE_GID}
    ASANA_PROJECT_GID={ASANA_PROJECT_GID}
    GITHUB_WEBHOOK_SECRET={GITHUB_WEBHOOK_SECRET}
    ```
    Get ASANA_PERSONAL_ACCESS_TOKEN as described in Step 3 below.  
    Get ASANA_WORKSPACE_GID from https://app.asana.com/api/1.0/workspaces.  
    Get ASANA_PROJECT_GID from asana tasks URL i.e. https://app.asana.com/0/{PROJECT_GID}/{TASK_GID}, the project GID is the first set of numbers after /0/.  
    Get GITHUB_WEBHOOK_SECRET as from Step 4 below.  

3. These environment variables will be used to authenticate and manage the Asana API requests and validate GitHub webhook events.

### Step 3: Set Up Asana Personal Access Token (PAT)

1. Go to your [Asana Developer App Console](https://app.asana.com/-/developer_console) and generate a Personal Access Token (PAT).
2. Copy the PAT and add it to the `.env` file as `ASANA_PERSONAL_ACCESS_TOKEN`.
3. Ensure the token has permissions to create tasks within the specified workspace.

### Step 4: Set Up GitHub Webhook

1. Go to your GitHub repository settings, and under **Webhooks**, click **Add webhook**.
2. Set the **Payload URL** to your ngrok URL followed by `/webhook` (e.g., `http://<ngrok_url>/webhook`).  
   For eg. **https://7796-2401-4900-883a-c6b1-9f5e-a754-3686-c3aa.ngrok-free.app/webhook**
3. Set the **Content type** to `application/json`.
4. Set the **Secret** field with the `GITHUB_WEBHOOK_SECRET` value from your `.env` file.
5. Choose the **Event** to trigger: Select **Issues** to ensure the webhook only triggers when a new issue is created.

### Step 5: Set Up Ngrok

1. Install ngrok if not already installed:  
    ```bash
    sudo apt install ngrok
    ```

2. Run ngrok to expose your local Django server to the internet:  
    ```bash
    ngrok http 8000
    ```

3. Copy the provided `https` URL and use it as the Payload URL in your GitHub webhook configuration.

### Step 6: Run the Django Application

1. Run migrations to set up the database:  
    ```bash
    python manage.py migrate
    ```

2. Start the Django server:  
    ```bash
    python manage.py runserver
    ```

3. Your application will now listen for incoming GitHub events at the `/webhook` endpoint.

### Step 7: Test the Integration

1. Create a new issue in your GitHub repository.
2. Check Asana to see if a new task has been created with the issue details.

## Endpoint

1. **GitHub Webhook Listener** [POST]  

   ``` /webhook ```  

   This endpoint receives payloads from GitHub when a new issue is created and triggers the Asana task creation process. 

## Summary

This project integrates GitHub with Asana, allowing for seamless task creation in response to new GitHub issues. The integration uses webhooks to detect events and Asana REST APIs to manage task creation, ensuring proper validation and security.

Follow the provided steps to configure the environment, set up the necessary tokens and secrets, and run the application. Use the GitHub webhook and Asana API guides linked below for additional support:

- [GitHub Webhooks Guide](https://docs.github.com/en/webhooks)
- [Asana API Documentation](https://developers.asana.com/reference/rest-api-reference)

Ensure all configuration steps are correctly followed to establish a secure and functioning integration.
