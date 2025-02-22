from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Carregar o arquivo CSV com pandas
    df = pd.read_csv(r'data/dados_apostas.csv')

    # Converter o DataFrame para uma lista de dicionários para enviar ao HTML
    data = df.to_dict(orient='records')

    # Renderizar o template e passar os dados
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
