# Resolvexa

<img src="resolvexa_logo.png" alt="Resolvexa logo" width="260">

**Service Desk Expertise. AI Intelligence.**

Resolvexa is an AI-assisted IT support demo built around the employee intake process. Employees describe an issue, answer relevant follow-up questions one at a time, and try simple troubleshooting steps. If they still need help, their answers and attempted steps become a ticket in the Service Desk portal.

## Application Preview

![Resolvexa employee IT support portal](resolvexa.png)

## Features

- Conversational employee intake with short, relevant follow-up questions.
- Guided self-service for common issues, including password resets and mapping network drives.
- Ticket handoff with the employee's description, answers, and troubleshooting outcomes.
- A Service Desk portal for reviewing tickets, updating status and assignment, and recording notes.
- Technician troubleshooting presented one step at a time, with outcomes recorded before continuing.
- A rolling 24-hour activity display, with separate ticket audit history.
- Optional dark mode and an Outlook example for testing the workflow.

## Try the Demo

[Open Resolvexa](https://aiservicedesk.streamlit.app/)

1. Choose **Employee** in the sidebar.
2. Describe a fictional IT issue, or select **Try the Outlook example**.
3. Answer the follow-up questions one at a time.
4. Follow the available self-service guidance and record whether it helped.
5. If the issue remains unresolved, generate a ticket. A non-AI ticket option is available when the AI service is unavailable.
6. Switch to **Service Desk** in the same browser tab to review the ticket and continue troubleshooting.

Use fictional details. Do not enter passwords, verification codes, or confidential information. Tickets are scoped to the browser session for this public demo. Cloud storage is temporary; this is a portfolio demo rather than an authenticated production support system.

## Tech Stack

- Python
- Streamlit
- SQLite
- GroqCloud API
- Requests

## Project Status

Resolvexa is actively being built and tested, drawing on practical Service Desk experience to improve ticket intake and give technicians a clearer starting point.
