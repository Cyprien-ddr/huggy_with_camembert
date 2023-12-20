from sentence_transformers import SentenceTransformer, util
from highlight import highlight


def cosine_score(model, first, second):
    first_embedding = model.encode(first, convert_to_tensor=True)
    second_embeddings = model.encode(second, convert_to_tensor=True)
    return util.pytorch_cos_sim(first_embedding, second_embeddings)


def find_best_sim_qa(model, answers, question):
    # Find the index of the highest similarity score for the question (index of the best answer)
    cosine_scores_question = cosine_score(model, question, answers)
    best_answer_index = cosine_scores_question.argmax().item()
    best_answer = answers[best_answer_index]


def find_best_sim_aa(model, answers, id_article, articles_filter):
    sim_ans = []
    n_sim_ans = []
    cosine_scores_answers = cosine_score(model, answers, answers)
    for i in range(len(answers)):
        line_sim_ans = []
        n_line_sim_ans = 0
        for j in range(len(answers)):
            if i != j:
                similarity_score = cosine_scores_answers[i][j].item()
                line_sim_ans.append(similarity_score)
                n_line_sim_ans += similarity_score
        sim_ans.append(line_sim_ans)
        n_sim_ans.append(n_line_sim_ans)
    best_n_sim_ans = max(n_sim_ans)
    index_best_sim_ans = n_sim_ans.index(best_n_sim_ans)
    result = []
    if index_best_sim_ans <= 0:
        ''' hat = f"I can\'t find the best sim answer/answer. I take the answer in the last doc {answers[len(answers) - 1]}\
        at this link : <a href=\"https://huggy.insign.fr/post/{id_article[len(answers) - 1]}<\">https://huggy.insign.fr\
        /post/{id_article[len(answers) - 1]}</a><br><br>" '''
        hat = "Une réponse pertinente trouvée (pas de réponse exacte trouvée) :"
        result.append(highlight(articles_filter[len(answers) - 1], answers[len(answers) - 1]))
    else:
        hat = f"La réponse exacte trouvée :<br><br>"
        result.append(highlight(articles_filter[index_best_sim_ans], answers[index_best_sim_ans]))
    return hat, result 
