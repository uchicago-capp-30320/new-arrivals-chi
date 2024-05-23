# Architecture Decisions

This document summarizes key architecture decisions in New Arrivals Chi.

## Client-Server Architecture
- **Decision**: The project follows a standard client-server network model.
- **Reason**: This model is sufficient to handle client requests through the web browser, ensuring scalability and centralized resource management. It supports multiple users and can easily scale if necessary.
- **Alternatives Considered**: N/A
- **Impacts**: 
  - **Pros**: Centralized resources and control, scalability.
  - **Cons**: Single points of failure, compatibility issues across client versions.

## Monolithic Architecture
- **Decision**: The project uses a monolithic architecture.
- **Reason**: Monolithic architecture is simpler than a microservice architecture, especially given the project's current use cases and traffic expectations. It ensures easy maintenance and scalability for the foreseeable future.
- **Alternatives Considered**: Microservices.
- **Impacts**: 
  - **Pros**: Simplicity, straightforward maintenance.
  - **Cons**: Potential difficulties in scaling out in the future.

## Single Server Deployment
- **Decision**: The project will start with a single server.
- **Reason**: Current traffic patterns do not anticipate high load levels. However, horizontal scaling plans are in place to accommodate uncertain traffic patterns and ensure high availability during peak times.
- **Alternatives Considered**: Multi-server deployment.
- **Impacts**: 
  - **Pros**: Cost-effective, easier initial setup.
  - **Cons**: Potential single point of failure, limited immediate scalability.

## Relational PostgreSQL Database
- **Decision**: The project will use a relational PostgreSQL database.
- **Reason**: The application requires interacting relationships and structured data, which PostgreSQL handles effectively. Simple look-ups and updates will be the primary operations, with no anticipation of complex queries.
- **Alternatives Considered**: Non-relational database.
- **Impacts**: 
  - **Pros**: Structured data management, effective handling of relationships and queries.
  - **Cons**: May not cover all unique services provided by organizations, potential limitation in flexibility compared to non-relational databases.
