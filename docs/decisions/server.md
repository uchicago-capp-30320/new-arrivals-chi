# Server Decisions

This document summarizes key server decisions in New Arrivals Chi.

## Server Configuration
- **Decision**: The project will operate with a single EC2 server.
- **Reason**: The expected traffic and workload do not require multiple servers or load balancing, which simplifies infrastructure and reduces costs.
- **Alternatives Considered**: Multiple servers with load balancing.
- **Impacts**: This approach minimizes unnecessary complexity.
