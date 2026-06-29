import streamlit as st
from agent import summarize_email
from utils import extract_text

st.set_page_config(page_title="Email Summarization Agent")

st.title("📧 Email Summarization Agent")

uploaded_file = st.file_uploader(
    "Upload Email",
    type=["txt", "pdf","doxc"]
)

email = ""

if uploaded_file:
    email = extract_text(uploaded_file)
    st.text_area("Extracted Email", email, height=250)

if st.button("Summarize Email"):

    if email.strip():

        with st.spinner("Summarizing..."):

            result = summarize_email(email)

        st.success("Done!")

        st.subheader("Summary")
        st.write(result["summary"])

        st.subheader("Key Points")
        for p in result["key_points"]:
            st.write("•", p)

        st.subheader("Action Items")
        for a in result["action_items"]:
            st.write("•", a)

        st.subheader("Deadlines")
        for d in result["deadlines"]:
            st.write("•", d)

        st.subheader("Urgency")
        st.write(result["urgency"])