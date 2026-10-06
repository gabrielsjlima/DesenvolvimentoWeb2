# Regras de Negócio

1. Cada evento possui um número limitado de vagas.

2. Um participante não pode se inscrever duas vezes
   no mesmo evento.

3. Uma inscrição deve estar relacionada a um participante existente.

4. Uma inscrição deve estar relacionada a um evento existente.

5. Cada participante possui um identificador único.

6. Cada evento possui um identificador único.

7. Cada inscrição possui um identificador único.

# Entidades e atributos

1. Participante
    - id (PK)
    - nome
    - email

2. Evento 
    - id (PK)
    - nome
    - data
    - local
    - vagas

3. Inscrição
    - id (PK)
    - participante_id (FK)
    - evento_id (FK)
    - data_inscricao

# Relacionamento e cardinalidades

Participante 1 -> N Inscrição (Um participante pode ter muitas incrições)

Evento 1 -> N Inscrição (Um evento pode ter muitas incrições)