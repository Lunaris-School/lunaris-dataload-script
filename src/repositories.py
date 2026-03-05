import random
import bcrypt
from src.generators import DataFactory


def _bcrypt_hash(password: str, rounds: int = 10) -> str:
    """Gera hash BCrypt (compatível com Spring Security BCryptPasswordEncoder)."""
    salt = bcrypt.gensalt(rounds=rounds)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


class SchoolRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.factory = DataFactory()

    def clean_database(self):
        """Apaga TODOS os dados usando CASCADE."""
        tables = [
            "notas",
            "pre_cadastro",
            "observacoes",
            "boletim",
            "turma_disciplina_professor",
            "aluno",
            "administrador",
            "professor",
            "turma",
            "disciplina",
            "genero",
            "role",
        ]
        for table in tables:
            self.cursor.execute(f"TRUNCATE TABLE public.{table} RESTART IDENTITY CASCADE;")
        self.conn.commit()

    def populate_database(self, num_alunos, num_turmas):
        default_password = "senha@123"

        self.cursor.execute("INSERT INTO public.genero (nome) VALUES ('Masculino'), ('Feminino'), ('Outro');")
        self.cursor.execute("INSERT INTO public.role (nome) VALUES ('Admin'), ('Professor'), ('Aluno');")

        self.cursor.execute("SELECT id FROM public.role WHERE nome = 'Admin'")
        admin_role_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT id FROM public.role WHERE nome = 'Professor'")
        professor_role_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT id FROM public.role WHERE nome = 'Aluno'")
        aluno_role_id = self.cursor.fetchone()[0]

        admin = self.factory.generate_person()
        admin_password_hash = _bcrypt_hash(default_password)
        self.cursor.execute(
            """
            INSERT INTO public.administrador (nome, senha, email, role_id)
            VALUES (%s, %s, %s, %s)
            """,
            (admin["nome"], admin_password_hash, admin["email"], admin_role_id),
        )

        discs = [
            "Matemática",
            "Italiano",
            "História",
            "Geografia",
            "Física",
            "Química",
            "Biologia",
            "Informática",
            "Ed. Física",
            "Inglês",
        ]

        disciplina_ids = []
        for d in discs:
            url = f"http://cdn.lunaris.org.br/{d.lower()}.png"
            self.cursor.execute(
                """
                INSERT INTO public.disciplina (nome, url_photo)
                VALUES (%s, %s)
                RETURNING id
                """,
                (d, url),
            )
            disciplina_ids.append(self.cursor.fetchone()[0])

        prof_cpfs = []
        for i in range(10):
            p = self.factory.generate_person()
            prof_cpfs.append(p["cpf"])
            disciplina_id = disciplina_ids[i % len(disciplina_ids)]
            professor_password_hash = _bcrypt_hash(default_password)
            self.cursor.execute(
                """
                INSERT INTO public.professor (cpf, nome, email, senha, data_contratacao, disciplina_id, role_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    p["cpf"],
                    p["nome"],
                    p["email"],
                    professor_password_hash,
                    p["data"],
                    disciplina_id,
                    professor_role_id,
                ),
            )

        series = ["9º Ano", "1º Ano Médio", "2º Ano Médio", "3º Ano Médio"]
        letras = ["A", "B", "C", "D", "E", "F"]

        for i in range(num_turmas):
            serie_idx = i % len(series)
            letra_idx = i // len(series)
            if letra_idx >= len(letras):
                letra_idx = 0

            nome_turma = f"{series[serie_idx]} {letras[letra_idx]}"
            self.cursor.execute(
                "INSERT INTO public.turma (nome, ano_letivo) VALUES (%s, 2026)", (nome_turma,)
            )

        aluno_cpfs = []
        for idx in range(num_alunos):
            a = self.factory.generate_student()
            aluno_cpfs.append(a["cpf"])
            turma_id = (idx % num_turmas) + 1
            aluno_password_hash = _bcrypt_hash(default_password)
            self.cursor.execute(
                """
                INSERT INTO public.aluno (cpf, nome, matricula, email, senha, genero_id, role_id, turma_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    a["cpf"],
                    a["nome"],
                    a["matricula"],
                    a["email"],
                    aluno_password_hash,
                    a["genero_id"],
                    aluno_role_id,
                    turma_id,
                ),
            )

            if random.random() < 0.3:
                self.cursor.execute(
                    """
                    INSERT INTO public.pre_cadastro (aluno_cpf, data_autorizacao)
                    VALUES (%s, CURRENT_DATE)
                    """,
                    (a["cpf"],),
                )

        for i, cpf in enumerate(prof_cpfs):
            turma_id = (i % num_turmas) + 1
            disciplina_id = disciplina_ids[i % len(disciplina_ids)]
            self.cursor.execute(
                """
                INSERT INTO public.turma_disciplina_professor (turma_id, disciplina_id, professor_cpf)
                VALUES (%s, %s, %s)
                """,
                (turma_id, disciplina_id, cpf),
            )

            alunos_da_turma = [
                a_cpf
                for a_idx, a_cpf in enumerate(aluno_cpfs)
                if ((a_idx % num_turmas) + 1) == turma_id
            ]
            for a_cpf in random.sample(alunos_da_turma, k=min(2, len(alunos_da_turma))):
                self.cursor.execute(
                    """
                    INSERT INTO public.observacoes (aluno_cpf, professor_cpf, observacao)
                    VALUES (%s, %s, %s)
                    """,
                    (a_cpf, cpf, "Participação e desempenho acompanhados."),
                )


        for a_idx, a_cpf in enumerate(aluno_cpfs):
            turma_id = (a_idx % num_turmas) + 1

            if random.random() < 0.7:
                self.cursor.execute(
                    """
                    INSERT INTO public.boletim (aluno_cpf, turma_id, media_final)
                    VALUES (%s, %s, NULL)
                    RETURNING id
                    """,
                    (a_cpf, turma_id),
                )
                boletim_id = self.cursor.fetchone()[0]

                n1 = round(random.uniform(4, 10), 2)
                n2 = round(random.uniform(4, 10), 2)
                media_final = round((n1 + n2) / 2, 2)

                self.cursor.execute(
                    """
                    INSERT INTO public.notas (boletim_id, valor_nota, valor_nota2, tipo_avaliacao, data_lancamento)
                    VALUES (%s, %s, %s, %s, CURRENT_DATE)
                    """,
                    (boletim_id, n1, n2, "Bimestre"),
                )

                self.cursor.execute(
                    "UPDATE public.boletim SET media_final = %s WHERE id = %s",
                    (media_final, boletim_id),
                )

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

        self.cursor.execute(
            """
            SELECT id, nome, email, role_id
            FROM public.administrador
            ORDER BY nome ASC
            """
        )
        report["administradores"] = rows_to_dict(self.cursor)

        self.cursor.execute(
            """
            SELECT a.cpf, a.nome, a.email, a.matricula, t.nome as turma
            FROM public.aluno a
            LEFT JOIN public.turma t ON t.id = a.turma_id
            ORDER BY a.nome ASC
            """
        )
        report["alunos"] = rows_to_dict(self.cursor)

        self.cursor.execute(
            """
            SELECT p.nome, p.email, d.nome as disciplina
            FROM public.professor p
            JOIN public.disciplina d ON p.disciplina_id = d.id
            """
        )
        report["professores"] = rows_to_dict(self.cursor)

        self.cursor.execute("SELECT * FROM public.turma")
        report["turmas"] = rows_to_dict(self.cursor)

        self.cursor.execute("SELECT count(*) FROM public.aluno")
        total_alunos = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT count(*) FROM public.boletim")
        total_boletins = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT count(*) FROM public.notas")
        total_notas = self.cursor.fetchone()[0]

        report["resumo"] = {
            "total_alunos": total_alunos,
            "total_boletins": total_boletins,
            "total_notas_lancadas": total_notas,
        }

        return report