import random
from src.generators import DataFactory

class SchoolRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.factory = DataFactory()

    def clean_database(self):
        """Apaga TODOS os dados usando CASCADE."""
        tables = ["boletim", "observacoes", "turma_disciplina_professor", "aluno", 
                  "professor", "turma", "disciplina", "genero", "role"]
        for table in tables:
            self.cursor.execute(f"TRUNCATE TABLE public.{table} RESTART IDENTITY CASCADE;")
        self.conn.commit()

    def populate_database(self, num_alunos, num_turmas):
            self.cursor.execute("INSERT INTO public.genero (nome) VALUES ('Masculino'), ('Feminino'), ('Outro');")
            self.cursor.execute("INSERT INTO public.role (nome) VALUES ('Admin'), ('Professor'), ('Aluno');")

            discs = ['Matemática', 'Português', 'História', 'Geografia', 'Física', 
                    'Química', 'Biologia', 'Informática', 'Ed. Física', 'Inglês']
            for d in discs:
                url = f"http://cdn.lunaris.org.br/{d.lower()}.png"
                self.cursor.execute("INSERT INTO public.disciplina (nome, url_photo) VALUES (%s, %s)", (d, url))

            prof_cpfs = []
            for i in range(1, 11):
                p = self.factory.generate_person()
                prof_cpfs.append(p['cpf'])
                self.cursor.execute("""
                    INSERT INTO public.professor (cpf, nome, email, senha, disciplina_id, role_id, data_contratacao) 
                    VALUES (%s, %s, %s, 'hash123', %s, 2, %s)
                """, (p['cpf'], p['nome'], p['email'], i, p['data']))

            series = ["9º Ano", "1º Ano Médio", "2º Ano Médio", "3º Ano Médio"]
            letras = ["A", "B", "C", "D", "E", "F"]
            
            for i in range(num_turmas):
                serie_idx = i % len(series)
                letra_idx = i // len(series)
                if letra_idx >= len(letras): letra_idx = 0
                
                nome_turma = f"{series[serie_idx]} {letras[letra_idx]}"
                self.cursor.execute("INSERT INTO public.turma (nome, ano_letivo) VALUES (%s, 2026)", (nome_turma,))

            aluno_cpfs = []
            for _ in range(num_alunos):
                a = self.factory.generate_student()
                aluno_cpfs.append(a['cpf'])
                self.cursor.execute("""
                    INSERT INTO public.aluno (cpf, nome, matricula, email, senha, role_id, genero_id) 
                    VALUES (%s, %s, %s, %s, 'senha123', 3, %s)
                """, (a['cpf'], a['nome'], a['matricula'], a['email'], a['genero_id']))

            for i, cpf in enumerate(prof_cpfs):
                turma_id = (i % num_turmas) + 1
                
                disciplina_id = i + 1 
                
                self.cursor.execute("""
                    INSERT INTO public.turma_disciplina_professor (turma_id, disciplina_id, professor_cpf) 
                    VALUES (%s, %s, %s)
                """, (turma_id, disciplina_id, cpf))
                
                alunos_sorteados = random.sample(aluno_cpfs, k=min(5, len(aluno_cpfs)))
                for a_cpf in alunos_sorteados:
                    n1 = round(random.uniform(4, 10), 2)
                    n2 = round(random.uniform(4, 10), 2)
                    media = (n1 + n2) / 2
                    self.cursor.execute("""
                        INSERT INTO public.boletim (disciplina_id, aluno_id, nota1, nota2, media)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (disciplina_id, a_cpf, n1, n2, media))

            self.conn.commit()

    def get_full_report(self):
            """Busca todos os dados formatados para JSON."""
            
            def rows_to_dict(cursor):
                if not cursor.description:
                    return []
                columns = [col[0] for col in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results

            report = {}

            self.cursor.execute("SELECT cpf, nome, email, matricula FROM public.aluno ORDER BY nome ASC")
            report["alunos"] = rows_to_dict(self.cursor)

            self.cursor.execute("""
                SELECT p.nome, p.email, d.nome as disciplina 
                FROM public.professor p
                JOIN public.disciplina d ON p.disciplina_id = d.id
            """)
            report["professores"] = rows_to_dict(self.cursor)

            self.cursor.execute("SELECT * FROM public.turma")
            report["turmas"] = rows_to_dict(self.cursor)
            
            self.cursor.execute("SELECT count(*) FROM public.aluno")
            total_alunos = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT count(*) FROM public.boletim")
            total_notas = self.cursor.fetchone()[0]

            report["resumo"] = {
                "total_alunos": total_alunos,
                "total_notas_lancadas": total_notas
            }

            return report