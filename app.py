
import streamlit as st

from preprocessing import (
    preprocess_text,
    preprocess_uploaded_email
)

from model import predict_email


# -------------------------------
# Reset Function
# -------------------------------

def reset_inputs():
    st.session_state["subject"] = ""
    st.session_state["body"] = ""
    st.session_state["clear_file"] = True


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="SpamShield",
    page_icon="🛡️",
    layout="wide"
)


# -------------------------------
# Header
# -------------------------------

st.title("🛡️ SpamShield")

st.write(
    "An AI-powered email spam detection system. "
    "Check whether an email is legitimate or spam."
)

st.warning(
    "Security Notice: Do not click suspicious links "
    "or download unexpected attachments. "
    "SpamShield provides predictions, not guaranteed "
    "security verification.",
    icon="⚠️"
)


# -------------------------------
# Email Input
# -------------------------------

st.subheader("📩 Analyze an Email")

subject = st.text_input(
    "Email Subject",
    placeholder="Enter the email subject...",
    key="subject"
)

body = st.text_area(
    "Email Body",
    placeholder="Paste your email content here...",
    height=200,
    key="body"
)


# -------------------------------
# Email File Upload
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload an email (.eml)",
    type=["eml"],
    key="email_file",
    disabled=st.session_state.get("clear_file", False)
)

# Clear the uploader through a temporary disabled state
if st.session_state.get("clear_file", False):
    st.session_state["clear_file"] = False
    st.rerun()


# -------------------------------
# Analyze Button
# -------------------------------

analyze = st.button(
    "🔍 Analyze Email",
    use_container_width=True
)

if analyze:

    email_text = ""

    if uploaded_file is not None:
        email_text = preprocess_uploaded_email(
            uploaded_file.getvalue()
        )

    elif subject.strip() or body.strip():
        email_text = preprocess_text(subject, body)

    else:
        st.warning(
            "Please enter an email or upload an .eml file."
        )

    # -------------------------------
    # Prediction
    # -------------------------------

    if email_text:

        result = predict_email(email_text)

        st.divider()
        st.subheader("📊 Analysis Results")

        # Three-column metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Prediction",
                result["prediction"]
            )

        with col2:
            st.metric(
                "Spam Probability",
                f'{result["spam_percentage"]}%'
            )

        with col3:
            st.metric(
                "Classification Threshold",
                f'{result["threshold_percentage"]}%'
            )

        # -------------------------------
        # Probability Bar
        # -------------------------------

        bar_color = (
            "#EF4444"
            if result["prediction"] == "Spam"
            else "#22C55E"
        )

        st.markdown(
            f"""
            <div style="
                background-color: #334155;
                border-radius: 10px;
                height: 12px;
                width: 100%;
                margin: 12px 0;
            ">
                <div style="
                    width: {result["spam_percentage"]}%;
                    background-color: {bar_color};
                    height: 12px;
                    border-radius: 10px;
                ">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            f'{result["spam_percentage"]}% probability of being spam'
        )

        # -------------------------------
        # Prediction Message
        # -------------------------------

        if result["prediction"] == "Spam":

            st.error(
                "🚨 Spam detected! Be careful with this email. "
                "Avoid suspicious links and attachments."
            )

        else:

            st.success(
                "✅ This email was classified as Ham. "
                "Still verify unexpected links and attachments."
            )


# -------------------------------
# Start New Analysis Button
# -------------------------------

st.divider()

st.button(
    "🔄 Start New Analysis",
    on_click=reset_inputs,
    use_container_width=True
)
