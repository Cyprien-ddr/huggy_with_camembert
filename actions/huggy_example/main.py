#!/usr/bin/python3
from connection_to_db import connection_to_db
from tf_idf import *
from variance_filter import *
from camembert import qa_extraction_camembert
from find_similarity_cos import *
from handle_error import handle_error
from highlight import highlight


def no_answer_found(id_article):
    result = "\nERROR : any solution found. The answer may be in one of this articles : <br>"
    for index in id_article:
        result += f"<a href=\"https://huggy.insign.fr/post/{index}\">https://huggy.insign.fr/post/{index}</a><br>"
    return result


def one_answer(answers, id_article, article):
    result = f"\n\nI find only one answer in the article : <a href=\"https://huggy.insign.fr/post/{id_article[0]}\">https://huggy.insign.fr/post/{id_article[0]}</a><br>The answer is : <br>"
    result += highlight(article[0], answers[0])
    return result


def main(user_question):

    handle_error()
    # Get all articles with the db
    articles, id_articles = connection_to_db()
    # Get the question with the terminal
    # user_question = input("Quelle est votre question: \n")

    # Filter the entire db to retrieve the 10 articles most related to the question with TF-IDF algo
    most_similar_articles, matrix_article = tf_idf_filter(articles, user_question)
    cosine_similarities, id_articles = tf_idf_fct(articles, user_question, id_articles)
    x_values, pdf_values, std_deviation, variance = create_pdf_and_extract_stats(cosine_similarities)

    # Filter output n articles with the variance of pdf->tf-idf (1 <= n <= 10)
    articles, id_articles = filter_variance(variance, std_deviation, matrix_article, id_articles)

    # Pipeline with the model CamemBERT
    answers, id_article, articles_filtered = qa_extraction_camembert(articles, user_question, id_articles)

    # If camembert find max one relevant answer print and exit code
    if len(answers) < 1:
        return no_answer_found(id_articles)
    if len(answers) == 1:
        return one_answer(answers, id_article, articles_filtered)

    # Init the model for sentence similarity
    model_name = "paraphrase-MiniLM-L12-v2"
    model = SentenceTransformer(model_name)
    # Best response with Question / Answers similarity
    # find_best_sim_qa(model, answers, user_question)
    # Output redundancy similarity between all answers
    return find_best_sim_aa(model, answers, id_article, articles_filtered)
