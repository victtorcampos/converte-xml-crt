from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from app.core.validation import XMLValidator
from app.core.conversion import XMLConverter
import zipfile
import io
import uuid
import re
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

generated_zips: Dict[str, bytes] = {}

def secure_filename(filename: str) -> str:
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    filename = filename.strip('._-')
    return filename if filename else "arquivo_sem_nome.xml"

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_files(
    request: Request,
    files: List[UploadFile] = File(...),
    picms: float = Form(17.0),
    csosn_900_cst: str = Form('90'),
    target_crt: int = Form(...)
):
    report_lines = ["Relatório de Processamento de Arquivos", "========================================="]
    converted_files_for_zip: Dict[str, bytes] = {}
    ignored_files_for_zip: Dict[str, bytes] = {}

    for file in files:
        original_filename = file.filename
        sanitized_filename = secure_filename(original_filename)
        file_report = [f"Arquivo: {original_filename}"]

        if not original_filename.lower().endswith('.xml') or file.content_type not in ['application/xml', 'text/xml']:
            file_report.append("Status: ❌ ERRO")
            file_report.append("Detalhes: Arquivo não parece ser um XML válido.")
            report_lines.append("\n".join(file_report))
            continue

        try:
            content = await file.read()
            original_content = content

            validator = XMLValidator(content)
            validator.validate()
            
            converter = XMLConverter(
                tree=validator.tree, 
                picms=picms, 
                csosn_900_cst=csosn_900_cst,
                target_crt=target_crt
            )
            converted_xml, conversion_report = converter.convert()

            status = conversion_report.get('status', 'ERRO')
            file_report.append(f"Status: {status}")
            file_report.append("--------------------")
            file_report.append(f"CRT Original: {conversion_report.get('original_crt', 'N/A')}")
            file_report.append(f"CRT Destino: {conversion_report.get('target_crt', 'N/A')}")
            file_report.append(f"Assinatura Removida: {'Sim' if conversion_report.get('signature_removed') else 'Não'}")
            file_report.append(f"Protocolo Removido: {'Sim' if conversion_report.get('protnfe_removed') else 'Não'}")

            if status == 'IGNORADO':
                ignored_files_for_zip[sanitized_filename] = original_content
                file_report.append("Detalhes: O CRT de origem e destino são '1'. Nenhuma alteração necessária.")
            elif status == 'CONVERTIDO':
                converted_filename = f"CONVERTIDO_{sanitized_filename}"
                converted_files_for_zip[converted_filename] = converted_xml
                file_report.append("Detalhes: O arquivo foi modificado com sucesso.")

        except ValueError as e:
            file_report.append("Status: ❌ ERRO")
            file_report.append(f"Detalhes: Erro na validação - {e}")
        except Exception as e:
            file_report.append("Status: ❌ ERRO")
            file_report.append(f"Detalhes: Erro inesperado - {e}")
        
        report_lines.append("\n".join(file_report))

    if not converted_files_for_zip and not ignored_files_for_zip:
        return templates.TemplateResponse("error.html", {
            "request": request, 
            "error_title": "Nenhum arquivo processado",
            "error_message": "Nenhum dos arquivos pôde ser processado. Verifique o relatório:",
            "report": "\n\n".join(report_lines)
        })

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in converted_files_for_zip.items():
            zip_file.writestr(f"convertidos/{filename}", content)
        for filename, content in ignored_files_for_zip.items():
            zip_file.writestr(f"ignorados/{filename}", content)

        report_content = "\n\n".join(report_lines)
        zip_file.writestr("relatorio.txt", report_content)
        
        with open("app/static/aviso_legal.txt", "r") as f:
            zip_file.writestr("aviso_legal.txt", f.read())

    zip_id = str(uuid.uuid4())
    generated_zips[zip_id] = zip_buffer.getvalue()
    
    download_link = f"/download/zip/{zip_id}"
    return templates.TemplateResponse("zip_download.html", {"request": request, "download_link": download_link})

@app.get("/download/zip/{zip_id}")
async def download_zip(zip_id: str):
    if zip_id not in generated_zips:
        raise HTTPException(status_code=404, detail="Arquivo ZIP não encontrado ou expirado.")
    
    zip_content = generated_zips.pop(zip_id)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"NFe_Convertidas_{timestamp}.zip"

    return Response(
        content=zip_content,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
