import streamlit as st
import requests
import sqlite3
import time

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Service Desk",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# GROQCLOUD CONFIGURATION
# --------------------------------------------------

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Working model verified in GroqCloud
GROQ_MODEL = "qwen/qwen3.8-27b"

# --------------------------------------------------
# REQUEST COOLDOWN
# --------------------------------------------------

COOLDOWN_SECONDS = 30

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

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
# PAGE HEADER
# --------------------------------------------------

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
# LEFT COLUMN - TICKET ANALYSIS
# --------------------------------------------------

with left_column:

    st.subheader("Submit an IT Support Ticket")

    ticket = st.text_area(
        "Describe the user's issue:",
        placeholder="Example: User cannot connect to the VPN while working remotely.",
        height=150,
        max_chars=2000
    )

    if st.button("Analyze Ticket", type="primary"):

        if not ticket.strip():

            st.warning("Please enter a ticket description.")

        else:

            current_time = time.time()

            time_since_last_request = (
                current_time - st.session_state.last_request_time
            )

            if time_since_last_request < COOLDOWN_SECONDS:

                remaining_seconds = int(
                    COOLDOWN_SECONDS - time_since_last_request
                ) + 1

                st.warning(
                    f"Please wait {remaining_seconds} seconds "
                    "before analyzing another ticket."
                )

            else:

                # Start cooldown before calling the API
                st.session_state.last_request_time = current_time

                with st.spinner("AI is analyzing the ticket..."):

                    prompt = f"""
You are an AI assistant supporting a Tier 1 IT Service Desk.

Analyze the following support ticket and provide practical troubleshooting guidance.

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

Keep the response practical and appropriate for a Tier 1 Service Desk Analyst.
"""

                    try:

                        response = requests.post(
                            GROQ_URL,
                            headers={
                                "Authorization": f"Bearer {GROQ_API_KEY}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": GROQ_MODEL,
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": prompt
                                    }
                                ],
                                "temperature": 0.2
                            },
                            timeout=120
                        )

                        response.raise_for_status()

                        result = response.json()

                        analysis = result["choices"][0]["message"]["content"]

                        # DISPLAY AI ANALYSIS

                        st.subheader("AI Ticket Analysis")

                        st.write(analysis)

                        # SAVE TICKET TO DATABASE

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
                            "Could not connect to GroqCloud. "
                            "Please check your internet connection."
                        )

                    except requests.exceptions.Timeout:

                        st.error(
                            "The AI model took too long to respond. "
                            "Please try again."
                        )

                    except requests.exceptions.HTTPError as error:

                        # Show a safe error message without exposing
                        # unnecessary API response details publicly.
                        status_code = error.response.status_code

                        if status_code == 429:
                            st.error(
                                "The AI service is temporarily busy. "
                                "Please try again later."
                            )

                        elif status_code in (401, 403):
                            st.error(
                                "AI service authentication failed. "
                                "Please contact the application owner."
                            )

                        else:
                            st.error(
                                f"The AI service returned an error "
                                f"(status {status_code})."
                            )

                    except requests.exceptions.RequestException:

                        st.error(
                            "An error occurred while contacting "
                            "the AI service."
                        )

                    except (KeyError, ValueError, IndexError):

                        st.error(
                            "The AI returned an unexpected response."
                        )

# --------------------------------------------------
# RIGHT COLUMN - RECENT TICKETS
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

            with st.expander(f"#{ticket_id} - {short_ticket}"):

                st.write("**Ticket**")
                st.write(ticket_text)

                st.write("**AI Analysis**")
                st.write(analysis)

    else:

        st.info("No tickets analyzed yet.")

# --------------------------------------------------
# CLOSE DATABASE CONNECTION
# --------------------------------------------------

connection.close()