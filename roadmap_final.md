# Roadmap da Ferramenta de Conversão de XML

Este documento descreve as funcionalidades implementadas e os próximos passos para a evolução da ferramenta de conversão e manipulação de XML de NFe/NFCe.

## Versão Atual: 1.0 - Conversor Universal de CRT

### Funcionalidades Implementadas

*   **[CONCLUÍDO] Carregamento e Processamento em Lote:**
    *   Permite o upload de múltiplos arquivos XML de uma só vez.
    *   Processa todos os arquivos e os agrupa em um único arquivo ZIP para download.

*   **[CONCLUÍDO] Conversão de Regime Tributário (CRT):**
    *   Interface permite ao usuário escolher o CRT de destino (1, 2 ou 3).
    *   Altera a tag `<CRT>` no XML do emitente para o valor selecionado.

*   **[CONCLUÍDO] Conversão de Tributação (CSOSN para CST):**
    *   Quando um XML com CRT 1 (Simples Nacional) é convertido para CRT 2 ou 3, a ferramenta converte automaticamente os grupos de imposto.
    *   Mapeamento de CSOSN para CST (ex: 101->00, 102->41, etc.).
    *   Recálculo do ICMS para o CST 00 com base em uma alíquota de ICMS informada pelo usuário.
    *   Opção para o usuário definir o CST de destino para o CSOSN 900.

*   **[CONCLUÍDO] Limpeza de Assinatura e Protocolo:**
    *   Remove automaticamente a tag `<Signature>` (assinatura digital) do XML.
    *   Remove automaticamente a tag `<protNFe>` (protocolo de autorização da SEFAZ) do XML.
    *   Isso garante que a nota possa ser validada ou processada por outros sistemas como um documento "frio".

*   **[CONCLUÍDO] Tratamento Inteligente de Arquivos:**
    *   A ferramenta identifica se uma conversão é necessária. Por exemplo, se o usuário tentar converter para CRT 1 um arquivo que já é CRT 1, o arquivo é ignorado para evitar processamento desnecessário.
    *   O arquivo ZIP de saída organiza os arquivos em pastas `convertidos/` e `ignorados/`.
    *   Um `relatorio.txt` é gerado detalhando a ação tomada para cada arquivo.

### Melhorias Futuras e Próximos Passos

*   **[SUGESTÃO] Suporte a mais Tipos de Impostos:**
    *   Adicionar conversão para IPI, PIS e COFINS, permitindo que a ferramenta seja usada em mais cenários (ex: notas de indústrias).

*   **[SUGESTÃO] Flexibilização das Regras de Conversão:**
    *   Permitir que o usuário personalize o mapeamento de CSOSN para CST através da interface.
    *   Adicionar mais lógicas de conversão (ex: para CST 20 - com redução de base de cálculo).

*   **[SUGESTÃO] Validação do XML Gerado:**
    *   Integrar a ferramenta com um validador de schemas XSD da NFe para garantir que o XML gerado seja 100% compatível antes de ser entregue ao usuário.

*   **[SUGESTÃO] Melhorias de Interface:**
    *   Adicionar uma barra de progresso mais detalhada durante o upload e a conversão.
    *   Exibir o relatório diretamente na tela após o processamento, além de incluí-lo no ZIP.
