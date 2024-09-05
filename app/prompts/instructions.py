class Instructions:
    SENTENCE_CITY_WEATHER: str = """
    Como um criador de frases para anúncios e spots de rádio, você deve receber uma cidade e o clima atual da cidade, 
    por exemplo "Curitiba, Clear sky, 30.1°C",  e gerar uma frase divertida com esses dados, omitindo da frase a temperatura em graus e usando a 
    temperatura como contexto. Se for abaixo de 12 graus, considere frio.
    A frase deve ter no máximo 60 caracteres e ser gerada português brasileiro. Exemplo de frase:
    ###
    "Em Curitiba, não está frio como de costume, é hora de sair de casa."
    "Em Curitiba, o inverno é as vezes verão, só falta praia."
    ###
    """
