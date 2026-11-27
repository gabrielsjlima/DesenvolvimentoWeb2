# Documentação da API REST — Gestão de Eventos Acadêmicos

Base local: `http://127.0.0.1:5000`.

## Autenticação e segurança

As consultas GET são públicas. As operações de escrita na API exigem usuário autenticado por sessão (`/cadastro` e `/login`) e o cabeçalho `X-CSRF-Token`, cujo valor precisa ser o token gerado para a sessão. O projeto não implementa autenticação por Bearer Token. Requisições sem token CSRF válido recebem `400`; sem login, mas com token válido, recebem `401`.

## Endpoints

| Método | Caminho | Finalidade | Respostas esperadas |
|---|---|---|---|
| GET | `/api/eventos` | Lista eventos | `200` |
| GET | `/api/eventos/<id>` | Consulta evento | `200`, `404` |
| POST | `/api/eventos` | Cria evento | `201`, `400`, `401`, `415` |
| PUT | `/api/eventos/<id>` | Atualiza campos do evento | `200`, `400`, `401`, `404`, `415` |
| PATCH | `/api/eventos/<id>` | Atualização parcial | `200`, `400`, `401`, `404`, `415` |
| DELETE | `/api/eventos/<id>` | Exclui evento | `204`, `400`, `401`, `404` |
| GET | `/api/feriados/<ano>` | Busca feriados na BrasilAPI | `200`, `400`, `502` |

### Modelo de evento

```json
{
  "id": 1,
  "nome": "Semana Acadêmica",
  "data": "2026-12-01",
  "local": "Auditório",
  "vagas": 50
}
```

`id` é gerado pelo banco. `nome` e `data` são obrigatórios na criação e na atualização completa; `data` usa `AAAA-MM-DD`. `local` é opcional, e `vagas` é inteiro não negativo. `PATCH` aceita apenas os campos informados. Os quatro campos aceitos são `nome`, `data`, `local`, `vagas`.

### Exemplos

Listar:

```bash
curl http://127.0.0.1:5000/api/eventos
```

Consultar um item:

```bash
curl http://127.0.0.1:5000/api/eventos/1
```

Feriados:

```bash
curl http://127.0.0.1:5000/api/feriados/2026
```

Para criar, alterar ou excluir eventos via API, autentique-se primeiro pela aplicação e envie o cookie da sessão e o respectivo token CSRF. Exemplo ilustrativo de POST, após obter ambos:

```bash
curl -X POST http://127.0.0.1:5000/api/eventos \
  -H 'Content-Type: application/json' \
  -H 'X-CSRF-Token: TOKEN_DA_SESSAO' \
  -b 'session=COOKIE_DA_SESSAO' \
  -d '{"nome":"Semana Acadêmica","data":"2026-12-01","local":"Auditório","vagas":50}'
```

Sucesso na criação: `201 Created`, corpo JSON do evento criado e cabeçalho `Location: /api/eventos/<id>`. Exclusão com sucesso: `204 No Content`, sem corpo. Erros de validação, recurso não encontrado e falha externa retornam JSON com a chave `erro`.

### BrasilAPI

A rota `/api/feriados/<ano>` consulta `https://brasilapi.com.br/api/feriados/v1/<ano>`. São aceitos anos de 2000 a 2100. Resposta de formato inesperado ou indisponibilidade da API externa gera `502`.

> Esta documentação reflete os controladores presentes na versão do GitHub analisada em 26/11/2026.
