import streamlit as st
import time
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from final_memoried_langchainhelper import get_chain
history = StreamlitChatMessageHistory(key="chat_messages")

st.title("MKBHD phone review 📱")
# question = st.text_input("Question : ", "Ask a question about a phone MKBHD has reviewed.")

# if st.button('ask') :
#     history.add_user_message(question)
#     chain = get_chain(history)
#     answer = chain.invoke({"question": question,"messages":history.messages})
#     history.add_ai_message(answer)
#     progress_text = "Retrieving your answer. Please wait."
#     my_bar = st.progress(0, text=progress_text)
#     for percent_complete in range(100):
#         time.sleep(0.01)
#         my_bar.progress(percent_complete + 1, text=progress_text)
#     my_bar.empty()
#     st.header("Answer : ")
#     st.write(answer)

#with st.chat_input("Ask") :

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main chat interface
if question := st.chat_input("Let's talk MKBHD"):
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(question)
        history.add_user_message(question)
        chain = get_chain(history)
        st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        answer = ''
        answer = chain.invoke({"question": question,"messages":history.messages})
        history.add_ai_message(answer)
        message_placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})





#cool feature ask for phone
#you can then ask for a link
#later we can ask for a q n a