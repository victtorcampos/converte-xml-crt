# Conversor de Regime Tributário para NFe/NFCe

Esta é uma ferramenta web para manipular arquivos XML de Nota Fiscal Eletrônica (NFe) e Nota Fiscal de Consumidor Eletrônica (NFCe), focada na alteração do regime de tributação (CRT) e na limpeza de informações de autorização para reprocessamento.

### Funcionalidades Principais

*   **Alteração de CRT:** Converte o regime tributário do emitente para Simples Nacional (1), Simples Nacional - excesso de sublimite (2) ou Regime Normal (3).
*   **Conversão de Tributação:** Ao migrar de Simples Nacional (CRT 1) para outros regimes, a ferramenta converte automaticamente os códigos CSOSN para os códigos CST equivalentes e recalcula o ICMS com base em uma alíquota configurável.
*   **Limpeza de XML:** Remove as seções `<protNFe>` e `<Signature>` do XML, permitindo que o documento seja revalidado ou transmitido a outros sistemas como uma nota "fria".
*   **Relatórios Detalhados:** Gera um `relatorio.txt` para cada lote de arquivos processados, informando o status de cada um (convertido, ignorado ou erro) e as alterações realizadas.

---

## Como Executar a Aplicação

A aplicação foi desenvolvida para ser executada em um ambiente com Python e um terminal (Bash para Linux/macOS ou PowerShell para Windows).

1.  **Ative o Ambiente Virtual:**
    *   **Linux/macOS:**
        ```sh
        source .venv/bin/activate
        ```
    *   **Windows (PowerShell):**
        ```powershell
        # Se for a primeira vez, talvez seja necessário permitir scripts:
        # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        . .venv/Scripts/Activate.ps1
        ```

2.  **Inicie o Servidor:**
    *   **Linux/macOS:**
        ```sh
        ./devserver.sh
        ```
    *   **Windows (PowerShell):**
        ```powershell
        ./devserver.ps1
        ```

3.  **Acesse a Interface:**
    Após iniciar o servidor, sua IDE deve notificá-lo para abrir a aplicação em uma aba de preview. Clique na notificação para acessar a interface web.

---

## Como Usar a Ferramenta

1.  **Upload:** Arraste e solte ou selecione os arquivos XML que deseja processar.
2.  **Configuração:**
    *   **CRT de Destino:** Escolha o regime tributário para o qual deseja converter os arquivos.
    *   **Alíquota ICMS (%):** Obrigatória apenas ao converter do CRT 1 para os regimes 2 ou 3.
    *   **Conversão CSOSN 900:** Defina o CST correspondente para o CSOSN 900 (geralmente '41' ou '90').
3.  **Conversão:** Clique em "Converter Arquivos".
4.  **Download:** Um link de download para um arquivo ZIP aparecerá. Este arquivo contém:
    *   `convertidos/`: Pasta com os XMLs que foram modificados.
    *   `ignorados/`: Pasta com os XMLs que não necessitaram de alteração (ex: converter para CRT 1 um arquivo que já era CRT 1).
    *   `relatorio.txt`: Um relatório detalhado da ação tomada em cada arquivo, incluindo CRT original, CRT de destino e se a assinatura e o protocolo foram removidos.
    *   `aviso_legal.txt`: Os termos de uso da ferramenta.

---

## Como Testar

O projeto utiliza `pytest` para testes unitários e de funcionalidades. Para executar os testes:

1.  **Ative o Ambiente Virtual** (instruções acima).
2.  **Rode o Pytest:**
    ```sh
    # É importante definir o PYTHONPATH para que os módulos da aplicação sejam encontrados
    PYTHONPATH=. pytest
    ```

---

## Comandos Úteis

*   **Instalar/Atualizar Dependências:**
    ```sh
    pip install -r requirements.txt
    ```
*   **Salvar Novas Dependências:**
    Após instalar um novo pacote com `pip install`, atualize o `requirements.txt`:
    ```sh
    pip freeze > requirements.txt
    ```

---

## Aviso Legal

**É fundamental que você leia e compreenda os seguintes termos antes de usar a ferramenta:**

Este software foi desenvolvido para auxiliar na manipulação de arquivos XML de NFe/NFCe.

1.  **Responsabilidade:** O uso deste software é de inteira responsabilidade do usuário. Recomenda-se que todos os arquivos convertidos sejam cuidadosamente revisados por um profissional de contabilidade antes de serem utilizados para fins fiscais ou legais.

2.  **Precisão:** Embora tenham sido feitos todos os esforços para garantir a precisão das conversões, os desenvolvedores não se responsabilizam por quaisquer erros, omissões ou inconsistências geradas pelo software, nem por quaisquer perdas ou danos decorrentes de seu uso.

3.  **Validação:** A conversão segue as regras técnicas e de negócio especificadas, mas não substitui a validação final por parte do emissor ou do responsável fiscal. As regulamentações fiscais podem variar e sofrer alterações.

4.  **Uso:** Este software é uma ferramenta de apoio e não deve ser considerado como consultoria fiscal ou contábil.

Ao utilizar este software, você concorda com estes termos.
