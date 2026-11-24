from . import db


class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(16), unique=True)
    professores = db.relationship('Professor', backref='disciplina', lazy='dynamic')

    CODIGOS = ['DSWA5', 'GPSA5', 'IHCA5', 'SODA5', 'PJIA5', 'TCOA5']

    @staticmethod
    def insert_disciplinas():
        """Garante que as disciplinas do semestre existam no banco."""
        for codigo in Disciplina.CODIGOS:
            if Disciplina.query.filter_by(codigo=codigo).first() is None:
                db.session.add(Disciplina(codigo=codigo))
        db.session.commit()

    def __repr__(self):
        return '<Disciplina %r>' % self.codigo


class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'))

    def __repr__(self):
        return '<Professor %r>' % self.nome
