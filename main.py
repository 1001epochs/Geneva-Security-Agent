# Streamlit frontend

# simple chatbot interface

# step 1 : text area, title submit report
# after you submit, chatbot spawns, and asks you calarifying questions

# after getting all the information, it generates a report
# and gives an opinion whether it is considered a legal violation or not


import streamlit as st
from ai.information_agent import info_agent

st.title("Submit Security Incident Report")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "report_init" not in st.session_state:
    st.session_state.report_init = False
if "report_generating" not in st.session_state:
    st.session_state.report_generating = False


# information to be collected
# date
# time
# location
# individuals involved and detailed description of what happened

if not st.session_state.report_init:
    report = st.text_area("Describe the security incident:")
    if st.button("Submit Report") and report.strip():
        st.session_state.report = report
        st.session_state.report_init = True
        st.session_state.chat_history.append(
            {"role": "user", "content": report}
        )
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "Thank you for using our security incident reporting system. Please provide more details about the incident, like the time and date, the location, any individuals involved and a detailed description of what happened."}
        )
        st.rerun()
else:
    # Chatbot interface
    st.success("Report process initiated. Please clarify the details with our AI Agent.")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(f"**User:** {message['content']}")
        else:
            with st.chat_message("assistant"):
                st.write(f"**AI Agent:** {message['content']}")

    if not st.session_state.report_generating:
        # Chat input
        user_input = st.chat_input("Provide more details:")

    # handle user input
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Ai response
        agent_response = info_agent(st.session_state.chat_history)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": agent_response['chat_response']}
        )
        if agent_response['next_step'] == "report":
            st.info("Report is being generated.")
            st.session_state.report_generating = True
            #  report_agent()
            # violation_agent()


        st.rerun()
