# MediSync Pro 🏥

**Healthcare Appointment & Records SaaS** with built-in Project Management (Kanban + Scrum).

## Features

- **Multi-role Authentication** (Admin, Doctor, Nurse, Receptionist, Patient)
- **Workspace & Project Management** (like Jira/Linear)
- **Appointment & Medical Records** system
- **File Storage** with MinIO
- **Real-time ready** architecture

## Tech Stack

- **Backend**: FastAPI + Python
- **Database**: PostgreSQL (async)
- **Cache**: Redis
- **Storage**: MinIO
- **Auth**: JWT + Refresh tokens
- **Container**: Docker Compose

## Quick Start

```bash
# 1. Clone
git clone https://github.com/selam-feyisa/medisync-pro.git
cd medisync-pro

# 2. Copy env
cp .env.example .env
# Edit .env with your secrets

# 3. Start services
make up

# 4. Run backend
make dev
## Current Progress (Day 7 Complete)

- ✅ Foundation & Auth (Days 1-5)
- ✅ Projects, Boards, Sprints (Day 6)
- ✅ Ticket CRUD + Move + Assignees + Labels + Comments (Day 7)

**Next:** Full comment threading, bulk operations, search (Day 8)

## Available Endpoints (Current)

- `POST /api/v1/seed` → Seed demo data
- Ticket routes under `/api/v1/tickets`
## Day 8 Completed ✅

- Enhanced Comment model with threading
- Mention parsing (@username)
- Full-text search with PostgreSQL `tsvector`
- Search API: `GET /api/v1/workspaces/{workspace_id}/search?q=...`

**Total Commits Progress:** Strong momentum on Ticket + Search features.