import os

import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

from gemini_utility import load_gemini_pro_model
from gemini_utility import gemini_pro_vision_model
from gemini_utility import embedding_model_response
from gemini_utility import gemini_pro_response
#get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))


#setting the page configuration i.e icon of the page
st.set_page_config(
    page_title= "Anto Ai",
    page_icon= "🤖",
    layout="centered"
)

with st.sidebar:
    selected = option_menu(
        "Anto Ai",["ChatBot", "Image Captioning", "Embed Text", "Ask Anything"],
        menu_icon= 'robot', icons=['chat-dots', "image-fill","textarea-t","patch-question"],
        default_index=0 #shows the page that will be selected
    )

#Function to translate role between gemini-pro and streamlit
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


if selected == "ChatBot":
    model = load_gemini_pro_model()

    #initialize chat session in streamlit
    if "chat_session" not in st.session_state:
        st.session_state.chat_session  = model.start_chat(history=[])       

    #streamlit page title
    st.title("🤖 ChatBot")    

    #Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    #Input field for user's message
    user_prompt = st.chat_input('Ask Gemini-Pro...')  

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)   

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        #displaying gemini-pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)   


#Image Captioing page
if selected == "Image Captioning" : 

    #Create a title
    st.title('📷 Image Narrator')   
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg, jpeg", "png"])

    if st.button("Generate Caption"):

        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        default_prompt = "write a short caption for this image" 

        #Getting response from the vision model
        caption = gemini_pro_vision_model(default_prompt, image)

        with col2:
            st.info(caption)   


#Text embedding page
if  selected == "Embed Text":

    st.title("🔡 Embed text")

    #input text box
    input_text= st.text_area(label='',placeholder='Enter the text to get the embeddings')

    if  st.button('Get Embeddings'):
        response = embedding_model_response(input_text)
        st.markdown(response)


#ask me any question
if selected == "Ask Anything" :
    st.title("❔ Ask me a question")

    #text box to enter prompt by the user
    user_prompt = st.text_area(label='',placeholder='Ask Anto...')

    if st.button('Get answer'):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)