# System Requirements — {{PROJECT_NAME}}

## Functional Requirements

### {{Module/Feature Area 1}}

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | {{requirement description}} | Must | |
| FR-002 | {{requirement description}} | Should | |
| FR-003 | {{requirement description}} | Could | |

### {{Module/Feature Area 2}}

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-010 | {{requirement description}} | Must | |

## Non-Functional Requirements

### Performance

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-P01 | Page load time | < {{X}} ms | > ⚠️ TODO: confirm target NFR |
| NFR-P02 | API response time (p95) | < {{X}} ms | > ⚠️ TODO: confirm target NFR |

### Security

| ID | Requirement | Notes |
|----|-------------|-------|
| NFR-S01 | {{e.g., Authentication via OAuth 2.0 / JWT}} | |
| NFR-S02 | {{e.g., All data encrypted at rest and in transit}} | |
| NFR-S03 | {{e.g., OWASP Top 10 compliance}} | |

### Availability & Scalability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-A01 | Uptime SLA | {{e.g., 99.9%}} |
| NFR-A02 | Concurrent users | {{e.g., 100}} |
| NFR-A03 | Data retention | {{e.g., 12 months}} |

> ⚠️ TODO: confirm target NFR values — do not fabricate performance figures.

## Constraints & Assumptions

### Constraints
- {{e.g., Must run on existing cloud infrastructure (AWS)}}
- {{e.g., Budget limited to free-tier services for MVP}}

### Assumptions
- {{e.g., Users have modern browsers (last 2 major versions)}}
- {{e.g., Internet connectivity is always available}}

## User Roles & Permissions

| Role | Access Level | Key Permissions |
|------|-------------|-----------------|
| {{Admin}} | Full | {{CRUD all resources, manage users}} |
| {{User}} | Standard | {{CRUD own resources, view shared}} |
| {{Guest}} | Read-only | {{View public resources only}} |
