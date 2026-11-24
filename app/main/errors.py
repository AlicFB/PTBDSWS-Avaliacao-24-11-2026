from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    # Os módulos ainda não desenvolvidos (Disciplinas, Alunos, Cursos e
    # Ocorrências) não possuem rota: caem aqui e mostram "Não disponível".
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
