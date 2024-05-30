import streamlit as st 
import logging
import model_handler as model_handler
import secret
# from streamlit_chat import message
# from streamlit.components.v1 import html
import numpy as np

# import prompt generator module
import market_sectors.sns as sns
import market_sectors.story as story

# Set up logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

TONE = {
    'Happy': ['happy','cheerful'],
    'Horror': ['sad','pessimistic','horror'],
    'Young': ['teenager','playful','emotional'],
    'Rebellious': ['emotional','mad']
}

def main():
    st.title("Welcome to Lucky 8 Banking!")
    st.header("Chat with our friendly chatbot Payton")

    # message("Hello there! My name is Payton. How can I help you today?")
    # message("Here are examples of things I can help you with")

    message = st.chat_message("assistant")
    message.write("Hello! What can I help you with today?")
    # message.bar_chart(np.random.randn(30, 3))

    prompt = st.chat_input("Enter your question here")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")

    # with st.container():
    #     st.text_input("User Input:", on_change=on_input_change, key="user_input")

    with st.form('blog_generator'):
        body = st.text_area("Objective of the story or postings")
        keyword = st.text_area("What keywords do you have in mind?")
        tone = st.radio("What's You r Mood Today?", list(TONE.keys()))
        submitted = st.form_submit_button('Write')

        if not open_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')

        model_name ="gpt-3.5-turbo-16k"
        if submitted and body:
            if body and tone:
                try:
                    prompt = story.story_prompt(body,keyword,tone)  # TODO this is the function to add
                    response = model_handler.openai_api(prompt, model=model_name, temperature=0.7, top_p=1.0, n=1, stream=False)
                    post = sns.sns_prompt(response,keyword)
                    response1 = model_handler.openai_api(post, model=model_name, temperature=0.7, top_p=1.0, n=1, stream=False)

                    col1,col2 = st.columns(2)
                    with col1:
                        st.subheader("Your Story~")
                        st.info(response)
                    with col2:
                        st.subheader("Your Posting~")
                        st.info(response1)
                except Exception as e:
                    logging.error(f"Error generating prompt or response: {e}")
                    st.error("Error generating prompt or response. Please try again later.")
        else:
            st.error("Start Being Creative!")

if __name__ == "__main__":
    open_api_key = secret.acn_token
    main()


