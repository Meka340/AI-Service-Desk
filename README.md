# Resolvexa linked demo
Service Desk Expertise. AI Intelligence.

This separate demo connects employee intake to a Service Desk view within one Streamlit app. It does not require changes to app.py, employee_intake.py, or technician_dashboard.py.

## Add to GitHub
Extract this ZIP. Upload the complete `resolvexa_demo` folder to the existing AI-Service-Desk repository. Keep your existing files. The new folder contains:
- resolvexa_demo.py: complete demo application
- requirements.txt: dependencies
- RELEASE_NOTES.md: release notes for this update
- README.md: setup and test instructions

Suggested commit message: Add linked Resolvexa employee and Service Desk demo

The release notes describe a prepared demo, not a verified deployment. Do not mark it released until the public test succeeds.

## Run locally
From the repository folder:

    .\.venv\Scripts\python.exe -m pip install -r resolvexa_demo/requirements.txt
    .\.venv\Scripts\python.exe -m streamlit run resolvexa_demo/resolvexa_demo.py

## Deploy to Streamlit Community Cloud
1. Open https://share.streamlit.io/ and sign in.
2. Choose Create app, then the option for an existing GitHub app/repository.
3. Choose your AI-Service-Desk repository and the branch containing this upload. Use the repository's actual default branch unless you intentionally uploaded elsewhere.
4. Main file path: `resolvexa_demo/resolvexa_demo.py`
5. In Advanced settings choose Python 3.12 and enter your existing Groq API key in Secrets:

    GROQ_API_KEY = "paste-your-existing-key-here"

Optional: set GROQ_MODEL to a model currently available to your Groq account. The existing project default is qwen/qwen3.8-27b. If the default is unavailable, configure an available model; the key remains in Streamlit Secrets.

Optional: set PASSWORD_RESET_URL to an approved HTTPS reset page. Without that, the guide uses the employee's normal company sign-in page, or Microsoft's reset page when the employee explicitly selects a Microsoft work/school account.

Never put a real API key or your actual secrets.toml into GitHub. Do not upload tickets.db or employee data.

6. Choose an available app subdomain, then deploy. The final URL is only established by Streamlit after successful deployment.
7. Enable public viewing for this demo if necessary, then open the final app URL in a private/incognito window and run the test below before adding it to LinkedIn.

## How visitors should test
1. Select Load the Outlook example.
2. Select Show the first step.
3. Use fictional observations. Select I can't do this step to simulate a handoff, or complete the steps and select Still need help. Do not change a real device to test.
4. The app generates a ticket using Groq. If the key/model is unavailable, choose Create ticket without AI.
5. After Ticket generated, select View my ticket in Service Desk.
6. Open the ticket and review the same employee conversation, attempted steps, and observations.
7. With Groq configured, start technician troubleshooting and record an outcome. Add an internal note, then document and confirm a resolution or prepare an escalation.
8. Inspect Activity and Audit history. Activity entries expire individually after 24 hours; audit entries are retained within the temporary demo data.

Each browser session has a different database. Switching roles in the same page preserves the ticket. A new browser tab/session may start a separate demo and will not necessarily show the first tab's tickets. That isolation is intentional for a public portfolio demo; it is not production authentication or durable cloud storage.
