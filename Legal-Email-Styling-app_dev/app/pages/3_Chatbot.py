import streamlit as st
import sys
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import difflib  # Pour filtrer les résultats similaires
import requests

# 🔹 Configuration de la page
st.set_page_config(
    page_title="Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon='🤖'
)

sys.path.append(str(Path(__file__).parent.parent))
from utils.helpers import apply_custom_css, add_logo_and_icons

apply_custom_css()
add_logo_and_icons()

# 🔹 Appliquer le CSS personnalisé (texte en blanc pour le chatbot)
st.markdown("""
    <style>
        /* Texte en blanc pour les messages du chatbot */
        .stChatMessage {
            color: white !important;
        }

        /* Texte en blanc pour les messages de l'assistant */
        .stChatMessageContent {
            color: white !important;
        }

        /* Texte en blanc pour les messages de l'utilisateur */
        .stMarkdown {
            color: white !important;
        }

        /* Force le texte à être blanc dans toute l'application */
        body, .stApp {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)


# 🔹 Fonction pour initialiser ChromaDB avec cache
@st.cache_resource
def init():
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name='Alibaba-NLP/gte-base-en-v1.5',
        trust_remote_code=True
    )
    chroma_client = chromadb.PersistentClient(path='/home/mambauser/data/DBV')
    collection = chroma_client.get_collection(name="mails_enron", embedding_function=emb_fn)
    return collection

# Charger la base de données
collection = init()
total_count = collection.count()
print(f"Nombre total de documents dans la collection : {total_count}")

# 🔹 Titre de la page
st.title("ChatBot")

# ✅ Initialisation de l'état de session
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": f"Base de données chargée avec {total_count} documents."}]
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

def process_message(message):
    """Nettoie et valide le message utilisateur"""
    return message.strip() if message else None

# 📝 Zone de chat
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 💬 Input utilisateur
    user_input = st.chat_input("Tapez votre recherche ici...")

    if user_input:
        processed_input = process_message(user_input)
        if processed_input:
            # ➤ Ajout du message de l'utilisateur
            st.session_state.messages.append({"role": "user", "content": processed_input})

            # 🔍 Exécuter la requête ChromaDB avec gestion d'erreur
            try:
                results = collection.query(query_texts=[processed_input], n_results=30) or {}

                # 📌 Extraction des IDs et des documents avec vérification de validité
                ids = results.get("ids", [[]])[0] if "ids" in results else []
                documents = results.get("documents", [[]])[0] if "documents" in results else []

                if not ids or not documents:
                    response_content = "❌ Aucun résultat trouvé pour cette requête."
                else:
                    # 🔄 Supprimer les doublons (y compris les textes similaires)
                    unique_docs = []
                    unique_ids = []
                    seen_texts = []

                    for i in range(len(documents)):
                        doc_text = ' '.join(documents[i].strip().lower().split())  # Normalisation

                        # Vérifier si un document similaire existe déjà (seuil de 85%)
                        if not any(difflib.SequenceMatcher(None, doc_text, seen).ratio() > 0.85 for seen in seen_texts):
                            seen_texts.append(doc_text)
                            unique_docs.append(documents[i])
                            unique_ids.append(ids[i])

                    # 🔄 Préparer la réponse
                    if unique_ids and unique_docs:
                        response_content = f"📊 **{len(unique_docs)} résultats trouvés :**\n\n"
                        for i in range(len(unique_ids)):
                            response_content += f"🔹 **ID:** {unique_ids[i]}\n📄 **Document:** {unique_docs[i]}\n\n"
                    else:
                        response_content = "❌ Aucun résultat trouvé pour cette requête."

                    # 📨 Construire le contexte pour l'API
                    context = ""  # Initialisation de la variable context
                    for mail_id, mail_doc in zip(unique_ids, unique_docs):
                        context += f"Mail ID: {mail_id}\nContenu:\n{mail_doc}\n\n"
                    url = "https://aristote-dispatcher.mydocker-run-vd.centralesupelec.fr/v1/chat/completions"
                    headers = {
                        "Authorization": "Bearer nothing",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "casperhansen/llama-3-70b-instruct-awq",  # Nom du modèle
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant that answers user questions based on the context provided. If the answer is not specified in the context, say 'I don't know the answer, it is not in the context, give a complete answer'."},
                            {"role": "user", "content": f"user question: {user_input}"},
                            {"role": "user", "content": f"context: {context}"}
                        ]
                    }

                    # 🔄 Envoyer la requête avec gestion d'erreur
                    try:
                        response = requests.post(url, headers=headers, json=payload)
                        response.raise_for_status()  # Vérifie si la requête a réussi (200 OK)
                        response_json = response.json()
                        message_content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "Réponse introuvable.")
                    except requests.exceptions.RequestException as e:
                        message_content = f"⚠️ Erreur lors de l'appel à l'API : {str(e)}"
                    except Exception as e:
                        message_content = f"⚠️ Une erreur inattendue s'est produite : {str(e)}"

            except Exception as e:
                response_content = f"⚠️ Erreur lors de la recherche : {str(e)}"
                message_content = response_content

            # ➤ Ajout de la réponse dans le chat
            st.session_state.messages.append({"role": "assistant", "content": message_content})

            # 🔄 Rafraîchir la page
            st.rerun()
