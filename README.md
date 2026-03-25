# Plataforma de Inteligência de Frotas e Manutenção Preditiva 2.0

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## Visão Geral e Impacto de Negócio
Esta é a versão 2.0 da plataforma *End-to-End* de gestão de frotas e telemetria. Evoluímos de uma arquitetura síncrona local para um **sistema distribuído e assíncrono**.

O objetivo técnico é processar grandes volumes de dados de telemetria e alertas de Segurança no Trabalho (SST) sem bloquear a API principal, garantindo alta disponibilidade. Do ponto de vista de negócio, esta lógica preditiva esteve na base da poupança de **R$ 1,56 milhão (redução de 27,7%)** nos custos anuais de manutenção de uma frota de 112 veículos.

## Arquitetura da Solução (Data Pipeline)

O fluxo de dados utiliza mensageria para desacoplar a ingestão do processamento, garantindo escalabilidade.

```mermaid
graph LR
    A((Sensores / Usuário)) -->|JSON Payload| B(FastAPI Backend)
    B -->|Publish| C{RabbitMQ Queue}
    C -->|Consume| D(Worker Process)
    D -->|Gravação ORM| E[(PostgreSQL)]
    E -->|Consultas Analíticas| F(Streamlit Dashboard)
    
    style A fill:#46E3B7,stroke:#fff,stroke-width:2px,color:#000
    style B fill:#005571,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#FF6600,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#005571,stroke:#fff,stroke-width:2px,color:#fff
    style E fill:#316192,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#FF4B4B,stroke:#fff,stroke-width:2px,color:#fff
