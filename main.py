#!/usr/bin/python3
from data_source.mysql import get_data
from tf_idf import *
from variance_filter import *
from camembert import qa_extraction_camembert
from find_similarity_cos import *
from handle_error import handle_error
from highlight import highlight
from bs4 import BeautifulSoup
from config import configs


def no_answer_found(id_article, article):
    result = []
    hat = "Réponse(s) approchante(s) (pas de réponse exacte trouvée) : "
    reverse_id = id_article[::-1]
    for index, id in enumerate(reverse_id):
        # result.append(f"<a href=\"https://huggy.insign.fr/post/{id}\">https://huggy.insign.fr/post/{id}</a><br>")
        result.append(article[index])
    return hat, result 


def one_answer(answers, id_article, article):
    result = []
    # hat = f"Une réponse correspondante a été trouvée dans l'article : <a href=\"https://huggy.insign.fr/post/{id_article[0]}\">https://huggy.insign.fr/post/{id_article[0]}</a><br><br> : <br>"
    hat = "Une réponse pertinente trouvée (pas de réponse exacte trouvée) : "
    result.append(highlight(article[0], answers[0]))
    return hat, result 


def one_max_answer(answers, id_article, article, index): 
    result = []
    #hat = f"My best answer is in the article : <a href=\"https://huggy.insign.fr/post/{id_article[index]}\">https://huggy.insign.fr/post/{id_article[index]}</a><br><br>The answer is : <br>"
    hat = "Une réponse trouvée : "
    result.append(highlight(article[index], answers[index]))
    return hat, result 
    
def main(user_question):

    handle_error()
    # Get all articles with the db
    articles, id_articles = get_data()

    # Filter the entire db to retrieve the 10 articles most related to the question with TF-IDF algo
    # Renvoie un dic avec mot et nombre d'occurences (fréquence)
    print("tf_idf_filter")
    most_similar_articles, matrix_article = tf_idf_filter(articles, user_question)
    # Renvoie deux dic, un avec la similarité, un avec l'id article
    print("tf_idf_fct")
    cosine_similarities, id_articles = tf_idf_fct(articles, user_question, id_articles)
    # ATTENTION, pdf = pounded density function
    x_values, pdf_values, std_deviation, variance = create_pdf_and_extract_stats(cosine_similarities)

    # Filter output n articles with the variance of pdf->tf-idf (1 <= n <= 10)
    print("filter_variance")
    articles, id_articles = filter_variance(variance, std_deviation, matrix_article, id_articles)

    # Pipeline with the model CamemBERT
    print("qa_extraction_camembert")
    answers, id_article, articles_filtered, scores = qa_extraction_camembert(articles, user_question, id_articles)

    # If camembert find max one relevant answer == .2 print and exit code
    # or one relevant answer > .5 in the BEST tf-idf article print and exit code
    if len(answers) < 1:
        hat, result = no_answer_found(id_articles, articles)
        return hat, result 
    if len(answers) == 1:
        hat, result = one_answer(answers, id_article, articles_filtered)
        return hat, result 
    index = len(answers) - 1
    if id_article[index] == id_articles[len(id_articles) - 1] and scores[index] > .5:
        hat, result = one_max_answer(answers, id_article, articles_filtered, index)
        return hat, result 

    # Init the model for sentence similarity
    model_name = "paraphrase-MiniLM-L12-v2"
    print("SentenceTransformer")
    model = SentenceTransformer(model_name)
    # Best response with Question / Answers similarity
    # find_best_sim_qa(model, answers, user_question)
    print("find_best_sim_aa")
    # Output redundancy similarity between all answers
    hat, result = find_best_sim_aa(model, answers, id_article, articles_filtered)
    return hat, result 

#main("Par quel moyen se procurer un casque ?");
