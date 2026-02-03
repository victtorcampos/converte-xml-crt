# Script para rodar o servidor de desenvolvimento FastAPI com uvicorn no PowerShell

# Ativa o ambiente virtual para a sessão atual do PowerShell
# Em caso de erro de execução de script, talvez seja necessário executar:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

Write-Host "Ambiente virtual ativado."
Write-Host "Iniciando o servidor FastAPI com uvicorn..."

# Inicia o servidor na porta 8000
# O --host 0.0.0.0 torna o servidor acessível na rede local
# O --reload faz com que o servidor reinicie automaticamente após alterações no código
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
