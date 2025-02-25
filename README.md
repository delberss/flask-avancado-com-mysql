# Jogoteca - Flask

Este é um projeto desenvolvido com Flask para gerenciamento de jogos.

## Capturas de Tela

### Página Inicial
<img src="https://github.com/user-attachments/assets/03bb04a5-90d0-4b75-b14d-8ae92eef62b9" width="500">

### Tela de Login
<img src="https://github.com/user-attachments/assets/9be79f54-95b2-49cc-a43f-440d8bfc889b" width="500">

### Tela de Novo Jogo
<img src="https://github.com/user-attachments/assets/8df66bb3-4eb6-44be-841e-62d8a15b9b73" width="500">

### Página Inicial Atualizada
<img src="https://github.com/user-attachments/assets/e418003e-bd9c-42d8-84e2-29eb98862d23" width="500">



## Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação corretamente.

### 1. Clone o repositório
Abra o terminal e execute o seguinte comando:
```bash
git clone https://github.com/delberss/flask-avancado-com-mysql
cd flask-avancado
```

### 2. Crie um ambiente virtual
Criar um ambiente virtual é recomendável para evitar conflitos de dependências:
```bash
python -m venv venv
```

Ative o ambiente virtual:
- **Windows (cmd/PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instale as dependências
Com o ambiente virtual ativado, instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

### 4. Executar o Banco de Dados
Com o Mysql instalado corretamente, execute o seguinte comando:

```bash
python prepara_banco.py
```

### 5. Execute a aplicação
Com todas as dependências instaladas e o banco configurado, execute o seguinte comando:
```bash
python jogoteca.py
```

A aplicação estará rodando em **http://127.0.0.1:5000/**

## Tecnologias Utilizadas
- Python
- Flask
- SQLite
- Bootstrap


