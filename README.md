# Trabalho Prático - Teste de Software: GoodPlays

## 1 - Membros do grupo:
- Giovanni Russo Paschoal
- João Victor Evangelista Cruz
- Luiza Sodre Salgado
- Victor Gabriel Moura Oliveira

## 2 - Explicação do sistema:
  O GoodPlays será um sistema de avaliação, compartilhamento de progresso e experiências de jogos digitais, na qual será possível simular ações como publicação de jogos, pesquisa de jogos disponíveis, criar avaliações de jogos, definir seu progresso em um jogo, entre outros.

## 3 - Possíveis tecnologias utilizadas:
  Faremos o projeto usando a linguagem Python e o Sqlite para banco de dados, FastAPI como framework para o backend.

## 4 - Como executar:
  Crie uma máquina virtual
  ```bash
  python -m venv venv 
  source venv/bin/activate
  ```

  Instale os requerimentos
  ```bash
  pip install -r requirements.txt
  ```

  Rode o servidor se quiser:
  ```bash
  uvicorn app.main:app --reload
  ```
  Com o servidor rodando, abra o seu navegador e acesse a documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI: 👉 http://127.0.0.1:8000/docs

  Para rodar os testes:
  ```bash
  python -m pytest --cov=app --cov-report=term-missing
  ```


