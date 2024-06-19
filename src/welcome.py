import streamlit as st
import os
import openai
import time
import asyncio


# st.set_page_config(
#     page_title="Task Agent",
#     page_icon="👋",
# )

# st.write("# Task Agent!👋")


# st.markdown(
#     f"Welcome to Task Agent!"
# )

# c1, c2 = st.columns(2)

# input_query_str = st.chat_input("Enter")


# if input_query_str:
#     run()


def model(query):
    time.sleep(query)
    yield "hello " + str(query)

def run():
    
    l1 = model(10)
    l2 = model()


    # with c1:
    #     s1 = st.empty()
    # with c2:
    #     s2 = st.empty()

    x, y = True, True
    while x is True or y is True:
        try:
            o1 = next(l1)
            print(o1)
        except Exception as e:
            print(e)
            x = False
        try:
            o2 = next(l2)
            print(o2)
        except Exception as e:
            print(e)
            y = False

            
            
run()