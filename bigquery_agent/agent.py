"""
Este agente consulta el tool de BigQuery para brindar respuestas sobre tablas y datos de la base de datos
PROJECT_ID: mundomotrizdev
DATASET: db_poc_agente_ia
TABLE: stg_venta_diaria
Documentación de Google ADK para bigquery: https://google.github.io/adk-docs/tools/built-in-tools/#bigquery
"""

import asyncio
import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode
from google.genai import types
from google.oauth2 import service_account

# Constantes del proyecto
PROJECT_ID = "mundomotrizdev"
DATASET = "db_poc_agente_ia"
TABLE = "stg_venta_diaria"

# Constantes del agente
AGENT_NAME = "bigquery_data_agent"
APP_NAME = "urbanova_data_app"
USER_ID = "user_urbanova"
SESSION_ID = "session_001"
GEMINI_MODEL = "gemini-2.5-flash"

# Ruta al archivo de service account
# Puede configurarse mediante variable de entorno o usar ruta por defecto
SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE",
    os.path.join(os.path.dirname(__file__), "mundomotrizdev-b0dcd30bbaa7.json")
)

# Configuración del tool de BigQuery para bloquear operaciones de escritura
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

# Cargar credenciales desde el archivo de service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/bigquery"]
)

# Configurar BigQueryCredentialsConfig con las credenciales del service account
credentials_config = BigQueryCredentialsConfig(credentials=credentials)

# Instanciar el BigQuery toolset con las credenciales del service account
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    bigquery_tool_config=tool_config
)

# Definición del agente de BigQuery
root_agent = Agent(
    model=GEMINI_MODEL,
    name=AGENT_NAME,
    description=(
        f"Agente especializado en consultar datos de BigQuery del proyecto {PROJECT_ID}, "
        f"específicamente del dataset {DATASET} y la tabla {TABLE}. "
        "Puede ejecutar consultas SQL, obtener información de tablas y responder preguntas sobre los datos."
    ),
    instruction=f"""
        Eres un agente de datos especializado con acceso a BigQuery.
        
        Información del proyecto:
        - PROJECT_ID: {PROJECT_ID}
        - DATASET: {DATASET}
        - TABLE PRINCIPAL: {TABLE}
        
        Tienes acceso a las siguientes herramientas de BigQuery:
        - list_dataset_ids: Para listar los datasets disponibles en el proyecto
        - get_dataset_info: Para obtener información sobre un dataset específico
        - list_table_ids: Para listar las tablas en un dataset
        - get_table_info: Para obtener el esquema y metadatos de una tabla
        - execute_sql: Para ejecutar consultas SQL y obtener resultados
        - forecast: Para realizar predicciones de series temporales usando AI.FORECAST
        - ask_data_insights: Para responder preguntas sobre los datos usando lenguaje natural
        
        Cuando el usuario haga preguntas:
        1. Primero, explora la estructura de datos si es necesario (tablas, esquemas)
        2. Formula consultas SQL apropiadas para responder la pregunta
        3. Ejecuta las consultas y presenta los resultados de forma clara
        4. Proporciona insights y análisis basados en los datos
        
        Siempre responde en español y sé claro y conciso en tus respuestas.
    """,
    tools=[bigquery_toolset],
)

# Servicio de sesión y Runner
session_service = InMemorySessionService()

# Crear sesión de forma síncrona para inicialización
def initialize_session():
    """Inicializa la sesión del agente"""
    return asyncio.run(
        session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    )

# Runner para ejecutar el agente
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# Función helper para interactuar con el agente
def consultar_agente(query: str):
    """
    Función helper para consultar el agente con una pregunta.
    
    Args:
        query: La pregunta o consulta para el agente
        
    Returns:
        La respuesta del agente
    """
    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    
    print(f"\n{'='*80}")
    print(f"USUARIO: {query}")
    print(f"{'='*80}")
    
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print(f"AGENTE: {final_response}")
            print(f"{'='*80}\n")
            return final_response
    
    return None


# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar sesión
    session = initialize_session()
    print(f"Sesión inicializada: {session.id}")
    print(f"Agente: {AGENT_NAME}")
    print(f"Proyecto: {PROJECT_ID}")
    print(f"Dataset: {DATASET}")
    print(f"Tabla principal: {TABLE}\n")
    
    # Ejemplos de consultas
    consultar_agente(f"¿Qué datasets existen en el proyecto {PROJECT_ID}?")
    
    consultar_agente(f"Dame información sobre el dataset {DATASET}")
    
    consultar_agente(f"¿Qué tablas hay en el dataset {DATASET}?")
    
    consultar_agente(f"Describe la estructura de la tabla {TABLE}")
    
    consultar_agente(f"¿Cuántos registros hay en la tabla {TABLE}?")
    
    consultar_agente(f"Muéstrame un resumen de las ventas diarias en la tabla {TABLE}")