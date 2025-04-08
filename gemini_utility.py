import os
import json
import google.generativeai as genai

#get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_directory}/config.json"
config_data = json.load(open(config_file_path))

#loading the api key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

#CONFIGURING google.generativeai with the api key
genai.configure(api_key=GOOGLE_API_KEY)

#Function to load gemini_pro_model to chatbot
def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-1.5-pro-latest")
    return gemini_pro_model

#function to load gemni_pro_model to image captioning
def gemini_pro_vision_model(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    results = response.text
    return results 


#Function to get embeddings for text
def embedding_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type ="retrieval_document")
    
    embedding_list = embedding["embedding"]
    return embedding_list


#function to get response from gemini-pro LLM
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = gemini_pro_model.generate_content(user_prompt)
    results = response.text
    return results

