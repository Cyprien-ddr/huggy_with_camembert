import numpy as np
from scipy.stats import gaussian_kde


def create_pdf_and_extract_stats(data):
    data_array = np.array(data).T
    kde = gaussian_kde(data_array)

    # Evaluate the KDE at a range of points to construct the probability density function
    x_values = np.linspace(0, 1, 1000)
    pdf_values = kde(x_values)

    # Calculate the standard deviation and variance from the KDE
    std_deviation = np.std(data)
    variance = np.var(data)
    return x_values, pdf_values, std_deviation, variance


def filter_variance(variance, std_deviation, matrix, id_matrix):
    resulting_matrix = []
    resulting_id = []
    cos_value = [row[1] for row in matrix]
    lim = std_deviation
    if variance > 0.02:
        lim += 3 * variance
    elif variance > 0.01:
        lim += 2 * variance
    elif variance > 0.05:
        lim += variance
    else:
        lim = 0
    for i, value in enumerate(cos_value):
        if value > lim:
            resulting_matrix.append(matrix[i][0])
            resulting_id.append(id_matrix[i])
    return resulting_matrix, resulting_id
