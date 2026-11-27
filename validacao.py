from datetime import date

def validar_evento(dados, parcial=False):
    if not isinstance(dados, dict):
        raise ValueError('Envie um objeto com dados do evento.')
    if not parcial and ('nome' not in dados or 'data' not in dados):
        raise ValueError('Nome e data sao obrigatorios.')
    saida = {}
    for chave in ('nome', 'data', 'local', 'vagas'):
        if chave not in dados:
            continue
        valor = dados[chave]
        if chave != 'vagas':
            if not isinstance(valor, str):
                raise ValueError(chave + ' deve ser texto.')
            valor = valor.strip()
            if chave in ('nome', 'data') and not valor:
                raise ValueError(chave + ' nao pode estar vazio.')
            if len(valor) > (10 if chave == 'data' else 120):
                raise ValueError('Campo muito longo: ' + chave)
            if chave == 'data':
                try:
                    if date.fromisoformat(valor).isoformat() != valor:
                        raise ValueError()
                except ValueError:
                    raise ValueError('Data invalida; use AAAA-MM-DD.')
        else:
            if valor in ('', None):
                valor = 0
            try:
                if isinstance(valor, bool) or str(int(valor)) != str(valor).strip():
                    raise ValueError()
                valor = int(valor)
            except (ValueError, TypeError):
                raise ValueError('Vagas deve ser numero inteiro.')
            if valor < 0:
                raise ValueError('Vagas nao pode ser negativo.')
        saida[chave] = valor
    if not parcial:
        saida.setdefault('local', '')
        saida.setdefault('vagas', 0)
    if not saida:
        raise ValueError('Nenhum campo informado.')
    return saida
