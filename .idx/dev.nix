{ pkgs, ... }: {
  # ============================================================================
  # FIREBASE STUDIO / IDX - CONFIGURAÇÃO PARA PROJETO PYTHON FASTAPI
  # Projeto: converte-xml-crt
  # ============================================================================

  # Qual canal Nix usar (estável recomendado)
  channel = "stable-24.05"; # Versão estável mais recente (suporta Python 3.11+)

  # ============================================================================
  # PACOTES SYSTEM
  # ============================================================================
  # https://search.nixos.org/packages para procurar pacotes
  packages = [
    # === Python Core ===
    pkgs.python311                    # Python 3.11 (versão estável)
    pkgs.python311Packages.pip        # Gerenciador de pacotes Python

    # === Quality of Life (Opcionais) ===
    pkgs.git                          # Para operações Git no terminal
    pkgs.curl                         # Para testes de API (ex: curl localhost:8000)
    pkgs.nano                         # Editor de texto simples
  ];

  # ============================================================================
  # VARIÁVEIS DE AMBIENTE
  # ============================================================================
  env = {
    # Garante que output Python seja exibido em tempo real (não bufferizado)
    # Crítico para logs de uvicorn/FastAPI no IDX
    PYTHONUNBUFFERED = "1";

    # Ambiente de desenvolvimento (útil para debugging)
    APP_ENV = "development";
  };

  # ============================================================================
  # CONFIGURAÇÃO IDX
  # ============================================================================
  idx = {
    # === Extensões do VS Code ===
    # IDs retirados de https://open-vsx.org/
    extensions = [
      "ms-python.python"              # IntelliSense, debugging, formato
      "ms-python.vscode-pylance"      # Type checking avançado (Type Checker)
      "ms-python.flake8"              # Linting (análise de código)
    ];

    # ============================================================================
    # PREVIEW WEB (Executar app em tempo real)
    # ============================================================================
    previews = {
      enable = true;                  # Ativar previews

      previews = {
        # Configuração do servidor FastAPI
        web = {
          # Comando: ativa venv + inicia uvicorn
          # $PORT é injetado automaticamente pelo IDX (normalmente 8000)
          command = [
            "bash" "-c"
            "source .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload"
          ];

          # Manager informa ao IDX que é um preview web
          manager = "web";
        };
      };
    };

    # ============================================================================
    # LIFECYCLE HOOKS - AUTOMAÇÃO NA CRIAÇÃO/REINÍCIO DO WORKSPACE
    # ============================================================================
    workspace = {
      # === onCreate: Executado UMA VEZ ao criar o workspace ===
      # Ideal para: setup inicial, criação de venv, instalação de deps
      onCreate = {
        # Cria ambiente virtual Python isolado
        # Nota: "bash" é necessário para source .venv/bin/activate funcionar
        venv = ''
          echo "📦 Criando ambiente virtual Python..."
          python3 -m venv .venv
          echo "✅ Ambiente virtual criado em .venv/"
        '';

        # Instala dependências do requirements.txt
        pip-install = ''
          echo "📥 Instalando dependências de requirements.txt..."
          source .venv/bin/activate
          pip install --upgrade pip setuptools wheel
          pip install -r requirements.txt
          echo "✅ Dependências instaladas!"
        '';

        # (Opcional) Cria pasta para downloads/uploads de XMLs
        setup-dirs = ''
          echo "📁 Criando pastas de trabalho..."
          mkdir -p downloads uploads logs
          echo "✅ Pastas criadas: downloads/, uploads/, logs/"
        '';
      };

      # === onStart: Executado SEMPRE que o workspace (re)inicia ===
      # Ideal para: mensagens, checks, limpeza de cache, etc
      onStart = {
        # Mensagem de boas-vindas
        welcome = ''
          echo ""
          echo "╔═══════════════════════════════════════════════════════╗"
          echo "║  🚀 Converte XML CRT - Ambiente FastAPI Pronto!       ║"
          echo "║  Project: converte-xml-crt                             ║"
          echo "║  Python: $(python --version)                               ║"
          echo "║  FastAPI: Acesse http://localhost:$PORT/docs               ║"
          echo "╚═══════════════════════════════════════════════════════╝"
          echo ""
        '';

        # Limpeza de cache Python (evita conflitos)
        clean-cache = ''
          echo "🧹 Limpando cache Python..."
          find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
          find . -type f -name "*.pyc" -delete 2>/dev/null || true
        '';
      };
    };
  };

  # ============================================================================
  # NOTAS E TROUBLESHOOTING
  # ============================================================================
  # 1. Se receber erro "source: command not found"
  #    → Use "bash -c" para executar comandos com source (conforme implementado)
  #
  # 2. Para recriar o ambiente manualmente:
  #    → Terminal: "idx rebuild" (reconstrói workspace)
  #    → Ou: Delete .venv/ e execute onCreate novamente
  #
  # 3. Se uvicorn não iniciar no preview:
  #    → Verifique se app/main.py existe e tem função app = FastAPI()
  #    → Verifique arquivo de log no terminal do IDX
  #
  # 4. Para atualizar requirements.txt:
  #    → source .venv/bin/activate
  #    → pip install <novo-pacote>
  #    → pip freeze > requirements.txt
  #    → Commit changes
  #
  # 5. Debugger do Python:
  #    → Instale breakpoint() no código
  #    → VS Code vai parar no breakpoint (Pylance)
  #
}
