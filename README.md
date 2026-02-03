# Conversor de NFe/NFCe - Simples Nacional para Regime Normal

Esta é uma ferramenta para converter arquivos XML de Nota Fiscal Eletrônica (NFe) e Nota Fiscal de Consumidor Eletrônica (NFCe) do regime de tributação Simples Nacional para o Regime de Apuração Normal.

A aplicação altera o CRT (Código de Regime Tributário) do emitente, converte os códigos CSOSN para os códigos CST correspondentes e recalcula os impostos (ICMS) com base em uma alíquota informada pelo usuário.

## Como Executar a Aplicação

O ambiente de desenvolvimento já está configurado para facilitar a execução. Siga os passos abaixo:

1.  **Ative o Ambiente Virtual:**
    Antes de executar qualquer comando, é essencial ativar o ambiente virtual que contém as dependências do projeto.
    ```sh
    source .venv/bin/activate
    ```

2.  **Inicie o Servidor de Desenvolvimento:**
    Use o script `devserver.sh` para iniciar o servidor web. Ele cuidará de executar a aplicação na porta correta para o ambiente.
    ```sh
    ./devserver.sh
    ```

3.  **Acesse a Aplicação:**
    Após iniciar o servidor, a IDE mostrará uma notificação para você abrir a aplicação em uma aba de preview. Clique nela para acessar a interface web.

## Como Usar a Ferramenta

A interface web é simples e direta:

1.  **Acesse a Página:** Abra a aplicação no seu navegador, conforme o passo 3 acima.

2.  **Selecione os Arquivos:** Clique no botão "Escolher arquivos" ou arraste e solte os arquivos XML de NFe/NFCe que você deseja converter.

3.  **Defina a Alíquota de ICMS:** No campo "Alíquota de ICMS (%)", insira o percentual de ICMS que será usado para calcular o imposto nos produtos.

4.  **Inicie a Conversão:** Clique no botão "Converter". A aplicação processará todos os arquivos.

5.  **Baixe o Resultado:** Ao final do processo, um botão "Download do ZIP" aparecerá. Clique nele para baixar um arquivo `.zip` contendo todos os XMLs convertidos e um relatório da operação.

## Aviso Legal

**É fundamental que você leia e compreenda os seguintes termos antes de usar a ferramenta:**

Este software foi desenvolvido para auxiliar na conversão de arquivos XML de NFe/NFCe do regime Simples Nacional para o Regime de Apuração Normal.

1.  **Responsabilidade:** O uso deste software é de inteira responsabilidade do usuário. Recomenda-se que todos os arquivos convertidos sejam cuidadosamente revisados por um profissional de contabilidade antes de serem utilizados para fins fiscais ou legais.

2.  **Precisão:** Embora tenham sido feitos todos os esforços para garantir a precisão das conversões, os desenvolvedores não se responsabilizam por quaisquer erros, omissões ou inconsistências geradas pelo software, nem por quaisquer perdas ou danos decorrentes de seu uso.

3.  **Validação:** A conversão segue as regras técnicas e de negócio especificadas, mas não substitui a validação final por parte do emissor ou do responsável fiscal. As regulamentações fiscais podem variar и sofrer alterações.

4.  **Uso:** Este software é uma ferramenta de apoio e não deve ser considerado como consultoria fiscal ou contábil.

Ao utilizar este software, você concorda com estes termos.
