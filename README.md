# data.lab() — Ambiente de Desenvolvimento Docker

[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Lab%20%2F%20Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.style=for-the-badge)](LICENSE)

Ambiente Docker padronizado do **data.lab() (Laboratório de Análise de Dados)** configurado para o desenvolvimento acelerado de projetos de Ciência de Dados, Análise de Dados e Machine Learning. 

O repositório disponibiliza contêineres prontos com **Python**, **Jupyter Lab** e as principais bibliotecas científicas pré-instaladas, garantindo reprodutibilidade e eliminando o problema de *"funciona na minha máquina"*.

---

## 📌 Índice
- [Pré-requisitos](#-pré-requisitos)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Usar](#-como-usar)
- [Dependências Pré-instaladas](#-dependências-pré-instaladas)
- [Como Contribuir](#-como-contribuir)
- [Autores e Contato](#-autores-e-contato)
- [Licença](#-licença)

---

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

* [Git](https://git-scm.com/)
* [Docker](https://docs.docker.com/get-docker/) (versão 20.10 ou superior)
* [Docker Compose](https://docs.docker.com/compose/install/) (versão v2.0+ ou plugin integrado ao Docker Desktop)

---

## 📁 Estrutura do Repositório

```text
env-docker/
├── .github/              # Automações e workflows CI/CD
├── notebooks/            # Diretório montado para notebooks Jupyter
├── src/                  # Código-fonte e scripts auxiliares
├── Dockerfile            # Definição do contêiner e dependências
├── docker-compose.yml    # Gerenciamento dos serviços e volumes
├── requirements.txt      # Pacotes Python pré-instalados
└── README.md             # Documentação do projeto
```

---

## 🚀 Instalação e Configuração

Siga os passos abaixo para clonar o repositório e subir o ambiente localmente:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Laboratorio-de-Analise-de-Dados/env-docker.git
   cd env-docker
   ```

2. **Copie o arquivo de variáveis de ambiente (se aplicável):**
   ```bash
   cp .env.example .env
   ```

3. **Construa e inicie os contêineres Docker:**
   ```bash
   docker compose up -d --build
   ```

---

## 💻 Como Usar

### Acessando o Jupyter Lab
Após subir o contêiner, acesse o Jupyter Lab pelo navegador através da URL:
```text
http://localhost:8888
```
*(Caso haja token de acesso configurado, verifique a saída do terminal com o comando `docker compose logs -f`)*.

### Executando comandos dentro do contêiner
Para rodar scripts em Python ou utilizar o terminal interativo dentro do ambiente isolado:
```bash
docker compose exec app bash
```

### Parando o ambiente
Para encerrar os serviços sem perder os arquivos salvos nos volumes:
```bash
docker compose down
```

---

## 🧪 Dependências Pré-instaladas

O ambiente vem configurado por padrão com a pilha essencial de Ciência de Dados:

* **Manipulação e Análise de Dados:** `pandas`, `numpy`
* **Visualização:** `matplotlib`, `seaborn`, `plotly`
* **Machine Learning & Estatística:** `scikit-learn`, `scipy`, `statsmodels`
* **Ambiente de Trabalho:** `jupyterlab`, `notebook`, `ipykernel`

---

## 🤝 Como Contribuir

Contribuições são muito bem-vindas! Se você deseja adicionar um novo pacote, corrigir um bug ou melhorar a documentação:

1. Faça um **Fork** do repositório.
2. Crie uma branch para a sua feature (`git checkout -b feature/MinhaFeature`).
3. Faça o **Commit** das suas alterações (`git commit -m 'feat: adiciona biblioteca X'`).
4. Envie as alterações para a sua branch (`git push origin feature/MinhaFeature`).
5. Abra um **Pull Request**.

---

## 👥 Autores e Contato

Desenvolvido e mantido pela equipe do **Laboratório de Análise de Dados — data.lab()**.

* 🌐 **Website:** [datalab.in.net](https://datalab.in.net/)
* 📧 **E-mail:** [gfsilveira@gmail.com](mailto:gfsilveira@gmail.com)
* 🐙 **GitHub:** [@Laboratorio-de-Analise-de-Dados](https://github.com/Laboratorio-de-Analise-de-Dados)

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
