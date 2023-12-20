from transformers import pipeline
import numpy as np


def qa_extraction_camembert(articles, question, id_article):
    qa = pipeline('question-answering', model='CATIE-AQ/QAmembert', tokenizer='CATIE-AQ/QAmembert', padding=True, truncation=True)
    answers = []
    model_scores = []
    result_id = []
    articles_filter = []
    for i, article in enumerate(articles):
        result = qa({
            'question': question,
            'context':  article,
        })
        if result['score'] > 0.2:
            articles_filter.append(article)
            answers.append(result['answer'])
            result_id.append(id_article[i])
            model_scores.append(result['score'])
    return answers, result_id, articles_filter
