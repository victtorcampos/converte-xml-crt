from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from app.core.validation import XMLValidator
from app.core.conversion import XMLConverter
import lxml.etree as ET
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
    """Sanitiza um nome de arquivo para uso seguro."""
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
    csosn_900_cst: str = Form('90')
):
    report_content = ""
    converted_files_for_zip = {}

    for file in files:
        original_filename = file.filename
        if not original_filename.lower().endswith('.xml') or file.content_type not in ['application/xml', 'text/xml']:
            report_content += f"{original_filename}: ❌ Erro - Arquivo não parece ser um XML válido.\n"
            continue

        sanitized_filename = secure_filename(original_filename)

        try:
            content = await file.read()
            validator = XMLValidator(content)
            validator.validate()
            
            converter = XMLConverter(
                tree=validator.tree, 
                picms=picms, 
                csosn_900_cst=csosn_900_cst
            )
            converted_xml = converter.convert()
            
            converted_filename = f"CONVERTIDO_{sanitized_filename}"
            converted_files_for_zip[converted_filename] = converted_xml
            report_content += f"{original_filename}: ✅ Convertido com sucesso\n"

        except ValueError as e:
            report_content += f"{original_filename}: ❌ Erro na Validação - {e}\n"
        except Exception as e:
            report_content += f"{original_filename}: ❌ Erro Inesperado - {e}\n"

    if not converted_files_for_zip:
        return templates.TemplateResponse("error.html", {
            "request": request, 
            "error_title": "Nenhum arquivo foi convertido",
            "error_message": "Nenhum dos arquivos enviados pôde ser convertido com sucesso. Verifique o relatório de erros abaixo:",
            "report": report_content
        })

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in converted_files_for_zip.items():
            zip_file.writestr(f"convertidos/{filename}", content)
        
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
