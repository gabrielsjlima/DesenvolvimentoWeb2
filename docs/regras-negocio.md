# Regras de negócio

1. Cada evento possui um número limitado de vagas.
2. Um participante não pode se inscrever duas vezes no mesmo evento.
3. Uma inscrição deve estar relacionada a um participante existente.
4. Uma inscrição deve estar relacionada a um evento existente.
5. Cada participante possui um identificador único.
6. Cada evento possui um identificador único.
7. Cada inscrição possui um identificador único.

## Entidades

- Evento: id (PK), nome, data, local, vagas.
- Participante: id (PK), nome, email (único).
- Inscricao: id (PK), participante_id (FK), evento_id (FK), data_inscricao.
- Usuario: id (PK), nome, email (único), senha_hash.

## Cardinalidades

- Participante 1:N Inscricao.
- Evento 1:N Inscricao.
- Par (participante_id, evento_id) único para impedir inscrições duplicadas.
