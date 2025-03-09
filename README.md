# AwareAI
An AI driven RAG SOC Analyst Assistant - Context Aware


Problem Statement: 
To develop an AI-driven RAG Security Analyst Assistant to help analysts investigate security incidents 
with context, and gain insights on how to respond to them effectively  
Pain Point: 
SOC (Security Operations Team) analysts face significant challenges in effectively managing and 
navigating huge volumes and complexities of alerts. Traditional rule-based systems fail to provide 
contextual insights, leading to prolonged response times and potential misses in analysing the alert. 
In particular: 
1. Security analysts must manually correlate alerts with organizational policies, user behavior, 
and historical logs. 
2. Analysts spend significant time retrieving and analyzing related information for each alert, 
delaying response. 
3. Existing systems often lack the intelligence to recommend actionable steps based on 
context. 
This project proposes an AI-driven assistant that integrates policies, and user behavior and logs into 
a centralized, context-aware system. Using a vector database and generative AI, the assistant will 
provide contextual insights, automate correlations, and recommend responses for security alerts. 
 
Input 
1. Security Alert Details 
2. Contextual Data 
• Policies 
• User Profiles 
• Historical Logs  
 
Output 
1. Automated Contextual Analysis: 
2. Insights and Correlations: 
o Relationships between the alert and stored policies, user data, and logs. 
o Risk assessment based on severity and context. 
2 
 
3. Recommendations: 
o Actionable steps include blocking accounts, investigating IP addresses, or escalating 
incidents. 
 
 
Stage: Data Collection and Embedding 
 
Example Intended Output: 
Alert ID: ALRT--001 
Severity: High 
User: XXXXXXXX 
Event: XXXXXXXXXXXXXXXXX 
Suspicious activity detected on XXXXXXXXXX 
 
Findings: 
1. Policy Violation: XXXXXXXXXXXXXXXXXXXXX 
2. User Context: XXXXXXXXXXXXX 
Recommendations: 
Steps XXXXXXXXXXXXXXXX 
