from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash, current_app
from .. import db
from ..models import Professor, Disciplina
from . import main
from .forms import ProfessorForm


@main.app_context_processor
def inject_current_time():
    """Disponibiliza a data/hora (UTC) a todos os templates; o Flask-Moment
    converte para o horário local do navegador."""
    return dict(current_time=datetime.now(timezone.utc).replace(tzinfo=None))


@main.route('/')
def index():
    return render_template('index.html',
                           aluno_nome=current_app.config['ALUNO_NOME'],
                           aluno_prontuario=current_app.config['ALUNO_PRONTUARIO'])


@main.route('/professores', methods=['GET', 'POST'])
def professores():
    Disciplina.insert_disciplinas()
    form = ProfessorForm()
    form.disciplina.choices = [(d.id, d.codigo)
                               for d in Disciplina.query.order_by(Disciplina.id)]

    if form.validate_on_submit():
        professor = Professor(nome=form.nome.data.strip(),
                              disciplina_id=form.disciplina.data)
        db.session.add(professor)
        db.session.commit()
        flash('Professor cadastrado com sucesso.')
        return redirect(url_for('.professores'))

    lista = Professor.query.order_by(Professor.id).all()
    return render_template('professores.html', form=form, professores=lista)
