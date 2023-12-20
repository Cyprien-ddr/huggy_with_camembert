import spacy
import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS


def extract_stop_words():
    """
    Extract stop words from a text file

    :return: list of stop words extracted
    """
    with open("./stop_words.txt", "r") as file:
        stop_words = set(file.read().splitlines())
    print("STOP WORDS read", flush=True)
    return stop_words


def replace_shitty_char(text):
    """
    Replace all non-alphanumeric characters with space

    :param text: text to parse
    :return: parsed text
    """
    pattern_list = ["\t", "\n", "\f", "\r", "\v", "\xa0"]
    for pattern in pattern_list:
        text = text.replace(pattern, " ")

    return text


def retrieve_texts(embeddings: HuggingFaceEmbeddings, database: list[dict]) -> FAISS:
    """
    The retrieve_texts function takes in two parameters: embeddings of type HuggingFaceEmbeddings and database.txt of type list[dict[str, str, str | int]]. It iterates over the database.txt and extracts the 'hat', 'content', and 'title' values from each index. It appends these values to separate lists all_texts and all_metadatas. It then creates a vector_store using the FAISS.from_texts method, passing in the all_texts, embeddings, and all_metadatas. Finally, it returns the vector_store.

    :param embeddings: An instance of the HuggingFaceEmbeddings class representing the word embeddings model.
    :param database: A list of dictionaries, where each dictionary represents an index in the database.txt. Each dictionary contains 'id', 'hat', 'content', and 'title' keys.
    :return: An instance of the FAISS class representing the vector store created from the texts and embeddings.
    """
    all_texts = []
    all_metadatas = []

    # Iterate over db
    for index in database:
        all_texts.append(index['hat'])
        all_metadatas.append({'id': index['id'], 'html': index['html_hat'], 'title': index['title']})

    vector_store = FAISS.from_texts(texts=all_texts, embedding=embeddings, metadatas=all_metadatas)

    print("end vector store")
    return vector_store


def init_model(database: list[dict]):
    """
    Initializes the model with the given database and returns the vector store

    :param database: A list of dictionaries
    :return: An instance of the FAISS class representing the vector store created
    """
    nlp = spacy.load("fr_core_news_lg", exclude=['morphologizer', 'parser', 'senter', 'attribute_ruler', 'ner'])
    stop_words = extract_stop_words()
    for index in database:
        doc = replace_shitty_char(index['hat'])
        doc = re.sub(r"[^a-zA-ZÀ-ÿ\s]", " ", doc)
        doc = nlp(doc.lower())
        doc_tokens = (token.lemma_ for token in doc if
                      not token.is_stop and token.lemma_ not in stop_words and token.lemma_.strip() != "" and len(
                          token) > 0)
        array = list(doc_tokens)
        string_tokens = " ".join(array)
        index['hat'] = string_tokens
    embeddings = HuggingFaceEmbeddings(model_name='camembert/camembert-large')
    return retrieve_texts(embeddings, database)
