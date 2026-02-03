# roadmap2.md — Converte XML CRT (limpeza + seleção CRT)

## 1) Objetivo (escopo desta etapa)
Implementar no projeto a **limpeza obrigatória** do XML convertido e uma **configuração de escolha do CRT** (1/2/3), com validações por arquivo e regra de ignorar quando CRT alvo = 1 e o XML já está em CRT=1.

Itens solicitados:
- Remover do XML convertido:
  - `nfeProc\NFe\infNFe\Signature`
  - `nfeProc\protNFe`
- Adicionar em “2. Configurações” a opção de escolher CRT destino: 1, 2 ou 3.
- Atualizar `nfeProc\NFe\infNFe\emit\CRT` para o CRT escolhido.
- Validar regra por XML.
  - Se opção CRT=1 e XML já está CRT=1: **ignorar arquivo (não alterar)**.

## 2) Critérios de aceite (objetivos verificáveis)
- Ao converter, o XML **não contém** `protNFe` e **não contém** `Signature` em `infNFe`.
- O campo `<emit><CRT>` no XML convertido corresponde ao CRT escolhido pelo usuário.
- Para cada XML:
  - Se CRT alvo = 1 e CRT do XML = 1 → arquivo entra como **IGNORADO** e o conteúdo original é preservado (sem mudanças).
- ZIP final contém:
  - XMLs convertidos (e, opcionalmente, os ignorados em pasta separada) + log que diferencia OK/IGNORADO/ERRO.

## 3) Decisões técnicas (não inventar depois)
- Parser XML: `lxml`.
- Namespace NF-e: `http://www.portalfiscal.inf.br/nfe`.
- Estratégia de remoção:
  - Remover `//nfe:protNFe` quando existir dentro de `nfeProc`.
  - Remover `//nfe:Signature` (pode estar sob `infNFe` ou outros pontos), mas o requisito mínimo é `nfeProc/NFe/infNFe/Signature`.
- A aplicação **não** tenta “reassinar” XML.

## 4) Roteiro (passo a passo)

### 4.1 Backend — Configuração CRT
1. Criar/atualizar modelo de configuração (Pydantic) com campo `target_crt: Literal[1,2,3]`.
2. Expor essa opção no endpoint de conversão (form field ou JSON, dependendo do fluxo atual).
3. Validar: se `target_crt` ausente → default (defina explicitamente; sugestão: 3).

### 4.2 Backend — Leitura CRT atual do XML
1. Implementar função `get_current_crt(xml_root) -> int | None`:
   - XPath: `//nfe:infNFe/nfe:emit/nfe:CRT`.
2. Se não encontrado → marcar arquivo como ERRO (não tentar inferir).

### 4.3 Regra de “ignorar”
1. Se `target_crt == 1` e `current_crt == 1`:
   - Não remover `protNFe` e não mexer em `Signature` (porque você não está convertendo).
   - Registrar no log: `IGNORADO (já CRT=1)`.
   - Gravar XML original no ZIP em `/ignorados/` (ou manter fora do ZIP; escolha e documente).

### 4.4 Atualizar CRT no XML
1. Se arquivo não for ignorado:
   - Setar texto da tag `<CRT>` para `str(target_crt)`.
2. Se `target_crt` == `current_crt` (2→2, 3→3):
   - Não foi pedido, mas decida: **converter mesmo assim** (para limpeza Signature/protNFe) ou **ignorar**. (Sugestão: converter/limpar, porque o requisito de remoção vale para “xml convertido”.)

### 4.5 Remoção de `protNFe` e `Signature`
1. Remover `protNFe`:
   - XPath: `//nfe:protNFe`.
   - Remover o nó do parent.
2. Remover `Signature`:
   - XPath: `//nfe:Signature`.
   - Remover todos os nós encontrados.
3. Garantir que não gere tags com `xmlns=""` (criação de elementos deve incluir namespace correto).

### 4.6 Log e ZIP
1. Log por arquivo com status:
   - `OK_CONVERTIDO`, `IGNORADO`, `ERRO`.
2. Log deve incluir:
   - CRT original, CRT destino, Signature removida? protNFe removido?

### 4.7 Testes (mínimo)
1. Fixture com XML `nfeProc` contendo `NFe` + `protNFe` + `Signature`.
2. Testar:
   - Quando converter (target_crt=3): `protNFe` removido, `Signature` removida, CRT alterado.
   - Quando ignorar (target_crt=1 e current_crt=1): XML byte-a-byte igual ao original.

## 5) Checklist (para preencher durante o desenvolvimento)

### Preparação
- [ ] Confirmar o fluxo atual da UI (“2. Configurações”) e onde adicionar o seletor CRT.
- [ ] Confirmar o contrato do endpoint (multipart? JSON?) e como receber `target_crt`.

### Implementação
- [ ] Adicionar `target_crt` no modelo/configuração.
- [ ] Implementar leitura do CRT atual do XML.
- [ ] Implementar regra de ignorar (CRT=1 e XML CRT=1).
- [ ] Implementar atualização do `<emit><CRT>`.
- [ ] Implementar remoção de `protNFe`.
- [ ] Implementar remoção de `Signature`.
- [ ] Ajustar criação/alteração de tags para preservar namespace.

### Saída e observabilidade
- [ ] Atualizar ZIP para separar `convertidos/` e `ignorados/` (ou documentar comportamento).
- [ ] Gerar `log.txt` com OK/IGNORADO/ERRO.

### Testes
- [ ] Criar fixtures de XML com `protNFe` e `Signature`.
- [ ] Teste unitário: conversão remove `protNFe` e `Signature`.
- [ ] Teste unitário: regra IGNORAR preserva XML.
- [ ] Teste de regressão: conversão em lote não quebra para múltiplos arquivos.

### Finalização
- [ ] Atualizar README: opção CRT, regra de ignorar, e o que é removido do XML.
- [ ] Versionar (tag) a entrega desta etapa.
