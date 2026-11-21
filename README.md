# Desenvolvimento Web II — Sistema de Gestão de Eventos Acadêmicos

**Aluno:** Gabriel Sebastião Jordão de Lima  
**Disciplina:** Desenvolvimento Web II — FATEC Porto Ferreira  
**Repositório original:** https://github.com/gabrielsjlima/DesenvolvimentoWeb2

## Endpoints REST

- `GET /api/eventos` — lista os eventos; resposta 200.
- `GET /api/eventos/<id>` — consulta evento; 200 ou 404.
- `POST /api/eventos` — cria evento; 201, 400, 401 ou 415.
- `PUT /api/eventos/<id>` — substitui campos; 200, 400, 401 ou 404.
- `PATCH /api/eventos/<id>` — altera campos selecionados; 200, 400, 401 ou 404.
- `DELETE /api/eventos/<id>` — remove; 204 ou 404.
- `GET /api/feriados/<ano>` — consome BrasilAPI; 200, 400 ou 502.

## Estrutura

- `app.py`: inicializa app e banco.
- `controllers/`: rotas do site, autenticação e API.
- `models/`: entidades ORM.
- `dao/`: consulta e persistência de eventos.
- `templates/`: HTML Jinja2.
- `static/`: CSS e AJAX/Fetch.
- `tests/`: testes automatizados.
- `docs/`: regras de negócio; mantenha o DER original no diretório `docs/DER/`.

