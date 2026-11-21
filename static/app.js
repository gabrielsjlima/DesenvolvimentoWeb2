'use strict';
const statusApi=document.getElementById('status-api');
document.getElementById('atualizar').addEventListener('click',async()=>{
  statusApi.textContent='Atualizando...';
  try {
    const resp=await fetch('/api/eventos');
    if(!resp.ok)throw new Error('HTTP '+resp.status);
    const eventos=await resp.json();
    statusApi.textContent=eventos.length+' evento(s) encontrado(s).';
    // Fetch sem recarregar a pagina: a lista renderizada pelo servidor permanece com formularios e botoes.
    // Exibe abaixo da mensagem os dados atuais obtidos pela API, sem injetar HTML externo.
    let lista=document.getElementById('resultado-api');
    if(!lista){lista=document.createElement('ul');lista.id='resultado-api';statusApi.after(lista);}
    lista.replaceChildren();
    eventos.forEach(e=>{const li=document.createElement('li');li.textContent=e.nome+' — '+e.data+' — '+(e.local||'Sem local');lista.append(li);});
  }catch(erro){statusApi.textContent='Falha ao consultar API: '+erro.message;}
});
document.getElementById('form-feriados').addEventListener('submit',async ev=>{
  ev.preventDefault();
  const status=document.getElementById('status-feriados');
  const lista=document.getElementById('feriados');
  lista.replaceChildren();status.textContent='Consultando...';
  try {
    const ano=document.getElementById('ano').value;
    const resp=await fetch('/api/feriados/'+encodeURIComponent(ano));
    const dados=await resp.json();
    if(!resp.ok)throw new Error(dados.erro||'HTTP '+resp.status);
    dados.forEach(f=>{const li=document.createElement('li');li.textContent=f.date+' — '+f.name;lista.append(li);});
    status.textContent=dados.length+' feriado(s) encontrado(s).';
  }catch(erro){status.textContent='Erro: '+erro.message;}
});
