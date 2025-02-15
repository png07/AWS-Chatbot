# Virtual Assistant for SM VITA Website

## Project Overview
This project is developed by **Group 2** as part of the **Post Graduate Diploma in Big Data Analytics (PG-DBDA)** program. Our goal is to create an virtual assistant for the **official SM VITA website**, enhancing user experience by providing **instant support, answering FAQs, and assisting with navigation**.

### Problem Statement
We aim to develop an intelligent chatbot powered by **AWS services** to provide **accurate, context-aware responses** regarding **SMVITA** to prospective candidates. The chatbot will serve as an **interactive tool** that answers common queries related to:
- **About SMVITA**
- CDAC's **programs**
- **Eligibility criteria**
- **Application process**

The knowledge base is built using publicly available resources, including data from **official websites and other relevant sources**. To enhance performance, we gathered a sample set of **expected user questions** to ensure the chatbot is trained effectively.

### Key Features
- **AWS-powered** chatbot leveraging Bedrock services
- **Dynamic responses** using Claude 3 Haiku Foundation Model
- **Vector-based search** for improved answer retrieval
- **Secure and context-aware interactions**
- **Web-based interface** for seamless user engagement

### Team Members
1) Abhay Tripathi - 001
2) Hansika Nemade - 012
3) Mihir Yadav - 019
4) Pooja Nayak - 025
5) Pratik Gurav - 027
6) Saurabh Pardeshi - 037
7) Sidhraj Sinh Zala - 040
8) Tushar Naik - 043
   
## Implementation Steps

### **1. Project Planning & Architecture Design**
- Defined the **problem statement** and **scope**.
- Designed the **system architecture** with AWS services, Bedrock, and Pinecone.
- Finalized **Titan Text Embedding Model** for the knowledge base.

### **2. Data Collection & Preprocessing**
- Gathered publicly available **SM VITA and CDAC related information**.
- Converted data into **structured format (PDFs)**.
- Stored data in **Amazon S3** for easy retrieval.
- Chunked data for **efficient embedding** and vector storage.

### **3. Knowledge Base Creation**
- Embedded text data using **Titan Text Embedding Model**.
- Indexed embeddings in **Pinecone Vector Database**.
- Integrated **Claude 3 Haiku Foundation Model** for reasoning.

### **4. Backend Development**
- Developed **AWS Lambda** functions for chatbot logic.
- Connected Lambda to **Amazon API Gateway** for seamless communication.
- Integrated **Bedrock Agent** to handle queries dynamically.

### **5. Frontend Development**
- Designed an **interactive UI using Streamlit**.
- Integrated UI with **API Gateway** to communicate with backend services.

### **6. Testing & Optimization**
- Conducted **multiple test cases** to validate chatbot responses.
- Fine-tuned **embeddings and query processing** for accuracy.
- Optimized API response times for **better performance**.

### **7. Deployment & Maintenance**
- Deployed the chatbot on **AWS cloud infrastructure**.
- Set up **continuous monitoring and debugging**.
- Provided documentation and a user guide for **future enhancements**.

## **Technology Stack**
  <br>**Frontend** - Streamlit 
  <br>**Backend** - AWS Lambda, API Gateway 
  <br>**AI Model** - Claude 3 Haiku (AWS Bedrock) 
  <br>**Embedding Engine** - Titan Text Embedding Model
  <br>**Vector Database** - Pinecone
  <br>**Storage** - Amazon S3
  <br>**Cloud Services** - AWS Bedrock, Lambda, API Gateway

## Conclusion
This chatbot is designed to **enhance user experience** by providing **instant, context-aware responses** to queries about **SM VITA and its courses**. By leveraging AWS services and a structured knowledge base, we ensure that the chatbot remains **accurate, efficient, and scalable**.

This project showcases **the power of AI and cloud computing** in delivering **intelligent automation** for educational institutions.

