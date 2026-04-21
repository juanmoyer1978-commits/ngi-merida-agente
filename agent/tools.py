import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}


def obtener_horario() -> dict:
    info = cargar_info_negocio()
    return info.get("negocio", {}).get("horario", {})


def registrar_solicitud_consejeria(telefono: str, nombre: str, motivo: str) -> str:
    """Registra una solicitud de cita de consejería."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    registro = f"[{timestamp}] Tel: {telefono} | Nombre: {nombre} | Motivo: {motivo}\n"
    os.makedirs("data", exist_ok=True)
    with open("data/solicitudes_consejeria.txt", "a", encoding="utf-8") as f:
        f.write(registro)
    logger.info(f"Solicitud de consejería registrada: {telefono}")
    return "Solicitud registrada correctamente"


def buscar_en_knowledge(consulta: str) -> str:
    """Busca información relevante en los archivos de /knowledge."""
    resultados = []
    knowledge_dir = "knowledge"
    if not os.path.exists(knowledge_dir):
        return "No hay archivos disponibles."
    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue
    return "\n---\n".join(resultados) if resultados else "No encontré información específica sobre eso."
