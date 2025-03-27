import streamlit as st
import requests
import json

# Base URL for your Flask API
API_URL = "https://letsdoitagain.onrender.com"

# Streamlit UI Elements
st.title("Email Analysis Application")

# Email Content Input
email_content = st.text_area("Enter the email content here:", height=300)

# Features to enable (checkboxes)
features = {
    "highlights": st.checkbox("Summarize Email", value=True),
    "response": st.checkbox("Generate Professional Response", value=True),
    "tone": st.checkbox("Detect Tone", value=True),
    "task_extraction": st.checkbox("List Actionable Tasks", value=True),
    "subject_recommendation": st.checkbox("Suggest Subject Line", value=True),
    "clarity": st.checkbox("Rate Clarity", value=True),
    "complexity_reduction": st.checkbox("Simplify Email", value=True),
    "scenario_responses": st.checkbox("Scenario-Based Response", value=True),
    "sentiment": st.checkbox("Sentiment Analysis", value=True),
    "phishing_detection": st.checkbox("Detect Phishing Links", value=True),
    "sensitive_info_detection": st.checkbox("Detect Sensitive Info", value=True),
    "confidentiality_rating": st.checkbox("Confidentiality Rating", value=True),
    "bias_detection": st.checkbox("Detect Biases", value=True),
    "conflict_detection": st.checkbox("Detect Conflicts", value=True),
    "argument_mining": st.checkbox("Analyze Arguments", value=True)
}

scenario = st.selectbox("Select Scenario for Response Generation", options=["General", "Customer Support", "Business Proposal", "Complaint"])

# Button to submit analysis
if st.button("Analyze Email"):
    # Prepare data for the API call
    data = {
        "email_content": email_content,
        "features": {key: val for key, val in features.items()},
        "scenario": scenario
    }

    try:
        # Make the API request to the Flask backend
        response = requests.post(f"{API_URL}/analyze", json=data)
        if response.status_code == 200:
            result = response.json()
            st.subheader("Analysis Results")
            
            # Display results in an organized way
            for key, value in result.items():
                if value is not None:
                    st.write(f"**{key.replace('_', ' ').title()}**: {value}")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error during request: {str(e)}")

# File upload section for attachments
st.subheader("Analyze Email Attachments")
attachment_file = st.file_uploader("Upload an attachment (PDF, DOCX, TXT)", type=["pdf", "docx", "txt", "eml", "msg"])

if attachment_file:
    try:
        files = {'file': attachment_file}
        attachment_analysis_response = requests.post(f"{API_URL}/analyze_attachment", files=files)
        if attachment_analysis_response.status_code == 200:
            attachment_data = attachment_analysis_response.json()
            st.write("Attachment Analysis Results")
            st.write(attachment_data.get("attachment_analysis"))
        else:
            st.error(f"Error: {attachment_analysis_response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error during request: {str(e)}")

# File upload section for metadata extraction
st.subheader("Extract Email Metadata")
email_file = st.file_uploader("Upload an email file (EML or MSG)", type=["eml", "msg"])

if email_file:
    try:
        files = {'email_file': email_file}
        metadata_response = requests.post(f"{API_URL}/extract_metadata", files=files)
        if metadata_response.status_code == 200:
            metadata_data = metadata_response.json()
            st.write("Email Metadata")
            st.write(metadata_data.get("email_metadata"))
        else:
            st.error(f"Error: {metadata_response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error during request: {str(e)}")

# Download results buttons
st.subheader("Download Analysis Results")

# Button for JSON download
if st.button("Download JSON Analysis"):
    try:
        download_response = requests.post(f"{API_URL}/download_json", json=data)
        if download_response.status_code == 200:
            st.download_button(
                label="Download JSON",
                data=download_response.content,
                file_name="analysis.json",
                mime="application/json"
            )
        else:
            st.error(f"Error: {download_response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error during request: {str(e)}")

# Button for PDF download
if st.button("Download PDF Analysis"):
    try:
        download_response = requests.post(f"{API_URL}/download_pdf", json=data)
        if download_response.status_code == 200:
            st.download_button(
                label="Download PDF",
                data=download_response.content,
                file_name="analysis.pdf",
                mime="application/pdf"
            )
        else:
            st.error(f"Error: {download_response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error during request: {str(e)}")
