from fastapi import FastAPI, HTTPException
from src.database import get_db_connection
from src.repositories import SchoolRepository

app = FastAPI(
    title="Lunaris School API",
    description="API para gerenciamento e carga de dados da escola",
    version="1.0"
)

@app.post("/populate", tags=["Database"])
def populate_db(total_alunos: int = 40, total_turmas: int = 3):
    """
    Insere dados fictícios no banco.
    - total_alunos: Quantidade de alunos a gerar (padrão 40)
    - total_turmas: Quantidade de turmas a gerar (padrão 3)
    """
    try:
        conn = get_db_connection()
        repo = SchoolRepository(conn)
        repo.populate_database(total_alunos, total_turmas)
        conn.close()
        return {
            "status": "success", 
            "message": f"Banco populado com {total_alunos} alunos e {total_turmas} turmas."
        }
    except Exception as e:
        print(f"Erro na API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reset", tags=["Database"])
def reset_db():
    """⚠️ PERIGO: Apaga TODOS os dados de TODAS as tabelas."""
    try:
        conn = get_db_connection()
        repo = SchoolRepository(conn)
        repo.clean_database()
        conn.close()
        return {"status": "success", "message": "Todas as tabelas foram limpas (TRUNCATE)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/dashboard", tags=["Visualização"])
def get_all_data():
    """Retorna um relatório completo dos dados inseridos."""
    try:
        conn = get_db_connection()
        repo = SchoolRepository(conn)
        dados = repo.get_full_report()
        conn.close()
        return dados
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)