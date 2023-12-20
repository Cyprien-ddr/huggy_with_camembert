from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
import numpy as np

def dump(obj):
  cpt = 0
  for index, item in enumerate(obj):
    # print(vars(item))
    print(item)
    print("-----")
    if cpt == 100000:
      break
    cpt = cpt + 1
    
def tf_idf_filter(articles, user_question):
    final_stopwords_list = list(fr_stop) + list(en_stop)
    #vectorized = TfidfVectorizer(stop_words=list(fr_stop))
    #vectorized = TfidfVectorizer(stop_words=final_stopwords_list)
    vectorized = TfidfVectorizer()
    tfidf_matrix = vectorized.fit_transform(articles)
    user_question_tfidf = vectorized.transform([user_question])
    # vectorized_features = vectorized.get_feature_names_out()

    cosine_similarities = cosine_similarity(user_question_tfidf, tfidf_matrix)

    # Sort text by prevalence and get the 10th most relevant
    most_similar_article_indices = np.argsort(cosine_similarities[0], )[-10:]
    matrix_article = [[articles[index], cosine_similarities[0][index], index] for index in most_similar_article_indices]
    most_similar_articles = [articles[index] for index in most_similar_article_indices]
    return most_similar_articles, matrix_article


def print_tf_idf_result(matrix_article):
    print("\n\\--------------ARTICLES filtered\\--------------\n")
    for i, article in enumerate(matrix_article):
        print(f'Text: {article[0]}')
        print(f"Cosine Similarity: {article[1]}")
        print(f'Index: {article[2]}')
        print("\n")


def tf_idf_fct(articles, user_question, ids):
    vectorized = TfidfVectorizer()
    tfidf_matrix = vectorized.fit_transform(articles)

    user_question_tfidf = vectorized.transform([user_question])
    cosine_similarities = cosine_similarity(user_question_tfidf, tfidf_matrix)

    # Sort text by prevalence and get the 10th most relevant
    most_similar_article_indices = np.argsort(cosine_similarities[0], )[-10:]
    matrix_article = [cosine_similarities[0][index] for index in most_similar_article_indices]
    matrix_id = [ids[index] for index in most_similar_article_indices]
    return matrix_article, matrix_id