#!/usr/bin/python3
import sys
from typing import Any
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def pre_rerank(docs: list, question: str) -> list[list[str]]:
    """
    Pre-rerank the documents based on the given question.

    :param docs: The list of documents to be pre-reranked.
    :param question: The question to be used for pre-reranking.
    :return: A list of lists containing the question and the page content for each document.
    """
    contents = [[question, data[0].page_content] for data in docs]
    return contents


def rerank(contents: list[list[str]]):
    """
    Rerank the documents based on the given list

    :param contents: list of lists containing the question and the page content for each document
    :return: list sorted by relevance of the document
    """
    tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-large')
    model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-large')
    model.eval()

    with torch.no_grad():
        inputs = tokenizer(contents, padding=True, truncation=True, return_tensors='pt', max_length=512)
        scores = model(**inputs, return_dict=True).logits.view(-1, ).float()

    scores = scores.tolist()

    sorted_indices = np.argsort(scores)

    id_sorted = sorted_indices[::-1]
    return id_sorted


def sort_list_of_dicts(list_of_dicts: list, index_order: list) -> list:
    """
    Sorts the given list of dictionaries

    :param list_of_dicts: list of dictionaries to be sorted
    :param index_order: list of dictionaries sorted by relevance
    :return: sorted list of dictionaries
    """
    sorted_list = []
    for i in index_order:
        print(f"{i}")
        sorted_list.append(list_of_dicts[i])

    return sorted_list


def extract_metadatas(structure: list[tuple]) -> list[dict]:
    """
    Extracts the 'html' and 'title' metadata from a list of tuples with the specified structure.

    :param structure: The list of tuples with the structure (Document, float).
    :return: A list of 'html' metadata strings.
    """
    return [{'result': doc.metadata.get('html', ''), 'title': doc.metadata.get('title', '')} for doc, _ in structure]


def main(question: str, vector_store):
    """
    The main entry point of the program

    :param vector_store: FAISS vector store
    :param question: A string representing the user's query.
    :return: None. The function prints the search results to the console.
    """
    print("Hello World")
    results = vector_store.similarity_search_with_score(question, k=50)
    for doc, score in results:
        print(f"Content: {doc.page_content}\nMetadata: {doc.metadata}, Score: {score}",
              end="\n------------------------\n")

    index = rerank(pre_rerank(results, question))
    for row in index:
        print(f"Results : {row}")
    print(index)
    db = sort_list_of_dicts(results, np.ndarray.tolist(index))
    print(db)
    result = extract_metadatas(db)
    print("\n\n-------------------------\n\n")
    print(result)
    return result
