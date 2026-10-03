import streamlit as st
import requests
import sqlite3


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

connection = sqlite3.connect("tickets.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket TEXT NOT NULL,
    analysis TEXT NOT NULL
)
""")

connection.commit()


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Service Desk",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Service Desk Operations Platform")

st.write(
    "AI-powered incident analysis, troubleshooting, "
    "ticket classification, and escalation assistance."
)


# --------------------------------------------------
# PAGE LAYOUT
# --------------------------------------------------

left_column, right_column = st.columns([2, 1], gap="large")


# --------------------------------------------------
# LEFT SIDE - TICKET ANALYSIS
# --------------------------------------------------

with left_column:

    st.subheader("Submit an IT Support Ticket")

    ticket = st.text_area(
        "Describe the user's issue:",
        placeholder=(
            "Example: User cannot connect to the VPN "
            "while working remotely."
        ),
        height=150
    )

    if st.button("Analyze Ticket", type="primary"):

        if not ticket.strip():
            st.warning("Please enter a ticket description.")

        else:

            with st.spinner("AI is analyzing the ticket..."):

                prompt = f"""
You are an AI assistant supporting a Tier 1 IT Service Desk.

Analyze the following support ticket and provide practical
troubleshooting guidance.

Follow these rules:

- Do not assume the symptom confirms the root cause.
- Start with simple and safe troubleshooting.
- Consider impact and urgency when determining priority.
- Do not automatically classify issues as High or Critical.
- Do not invent company policies or procedures.
- Recommend escalation only when appropriate.

SUPPORT TICKET:

{ticket}

Provide:

1. Issue Category
2. Priority
3. Priority Reason
4. Information Needed
5. Possible Causes
6. Troubleshooting Steps
7. Recommended Resolution
8. Escalation Recommendation

Keep the response practical and appropriate for a
Tier 1 Service Desk Analyst.
"""

                try:

                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "llama3.2:3b",
                            "prompt": prompt,
                            "stream": False
                        },
                        timeout=120
                    )

                    response.raise_for_status()
                    result = response.json()

                    analysis = result["response"]

                    st.subheader("AI Ticket Analysis")
                    st.write(analysis)

                    cursor.execute(
                        """
                        INSERT INTO tickets (ticket, analysis)
                        VALUES (?, ?)
                        """,
                        (ticket, analysis)
                    )

                    connection.commit()

                    st.success("Ticket saved to history.")

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to Ollama. "
                        "Make sure Ollama is running."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "The AI model took too long to respond. "
                        "Please try again."
                    )

                except requests.exceptions.RequestException as error:

                    st.error(
                        f"AI connection error: {error}"
                    )

                except (KeyError, ValueError):

                    st.error(
                        "The AI returned an unexpected response."
                    )


# --------------------------------------------------
# RIGHT SIDE - RECENT TICKETS
# --------------------------------------------------

with right_column:

    st.subheader("📋 Recent Tickets")

    cursor.execute(
        """
        SELECT id, ticket, analysis
        FROM tickets
        ORDER BY id DESC
        LIMIT 10
        """
    )

    saved_tickets = cursor.fetchall()

    if saved_tickets:

        for ticket_id, ticket_text, analysis in saved_tickets:

            short_ticket = ticket_text[:35]

            if len(ticket_text) > 35:
                short_ticket += "..."

            with st.expander(
                f"#{ticket_id} - {short_ticket}"
            ):

                st.write("**Ticket**")
                st.write(ticket_text)

                st.write("**AI Analysis**")
                st.write(analysis)

    else:

        st.info("No tickets analyzed yet.")