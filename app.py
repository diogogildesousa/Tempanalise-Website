from flask import (
    Flask,
    render_template,
    send_from_directory,
    abort,
    url_for,
    request,
    flash,
    redirect,
    g,
)
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import os
import sqlite3
import click  # Adicionado para usar comandos de linha de comando do Flask

# ----------------------------- CONFIGURAÇÃO INICIAL -----------------------------
app = Flask(__name__)
# Chave secreta obrigatória para Flask-WTF e flash messages
app.secret_key = os.urandom(24)
PDF_FOLDER = "static/pdfs"
DATABASE = "site.db"


# ----------------------------- GESTÃO DA BASE DE DADOS -----------------------------


def get_db():
    """Conecta à base de dados especificada na configuração da aplicação."""
    # O g é um objeto global de contexto para o pedido atual.
    # Garante que a mesma conexão DB é usada durante um único request.
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Permite aceder às colunas por nome
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Fecha a conexão com o DB no final de cada pedido."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas da base de dados e insere os dados iniciais."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # 1. Tabela para Artigos de Legislação (Dados Persistentes)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS legislation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                date TEXT,
                resumo TEXT
            );
        """
        )

        # 2. Tabela para Mensagens de Contacto (Dados Dinâmicos de Utilizador)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        # Insere dados de PDFs se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM legislation")
        if cursor.fetchone()[0] == 0:
            insert_initial_pdf_data(db)

        db.commit()


def insert_initial_pdf_data(db):
    """
    Insere a lista inicial de PDFs na BD.
    Esta função agora preenche a BD com metadados básicos
    para os ficheiros que já estão na pasta 'static/pdfs',
    eliminando a necessidade de listar todos os nomes no código Python.
    """

    # Metadados específicos para os ficheiros já existentes (para não perder a informação original)
    metadata_map = {
        "regulamento-1054-2020.pdf": {
            "title": "Regulamento 1054/2020",
            "date": datetime(2020, 7, 15),
            "resumo": "Regulamento de Execução (UE) 2020/1054 da Comissão, de 15 de julho de 2020.",
        },
        "Regulamento_165_2014.pdf": {
            "title": "Regulamento 165/2014",
            "date": datetime(2014, 2, 4),
            "resumo": "Regulamento (UE) n.º 165/2014, relativo aos tacógrafos no transporte rodoviário.",
        },
        "Regulamento_581_2010.pdf": {
            "title": "Regulamento 581/2010",
            "date": datetime(2010, 1, 1),
            "resumo": "Regulamento (UE) n.º 581/2010, relativo à duração dos períodos de interrupção e de repouso dos condutores.",
        },
        "Lei_27_2010.pdf": {
            "title": "Lei 27/2010",
            "date": datetime(2010, 1, 1),
            "resumo": "Lei n.º 27/2010, que estabelece o regime sancionatório aplicável às infrações aos tempos de condução e repouso.",
        },
        "Regulamento_1073_2009.pdf": {
            "title": "Regulamento 1073/2009",
            "date": datetime(2009, 1, 1),
            "resumo": "Regulamento (CE) n.º 1073/2009, relativo às regras comuns de acesso ao mercado internacional de serviços de autocarro e de camioneta.",
        },
        "DecretoLei_169_2009.pdf": {
            "title": "Decreto-Lei 169/2009",
            "date": datetime(2009, 1, 1),
            "resumo": "Decreto-Lei n.º 169/2009, transpondo a Diretiva 2002/15/CE, relativa à organização do tempo de trabalho das pessoas que exercem atividades móveis de transporte rodoviário.",
        },
        "Recomendacao_23_Jan_2009.pdf": {
            "title": "Recomendação 23 Jan 2009",
            "date": datetime(2009, 1, 23),
            "resumo": "Recomendação da Comissão Europeia sobre a utilização dos tacógrafos digitais.",
        },
        "Portaria_44_2012.pdf": {
            "title": "Portaria 44/2012",
            "date": datetime(2012, 1, 1),
            "resumo": "Portaria n.º 44/2012, que regulamenta a fiscalização dos tempos de condução e repouso.",
        },
        "Portaria_222_2008.pdf": {
            "title": "Portaria 222/2008",
            "date": datetime(2008, 1, 1),
            "resumo": "Portaria n.º 222/2008, sobre as condições de acesso à atividade de transportador.",
        },
        "DecretoLei_237_2007.pdf": {
            "title": "Decreto-Lei 237/2007",
            "date": datetime(2007, 1, 1),
            "resumo": "Decreto-Lei n.º 237/2007, relativo à inspeção técnica de veículos.",
        },
        "DecretoLei_117_2012.pdf": {
            "title": "Decreto-Lei 117/2012",
            "date": datetime(2012, 1, 1),
            "resumo": "Decreto-Lei n.º 117/2012, que transpõe diretivas sobre o transporte de mercadorias perigosas.",
        },
        "Despacho_13449_2006.pdf": {
            "title": "Despacho 13449/2006",
            "date": datetime(2006, 1, 1),
            "resumo": "Despacho n.º 13449/2006, estabelecendo regras para a emissão de cartões de condutor.",
        },
        "Regulamento_561_2006.pdf": {
            "title": "Regulamento 561/2006",
            "date": datetime(2006, 1, 1),
            "resumo": "Regulamento (CE) n.º 561/2006, relativo à harmonização de certas disposições em matéria social no domínio dos transportes rodoviários.",
        },
        "DecretoLei_117_2002.pdf": {
            "title": "Decreto-Lei 117/2002",
            "date": datetime(2002, 1, 1),
            "resumo": "Decreto-Lei n.º 117/2002, relativo à formação de condutores de veículos pesados.",
        },
        "Diretiva_2002_15_CE.pdf": {
            "title": "Diretiva 2002/15/CE",
            "date": datetime(2002, 1, 1),
            "resumo": "Diretiva 2002/15/CE, relativa à organização do tempo de trabalho das pessoas que exercem atividades móveis de transporte rodoviário.",
        },
    }

    # Certifica-se de que a pasta de PDFs existe
    pdf_dir_path = os.path.join(app.root_path, PDF_FOLDER)
    if not os.path.exists(pdf_dir_path):
        print(
            f"ATENÇÃO: A pasta {PDF_FOLDER} não existe. Não foram encontrados PDFs para adicionar à BD."
        )
        # Podemos ainda adicionar as notas de orientação que não requerem ficheiros físicos.
    else:
        # Percorre a pasta de PDFs e insere na BD se não existir
        for filename in os.listdir(pdf_dir_path):
            if filename.lower().endswith(".pdf"):
                # Tenta obter metadados específicos ou usa genéricos
                pdf_data = metadata_map.get(filename, {})

                title = (
                    pdf_data.get("title")
                    or filename.replace(".pdf", "").replace("_", " ").title()
                )
                date_obj = pdf_data.get("date")
                date_str = date_obj.isoformat() if date_obj else None
                resumo = (
                    pdf_data.get("resumo") or f"Resumo genérico do documento: {title}."
                )

                # Insere apenas se não existir (ignora se UNIQUE constraint falhar)
                sql = "INSERT OR IGNORE INTO legislation (filename, title, date, resumo) VALUES (?, ?, ?, ?)"
                db.execute(sql, (filename, title, date_str, resumo))

    # Adiciona as Notas de Orientação (que podem não ter ficheiros físicos no início)
    initial_notes = [
        {
            "filename": "Nota_Orientacao_1.pdf",
            "title": "Nota de Orientação 1",
            "date": None,
            "resumo": "Esclarecimentos sobre o Regulamento (CE) n.º 561/2006.",
        },
        {
            "filename": "Nota_Orientacao_2.pdf",
            "title": "Nota de Orientação 2",
            "date": None,
            "resumo": "Guia prático para a aplicação dos tempos de condução e repouso.",
        },
        {
            "filename": "Nota_Orientacao_3.pdf",
            "title": "Nota de Orientação 3",
            "date": None,
            "resumo": "Orientações sobre o uso do tacógrafo digital.",
        },
        {
            "filename": "Nota_Orientacao_4.pdf",
            "title": "Nota de Orientação 4",
            "date": None,
            "resumo": "Detalhes sobre as exceções e derrogações ao Regulamento 561/2006.",
        },
        {
            "filename": "Nota_Orientacao_5.pdf",
            "title": "Nota de Orientação 5",
            "date": None,
            "resumo": "Interpretação da legislação sobre o período de repouso semanal.",
        },
        {
            "filename": "Nota_Orientacao_6.pdf",
            "title": "Nota de Orientação 6",
            "date": None,
            "resumo": "Regras sobre a 'regra dos 12 dias' para transporte internacional.",
        },
        {
            "filename": "Nota_Orientacao_7.pdf",
            "title": "Nota de Orientação 7",
            "date": None,
            "resumo": "Fiscalização dos tempos de trabalho e repouso.",
        },
        {
            "filename": "Nota_Orientacao_8.pdf",
            "title": "Nota de Orientação 8",
            "date": None,
            "resumo": "Implicações da utilização de ferries ou comboios.",
        },
    ]

    sql = "INSERT OR IGNORE INTO legislation (filename, title, date, resumo) VALUES (?, ?, ?, ?)"
    for pdf in initial_notes:
        db.execute(sql, (pdf["filename"], pdf["title"], None, pdf["resumo"]))

    db.commit()


# Comando CLI para inicialização da BD
@click.command("init-db")
def init_db_command():
    """Limpa os dados existentes e cria novas tabelas (inicialização manual)."""
    # Para garantir que recria a BD do zero e carrega tudo
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    init_db()
    click.echo(
        "Base de dados inicializada com sucesso! Dados carregados a partir dos ficheiros em static/pdfs."
    )


# NOVO: Função para adicionar PDFs individualmente, sem apagar o resto
@click.command("add-pdf")
@click.argument("filename")
@click.argument("title")
@click.option("--date", default=None, help="Data no formato YYYY-MM-DD.")
@click.option("--resumo", default="Resumo não fornecido.", help="Resumo do documento.")
def add_pdf_command(filename, title, date, resumo):
    """
    Adiciona um novo documento à tabela Legislation.
    Requer: FILENAME (Nome do ficheiro.pdf) e TITLE (Título)
    Exemplo: flask add-pdf novo_doc.pdf "Novo Documento Importante" --date 2025-10-05
    """
    with app.app_context():
        db = get_db()
        date_str = None
        if date:
            try:
                # Valida o formato da data, embora seja guardada como string
                datetime.strptime(date, "%Y-%m-%d")
                date_str = date
            except ValueError:
                click.echo(
                    f"ERRO: Formato de data inválido. Use YYYY-MM-DD. Data ignorada."
                )

        try:
            sql = "INSERT INTO legislation (filename, title, date, resumo) VALUES (?, ?, ?, ?)"
            db.execute(sql, (filename, title, date_str, resumo))
            db.commit()
            click.echo(f'Sucesso! Documento "{filename}" adicionado à BD.')
        except sqlite3.IntegrityError:
            click.echo(
                f'ERRO: O documento com o nome de ficheiro "{filename}" já existe na Base de Dados.'
            )
        except Exception as e:
            click.echo(f"ERRO na Base de Dados: {e}")


# Adiciona os comandos ao CLI do Flask
app.cli.add_command(init_db_command)
app.cli.add_command(add_pdf_command)


# ----------------------------- FORMULÁRIOS -----------------------------
class ContactForm(FlaskForm):
    nome = StringField(
        "Nome",
        validators=[
            DataRequired("Por favor, introduza o seu nome."),
            Length(min=2, max=100, message="O nome deve ter entre 2 e 100 caracteres."),
        ],
        render_kw={"autocomplete": "off"} # Adicione isto!
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired("Por favor, introduza o seu email."),
            Email("Formato de email inválido."),
        ],
        render_kw={"autocomplete": "off"} # Adicione isto!
    )
    mensagem = TextAreaField(
        "Mensagem",
        validators=[
            DataRequired("Por favor, introduza uma mensagem."),
            Length(min=10, message="A mensagem deve ter pelo menos 10 caracteres."),
        ],
    )
    submit = SubmitField("Enviar")


# ----------------------------- ROTAS -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/servicos")
def servicos():
    return render_template("servicos.html")


@app.route("/certificados")
def certificados():
    return render_template("certificados.html")


@app.route("/legislacao")
def legislacao():
    db = get_db()
    # Busca todos os PDFs, ordenados pela data (mais recente primeiro)
    pdfs_from_db = db.execute(
        "SELECT * FROM legislation ORDER BY date DESC NULLS LAST, title ASC"
    ).fetchall()  # Adicionado title ASC para desempate

    # Processa os dados para o formato esperado pelo Jinja2 (datetimes para a ordenação no template)
    processed_pdfs = []
    for pdf in pdfs_from_db:
        pdf_dict = dict(pdf)  # Converte sqlite3.Row para dict
        # Se a data existir, converte a string ISO de volta para objeto datetime
        if pdf_dict["date"]:
            # Ligeira melhoria de robustez: usamos try/except para parsing de data
            try:
                pdf_dict["date"] = datetime.fromisoformat(pdf_dict["date"])
            except ValueError:
                pdf_dict["date"] = None  # Caso o formato ISO esteja incorreto

        processed_pdfs.append(pdf_dict)

    return render_template("legislacao.html", pdfs=processed_pdfs)


@app.route("/contactos", methods=["GET", "POST"])
def contactos():
    form = ContactForm()
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        mensagem = form.mensagem.data

        # Salvar os dados na Base de Dados (Persistência CS50x)
        try:
            db = get_db()
            db.execute(
                "INSERT INTO messages (nome, email, mensagem) VALUES (?, ?, ?)",
                (nome, email, mensagem),
            )
            db.commit()
            flash(
                "Mensagem enviada com sucesso! A sua mensagem foi guardada.", "success"
            )
        except sqlite3.Error as e:
            # Em caso de erro na BD, regista-o e avisa o utilizador
            print(f"Erro ao inserir mensagem na BD: {e}")
            flash(
                "Ocorreu um erro ao guardar a sua mensagem. Por favor, tente novamente.",
                "danger",
            )

        # Redireciona após POST (Post/Redirect/Get pattern)
        return redirect(url_for("contactos"))

    if request.method == "POST" and not form.validate_on_submit():
        # Se for POST, mas a validação falhar, esta linha captura erros não relacionados com validações de campo
        flash("Erro: verifica os dados inseridos.", "danger")

    return render_template("contactos.html", form=form)


@app.route("/pdf/<filename>/")
def visualizar_pdf(filename):
    db = get_db()
    # Busca o PDF por filename na Base de Dados
    pdf = db.execute(
        "SELECT title, filename, resumo FROM legislation WHERE filename = ?",
        (filename,),
    ).fetchone()

    if not pdf:
        abort(404)

    pdf_dict = dict(pdf)
    return render_template(
        "pdf_viewer.html", filename=pdf_dict["filename"], title=pdf_dict["title"]
    )


@app.route("/static/pdfs/<filename>")
def serve_pdf(filename):
    # Envia o ficheiro PDF do diretório estático
    # Note: O ficheiro só é servido se existir fisicamente na pasta static/pdfs
    return send_from_directory(PDF_FOLDER, filename)


# ----------------------------- ERROS -----------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


# ----------------------------- INICIALIZAÇÃO -----------------------------
# Verifica se a BD existe para inicializar.
if not os.path.exists(DATABASE):
    print(
        f"Base de dados '{DATABASE}' não encontrada. A criar e inicializar com dados de legislação..."
    )
    init_db()

if __name__ == "__main__":
    # Garante que a pasta de PDFs existe para evitar erros de leitura na inicialização
    os.makedirs(PDF_FOLDER, exist_ok=True)
    app.run(debug=True, host="0.0.0.0")
