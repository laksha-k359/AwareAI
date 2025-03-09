import openai
from pinecone import Pinecone
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import json

# Initialize Pinecone instance with your API key
pc = Pinecone(api_key="INSERT_YOUR_PINECONE_API_KEY")
# Initialize OpenAI API with your API key
openai.api_key = "INSERT_YOUR_OPENAI_API_KEY"


# Create or connect to an index
index_name = "security-rag"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to the index
index = pc.Index(index_name)
print("Connected to Pinecone index!")

# Load embedding model from SentenceTransformers
embed_model = SentenceTransformer("all-mpnet-base-v2")

def store_policies_and_users():

    # Hardcoded policies and users
    policies = [
        {"id": "P001", "text": "Users should not log in after 10PM PST except for users with role Security Engineer."},
        {"id": "P002", "text": "Multiple failed logins are not allowed."},
        {"id": "P003", "text": "No logins from external IP addresses."}
    ]
    
    users = [
        {"id": "U001", "name": "Alice Johnson", "role": "Security Engineer"},
        {"id": "U002", "name": "Bob Smith", "role": "Software Engineer"}
    ]

    # Prepare documents for storage
    documents = [{"id": item["id"], "text": item["text"]} for item in policies] + \
                [{"id": user["id"], "text": json.dumps(user)} for user in users]

    # Generate embeddings and upsert into Pinecone
    for doc in documents:
        embedding = embed_model.encode(doc["text"]).tolist()
        index.upsert([(doc["id"], embedding, {"text": doc["text"]})])

    print("Policies and users stored in Pinecone!")




def retrieve_relevant_info(alert_text):
    """Retrieve relevant policy and user context based on the security alert"""
    store_policies_and_users()
    alert_embedding = embed_model.encode(alert_text).tolist()

    # Query Pinecone for top 4 most relevant documents using keyword arguments
    results = index.query(
        vector=alert_embedding,  
        top_k=4,                 
        include_metadata=True    
    )

    # Extract relevant text (policy or user data) from the query results
    relevant_chunks = [match["metadata"]["text"] for match in results["matches"]]
    return relevant_chunks



def process_alert_and_generate_insights(alert_json):
    """Process security alert in JSON format and generate actionable insights"""

    # Extract alert details
    alert_id = alert_json.get("alert_id")
    timestamp = alert_json.get("timestamp")
    user_id = alert_json.get("user_id")
    user_name = alert_json.get("user_name")
    description = alert_json.get("description")
    ip_address = alert_json.get("ip_address")
    location = alert_json.get("location")
    severity = alert_json.get("severity")
    status = alert_json.get("status")

    # Construct the alert's description for embedding
    alert_text = f"""
    Alert ID: {alert_id}
    Timestamp: {timestamp}
    User: {user_name} (ID: {user_id})
    Description: {description}
    IP Address: {ip_address}
    Location: {location}
    Severity: {severity}
    Status: {status}
    """

    # Retrieve relevant context from Pinecone
    relevant_chunks = retrieve_relevant_info(alert_text)

    # Construct the prompt for GPT
    prompt = f"""
    Security Alert: {alert_text}

    Relevant Policies & User Data:
    {relevant_chunks}

    Based on this information, provide a security analysis and recommended actions.
    """

    
    response = openai.chat.completions.create(
        model="gpt-4",    
        messages=[{
            "role": "system",
            "content": "You are a security analyst providing incident response insights."
        },
        {
            "role": "user",
            "content": prompt
        }],
        max_tokens=500,   
        temperature=0.1  
    )

    return response  # Extract and return the response text

def format_insights(insights_response):
    """Format the response content nicely."""
    content = insights_response.choices[0].message.content

    formatted_content = f"""
    Security Analysis:

    {content}

    Recommendations:
    """

    recommendations = content.split("Recommendations:")[-1].strip()
    formatted_content += recommendations
    return formatted_content