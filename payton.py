import streamlit as st
import model_handler as model_handler
import logging
import secret

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

firstmessage = f"""
Welcome to Lucky 8 Bank! I'm Payton👋 How can I assist you today?\n
You can ask me questions like:\n
What types of accounts do you offer, such as checking, savings, or money market?\n
Are there any monthly fees associated with these accounts?\n
What are the current interest rates for savings accounts, CDs, and other interest-bearing accounts?
"""

def main():

    st.title("Welcome to Lucky 8 Banking!")
    st.header("Chat with our friendly chatbot Payton")
    model_name ="gpt-3.5-turbo-16k"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Send first message
    st.chat_message("assistant").markdown(firstmessage)

    # React to user input
    if input := st.chat_input("Enter your question here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(input)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": input})

        try:
            prompt = sns.sns_prompt(input)  # TODO this is the function to add
            response = model_handler.openai_api(prompt, model=model_name, temperature=0.7, top_p=1.0, n=1, stream=False)
            # post = sns.sns_prompt(response,keyword)
            # response1 = model_handler.openai_api(post, model=model_name, temperature=0.7, top_p=1.0, n=1, stream=False)
            # Display assistant response in chat message container
            
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # col1,col2 = st.columns(2)
            # with col1:
            #     st.subheader("Your Story~")
            #     st.info(response)
            # with col2:
            #     st.subheader("Your Posting~")
            #     st.info(response1)
        except Exception as e:
            logging.error(f"Error generating prompt or response: {e}")
            st.error("Error generating prompt or response. Please try again later.")

        


if __name__ == "__main__":
    open_api_key = secret.acn_token
    main()