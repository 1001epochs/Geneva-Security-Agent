import streamlit as st
import speech_recognition as sr
from ai.information_agent import info_agent
from ai.report_agent import report_agent
from ai.violation_agent import violation_agent
import tempfile
import os
from audio_recorder_streamlit import audio_recorder
import time

# Initialize session state more robustly
def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "report_init" not in st.session_state:
        st.session_state.report_init = False
    if "report_generating" not in st.session_state:
        st.session_state.report_generating = False
    if "voice_processed" not in st.session_state:
        st.session_state.voice_processed = False
    if "last_voice_input" not in st.session_state:
        st.session_state.last_voice_input = ""

init_session_state()

# Improved voice processing function
def process_voice_input(audio_bytes):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            fp.write(audio_bytes)
            temp_path = fp.name
        
        # Initialize recognizer with better configuration
        r = sr.Recognizer()
        r.energy_threshold = 4000  # Adjust for better sensitivity
        r.dynamic_energy_threshold = True
        
        with sr.AudioFile(temp_path) as source:
            # Adjust for ambient noise and read audio
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source)
            
            # Use Google Web Speech API
            text = r.recognize_google(audio)
            st.session_state.last_voice_input = text
            return text
            
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try again.")
    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {e}")
    except Exception as e:
        st.error(f"Error processing voice input: {str(e)}")
    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
    return None

# Main app interface
st.title("Security Incident Reporter")

# Initial report submission
if not st.session_state.report_init:
    st.subheader("Report a Security Incident")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        report = st.text_area(
            "Describe the security incident:",
            placeholder="Include date, time, location, people involved, and what happened...",
            height=150
        )
    
    with col2:
        st.write("**Or use voice input:**")
        audio_bytes = audio_recorder(
            pause_threshold=2.0,  # Longer pause before stopping
            text="Click to record",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="2x",
        )
        
        if audio_bytes and not st.session_state.voice_processed:
            with st.spinner("Processing voice input..."):
                voice_text = process_voice_input(audio_bytes)
                if voice_text:
                    report = voice_text
                    st.session_state.last_voice_input = voice_text
                    st.session_state.voice_processed = True    
    
    submit_button = st.button("Submit Report")
    if (submit_button and report.strip()) or st.session_state.voice_processed:
        st.session_state.report = report if report else st.session_state.last_voice_input
        st.session_state.report_init = True
        st.session_state.chat_history.append({"role": "user", "content": st.session_state.report})
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": "Thank you for your report. Please provide more details about the incident, like the date, time, location, and people involved."
        })
        st.session_state.voice_processed = False
        st.rerun()

# Chat interface after initial report
else:
    st.success("Report process initiated. Please provide additional details.")
    
    # Display chat history
    st.subheader("Chat Session")
    chat = st.container()
    with chat:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

    # Report generation phase
    if st.session_state.report_generating:
        with st.spinner("Generating report and legal analysis..."):
            report_data = report_agent(st.session_state.chat_history)
            violation_analysis = violation_agent("\n".join(
                [msg["content"] for msg in st.session_state.chat_history if msg["role"] == "user"]
            ))
            st.session_state.report_data = report_data
            st.session_state.violation_analysis = violation_analysis
        
        st.success("Report generated successfully!")
        st.subheader("Incident Report")
        st.markdown(report_data["report_content"])
        
        st.subheader("Legal Analysis")
        st.markdown(violation_analysis)
        
        col1, col2 = st.columns(2)
        with col1:
            with open(report_data["pdf_path"], "rb") as f:
                st.download_button(
                    "Download PDF Report",
                    f.read(),
                    "security_incident_report.pdf",
                    "application/pdf"
                )
        with col2:
            st.download_button(
                "Download HTML Report",
                report_data["html_content"],
                "security_incident_report.html",
                "text/html"
            )
    
    # Chat interaction phase
    else:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.chat_input("Type your response here...")
        
        with col2:
            st.write("")  # Spacer
            audio_bytes = audio_recorder(
                pause_threshold=2.0,
                text="Record voice",
                recording_color="#e8b62c",
                neutral_color="#6aa36f",
                icon_name="microphone",
                icon_size="1x",
            )
            
            if audio_bytes and not st.session_state.voice_processed:
                with st.spinner("Processing voice input..."):
                    voice_text = process_voice_input(audio_bytes)
                    if voice_text:
                        st.session_state.last_voice_input = voice_text
                        st.session_state.voice_processed = True
        
        # Process any type of input
        if user_input or audio_bytes:
            if st.session_state.voice_processed:
                st.session_state.voice_processed = False
                st.session_state.chat_history.append({
                    "role": "user", 
                    "content": st.session_state.last_voice_input
                })
                audio_bytes = None  # Clear audio bytes after processing
                # Display user input in chat
                with chat:
                    st.chat_message("user").write(st.session_state.last_voice_input)
            else:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                # Display user input in chat
                with chat:
                    st.chat_message("user").write(user_input)
            
            # Get AI response
            agent_response = info_agent(st.session_state.chat_history)
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": agent_response['chat_response']
            })
            # update ui after response
            with chat:
                st.chat_message("assistant").write(agent_response['chat_response'])

            if agent_response['next_step'] == "report":
                st.session_state.report_generating = True

