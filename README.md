# Conversor de NFe/NFCe - Simples Nacional para Regime Normal

Esta é uma ferramenta para converter arquivos XML de Nota Fiscal Eletrônica (NFe) e Nota Fiscal de Consumidor Eletrônica (NFCe) do regime de tributação Simples Nacional para o Regime de Apuração Normal.

A aplicação altera o CRT (Código de Regime Tributário) do emitente, converte os códigos CSOSN para os códigos CST correspondentes e recalcula os impostos (ICMS) com base em uma alíquota informada pelo usuário.

## Ambiente de Desenvolvimento no Windows

Para uma melhor experiência de desenvolvimento no Windows, recomendamos o uso do **PowerShell 7.5** e do **Windows Terminal**.

### Instalando o PowerShell 7.5

1.  **Via Microsoft Store:**
    *   Abra a Microsoft Store no Windows 11.
    *   Procure por "PowerShell" e instale a versão mais recente.

2.  **Via Winget (no Terminal):**
    *   Abra o Windows Terminal (pode ser com o PowerShell 5 que vem com o Windows).
    *   Execute o comando:
        ```powershell
        winget install --id Microsoft.PowerShell --source winget
        ```

### Como Instalar o Python e Configurar no Windows 11

1.  **Baixe o Python:**
    *   Acesse o site oficial do Python em [python.org](https://www.python.org/downloads/).
    *   Clique no botão "Download Python" para baixar a versão mais recente.

2.  **Execute o Instalador:**
    *   Abra o arquivo que você baixou.
    *   **Importante:** Na primeira tela do instalador, marque a caixa que diz **"Add Python to PATH"**. Isso facilitará a execução de comandos Python no terminal.
    *   Clique em "Install Now".

3.  **Verifique a Instalação:**
    *   Abra o **PowerShell 7**.
    *   Digite os seguintes comandos para verificar se o Python e o pip (gerenciador de pacotes) foram instalados corretamente:
        ```powershell
        python --version
        pip --version
        ```

## Como Executar a Aplicação

As instruções variam um pouco dependendo do seu sistema operacional.

### Para Linux e macOS (usando Bash)

1.  **Ative o Ambiente Virtual:**
    ```sh
    source .venv/bin/activate
    ```

2.  **Inicie o Servidor de Desenvolvimento:**
    ```sh
    ./devserver.sh
    ```

### Para Windows (usando PowerShell)

1.  **Ative o Ambiente Virtual:**
    Primeiro, talvez seja necessário permitir a execução de scripts no seu sistema. Execute o PowerShell como Administrador e rode:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
    Depois, em um terminal normal, ative o ambiente:
    ```powershell
    . .venv/Scripts/Activate.ps1
    ```

2.  **Inicie o Servidor de Desenvolvimento:**
    ```powershell
    ./devserver.ps1
    ```

### Acesse a Aplicação

Após iniciar o servidor, a IDE mostrará uma notificação para você abrir a aplicação em uma aba de preview. Clique nela para acessar a interface web.

## Como Usar a Ferramenta

A interface web é simples e direta:

1.  **Acesse a Página:** Abra a aplicação no seu navegador.
2.  **Selecione os Arquivos:** Clique no botão "Escolher arquivos" ou arraste e solte os arquivos XML.
3.  **Defina a Alíquota de ICMS:** Insira o percentual de ICMS a ser usado.
4.  **Inicie a Conversão:** Clique em "Converter".
5.  **Baixe o Resultado:** Clique em "Download do ZIP" para baixar os arquivos convertidos.

## Comandos Úteis

### Para Linux e macOS (usando Bash)

*   **Ativar o ambiente virtual:**
    ```sh
    source .venv/bin/activate
    ```
*   **Instalar/Atualizar as dependências:**
    ```sh
    pip install -r requirements.txt
    ```
*   **Salvar novas dependências:**
    ```sh
    pip freeze > requirements.txt
    ```

### Para Windows (usando PowerShell)

*   **Ativar o ambiente virtual:**
    ```powershell
    . .venv/Scripts/Activate.ps1
    ```
*   **Instalar/Atualizar as dependências:**
    ```powershell
    pip install -r requirements.txt
    ```
*   **Salvar novas dependências:**
    ```powershell
    pip freeze > requirements.txt
    ```

## Aviso Legal

**É fundamental que você leia e compreenda os seguintes termos antes de usar a ferramenta:**

Este software foi desenvolvido para auxiliar na conversão de arquivos XML de NFe/NFCe do regime Simples Nacional para o Regime de Apuração Normal.

1.  **Responsabilidade:** O uso deste software é de inteira responsabilidade do usuário. Recomenda-se que todos os arquivos convertidos sejam cuidadosamente revisados por um profissional de contabilidade antes de serem utilizados para fins fiscais ou legais.

2.  **Precisão:** Embora tenham sido feitos todos os esforços para garantir a precisão das conversões, os desenvolvedores não se responsabilizam por quaisquer erros, omissões ou inconsistências geradas pelo software, nem por quaisquer perdas ou danos decorrentes de seu uso.

3.  **Validação:** A conversão segue as regras técnicas e de negócio especificadas, mas não substitui a validação final por parte do emissor ou do responsável fiscal. As regulamentações fiscais podem variar e sofrer alterações.

4.  **Uso:** Este software é uma ferramenta de apoio e não deve ser considerado como consultoria fiscal ou contábil.

Ao utilizar este software, você concorda com estes termos.
