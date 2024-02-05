import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import fitz  # PyMuPDF
import base64

# Funksjon for innlasting av pdf
def load_pdf_content(pdf_path):
    """Load and return the text content of a PDF document."""
    text = ''
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Load PDF document content
pdf_path = 'leietakerhandbok-moller.pdf'
pdf_content = load_pdf_content(pdf_path)


# Sett opp Streamlit-sidekonfigurasjon
st.set_page_config(page_title="Møller Eiendoms Leietakerhåndbok", page_icon="🤖", layout="wide")

LOGO_IMAGE = "moller_eiendom_logo.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
        align-items: flex-end; /* Justerer elementene slik at de flukter med bunnen */
    }
    .logo-text {
        font-weight:700 !important;
        font-size:36px !important;
        color: #000000 !important;
        padding-top: 25px !important;
        margin-left: 25px !important;
        padding-bottom: 0px !important;
    }
    .logo-img {
        /* Sørger for at bildet ikke strekker seg utover sin opprinnelige størrelse */
        max-height: 100%; 
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" style="width:200px; height:auto;">
        <p class="logo-text">Møller Eiendoms<br>leietakerhåndbok</p>
    </div>
    """,
    unsafe_allow_html=True
)



# Initialiser ChatOpenAI-modellen
API = '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'
chat = ChatOpenAI(temperature=0.5, model_name="gpt-4-0125-preview", openai_api_key=API, verbose=True)

# Initialiser session state for å lagre meldinger
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hei! Jeg er Møller Eiendoms assistent for leietakere. Hva kan jeg hjelpe deg med?"}]

# Vis alle meldinger
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Håndter brukerinput
user_input = st.chat_input("Din forespørsel")

if user_input:
    
    # Legg umiddelbart til brukerens melding
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Bygg listen med meldinger for AI-respons
    zipped_messages = [SystemMessage(
        content="Speak Norwegian. You are a helpful AI assistant talking with a human. If you do not know an answer, just say 'I don't know', do not make up an answer. Here is the document content for reference:\n" + pdf_content)]
    for message in st.session_state.messages:
        if message["role"] == "user":
            zipped_messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            zipped_messages.append(AIMessage(content=message["content"]))

    # Generer AI-respons direkte
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = chat(zipped_messages).content
            st.write(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
