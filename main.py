####################################################################
#!pip install openai pinecone-client sentence-transformers streamlit
#Insert your openAI and Pinecone API keys in the backend.py file
####################################################################

import streamlit as st
import json
import os
import openai
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from backend import store_policies_and_users,process_alert_and_generate_insights, format_insights  


st.title(":blue[AwareAI]")


st.subheader("Contextualizing Security Repsonse", divider="gray")
# File Uploader
uploaded_file = st.file_uploader("Upload a file", type="json")

if uploaded_file:
    st.write(f"Uploaded file: {uploaded_file.name}")

    # Submit button
    if st.button("Submit"):
        # Save the file to local storage
        save_path = f"./{uploaded_file.name}"  # Modify path as needed
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File saved successfully to {save_path}")

        # Read the content of the uploaded JSON file
        with open(save_path, "r") as file:
            try:
                security_alert_json = json.load(file)
                st.write("Security alert loaded successfully!")

                # Call the backend processing function with the loaded JSON
                insights = process_alert_and_generate_insights(security_alert_json)

                # Format and display the insights
                formatted_insights = format_insights(insights)
                st.write(formatted_insights)
                
            except json.JSONDecodeError:
                st.error("Error decoding JSON from the uploaded file. Please check the file format.")