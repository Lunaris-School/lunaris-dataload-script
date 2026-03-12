# 🌙 Lunaris DataLoad Script - Sistema de Carga de Dados Escolares

Uma API FastAPI robusta e automatizada para popular bancos de dados PostgreSQL com dados fictícios realistas de um sistema de gestão escolar completo.

## 📋 Sobre o Projeto

O **Lunaris DataLoad Script** é uma ferramenta desenvolvida para facilitar o processo de desenvolvimento e testes do sistema Lunaris School. Ele automatiza a geração e inserção de dados fictícios em massa, permitindo simular cenários reais de uma instituição educacional.

**Características principais:**

- 🎲 **Geração de Dados Realistas**: Utiliza Faker para criar nomes, CPFs, emails e datas em português brasileiro
- 🔐 **Segurança Integrada**: Implementa hash BCrypt compatível com Spring Security
- 🎯 **API RESTful**: Interface FastAPI com documentação automática (Swagger)
- 🗄️ **Gestão Completa de Banco**: Operações de população e limpeza de dados
- 📊 **Dashboard de Visualização**: Endpoint para relatório completo dos dados inseridos
- ⚡ **Configurável**: Quantidade personalizável de registros via parâmetros

**Módulos de Dados Gerados:**

- **Perfis de Usuário**: Administradores, Professores e Alunos com autenticação
- **Estrutura Acadêmica**: Turmas, Disciplinas e relacionamentos
- **Sistema de Avaliação**: Boletins, Notas e observações pedagógicas
- **Gestão de Acesso**: Roles e permissões por perfil
- **Dados Demográficos**: Gêneros e informações pessoais

## 🚀 Tecnologias

| Tecnologia | Descrição |
|------------|-----------|
| **Python 3.13** | Linguagem base do projeto |
| **FastAPI 0.110.0** | Framework web moderno e de alta performance |
| **Uvicorn 0.27.1** | Servidor ASGI para aplicações assíncronas |
| **pg8000 1.30.5** | Driver PostgreSQL puro em Python |
| **Faker 23.2.1** | Gerador de dados fictícios realistas |
| **BCrypt 4.1.3** | Biblioteca para hash seguro de senhas |
| **python-dotenv 1.0.1** | Gerenciamento de variáveis de ambiente |

## 📁 Estrutura do Projeto

```
lunaris-dataload-script/
│
├── main.py                    # Aplicação FastAPI principal com endpoints
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação principal
├── STRUCTURE.md              # Documentação detalhada da estrutura
├── LICENSE                    # Licença MIT
│
├── src/                       # Código-fonte principal
│   ├── __init__.py           # Inicializador do pacote
│   ├── database.py           # Conexão e configuração do PostgreSQL
│   ├── generators.py         # Factories para geração de dados fictícios
│   ├── repositories.py       # Lógica de negócio e operações de BD
│   └── utils.py              # Funções utilitárias (formatação, limpeza)
│
└── __pycache__/              # Cache de bytecode Python (gerado automaticamente)
```

## 🛠️ Instalação

### Pré-requisitos

Certifique-se de ter instalado:

- **Python 3.13+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL** (local ou remoto com SSL)
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

### Passo a passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Lunaris-School/lunaris-dataload-script.git
   cd lunaris-dataload-script
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   DB_USER=seu_usuario
   DB_PASS=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=lunaris_db
   ```

5. **Execute a aplicação**
   ```bash
   uvicorn main:app --reload
   ```

6. **Acesse a documentação interativa**
   
   Abra seu navegador em: `http://localhost:8000/docs`

## 📜 Scripts Disponíveis

```bash
# Iniciar servidor de desenvolvimento
uvicorn main:app --reload

# Iniciar em modo produção (sem reload)
uvicorn main:app --host 0.0.0.0 --port 8000

# Instalar dependências
pip install -r requirements.txt

# Atualizar dependências
pip install --upgrade -r requirements.txt
```

## 🎯 Funcionalidades

### 📥 População de Dados
✅ Criação automática de registros de gênero  
✅ Geração de roles (ADMIN, PROFESSOR, ALUNO)  
✅ Inserção de administradores com senha criptografada  
✅ Criação de 10 disciplinas com URLs de imagens  
✅ Geração de professores vinculados a disciplinas  
✅ Criação de turmas por série e letra  
✅ Associação turma-disciplina e turma-professor  
✅ Geração de alunos com matrícula e distribuição por turma  
✅ Criação opcional de pré-cadastros (30% dos alunos)  
✅ Geração de observações pedagógicas  
✅ Criação de boletins com notas bimestrais (70% dos alunos)  
✅ Cálculo automático de médias finais  

### 🗑️ Limpeza de Banco
✅ Reset completo de todas as tabelas com CASCADE  
✅ Reinício de sequências de IDs  
✅ Preservação da estrutura do schema  

### 📊 Visualização de Dados
✅ Relatório completo de administradores  
✅ Lista de alunos com suas turmas  
✅ Professores vinculados às disciplinas  
✅ Informações de todas as turmas  
✅ Resumo estatístico (totais de alunos, boletins e notas)  

### 🔒 Segurança
✅ Hash BCrypt para todas as senhas  
✅ Compatibilidade com Spring Security BCryptPasswordEncoder  
✅ Conexão SSL/TLS ao banco PostgreSQL  
✅ Validação de variáveis de ambiente  

## 📝 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

```
Copyright (c) 2026 Lunaris-School
```

## 👥 Equipe

Desenvolvido com 💙 pela equipe **Lunaris School**
- Beatriz
- Breno
- Clara
- Giulia
- Isabela
- Maria Eduarda

## 📞 Contato

- 📧 **Email**: lunaris.school@gmail.com
- 💻 **GitHub**: [@Lunaris-School](https://github.com/Lunaris-School)

---

⭐ **Se este projeto foi útil, considere dar uma estrela no repositório!**