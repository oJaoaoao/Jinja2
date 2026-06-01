from flask import Flask, jsonify, request, render_template
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

@app.route('/api/biblioteca', methods=['GET', 'POST'])
@app.route('/api/biblioteca/<isbn>', methods=['GET', 'DELETE', 'PUT'])
def manipular_livro(isbn=None):
    if request.method == 'GET':
        if not isbn:
            return jsonify(biblioteca)
        else:
            for livro in biblioteca:
                if livro['isbn'] == isbn:
                    return jsonify(livro)
            return jsonify("Livro não encontrado"), 404
            
    elif request.method == 'POST':
        novo_livro = request.get_json()
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify("Livro criado com sucesso"), 201
        
    elif request.method == 'DELETE':
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                biblioteca.remove(livro)
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro deletado com sucesso"), 200
        return jsonify("Livro não encontrado"), 404
                
    elif request.method == 'PUT':
        novo_livro = request.get_json()
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                for key, values in novo_livro.items():
                    livro[key] = values
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro alterado com sucesso"), 200
        return jsonify("Livro não encontrado"), 404
        
    else:
        return jsonify("Método não permitido"), 405

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/biblioteca')
def biblio():
    return render_template('biblioteca.html', variavel1=biblioteca)


if __name__ == '__main__':
    app.run(debug=True)
