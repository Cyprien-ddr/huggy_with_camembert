def highlight(text, highlight_text):
    answer = text.replace(highlight_text, f'<b>{highlight_text}</b>')
    return answer
