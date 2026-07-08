# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-08

### Added

- LangChain-based Retrieval-Augmented Generation application with a FastAPI
  service exposing `/health`, `/ready`, `/chat`, `/query`, and `/ingest`.
- RAG chain assembly, vector-store-backed retriever, embedding/vector store
  provider abstractions, and windowed conversational memory.
- `RagChatService` orchestrating the chain and per-session memory, plus
  pydantic request/response models.
- Terraform infrastructure under `terraform/` (ECR repository, CloudWatch log
  group, security group, and a reusable `vector-store` module) with per-env
  configuration.
- Multi-stage Dockerfile, documentation, CI pipeline, pre-commit hooks,
  issue/PR templates, CODEOWNERS, and Dependabot configuration.
