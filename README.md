# DevFlow Pro

**Project Management & Collaboration Platform** - A comprehensive Kanban and Scrum-based project management system with advanced features.

## Features

- **User Authentication & Authorization** - JWT-based auth with refresh tokens, role-based access control, OAuth (Google/GitHub)
- **Workspace & Project Management** - Multi-tenant workspaces with projects and boards
- **Kanban Boards** - Drag-and-drop ticket management with columns
- **Scrum Sprints** - Sprint planning, tracking, and velocity metrics
- **Ticket Management** - Full CRUD, assignees, labels, comments, dependencies
- **Time Tracking** - Timer-based and manual time entry with approval workflow
- **File Attachments** - File upload and management with MinIO
- **Search & Filtering** - Full-text search with advanced filtering and sorting
- **Team Management** - Team member management with role assignments
- **Permissions System** - Granular role-based permissions configuration
- **Analytics Dashboard** - Metrics, charts, and activity tracking
- **Reports Generation** - Export reports in PDF, CSV, and Excel formats
- **Real-time Updates** - WebSocket support for live updates
- **Notifications** - In-app notification system
- **AI Assistant** - OpenAI integration for ticket summarization and PR descriptions
- **Billing & Subscriptions** - Stripe integration for subscription management
- **Admin Panel** - Audit logs, feature flags, and detailed health checks
- **Public API v2** - OAuth client credentials grant with camelCase schemas
- **Webhooks** - HMAC-signed webhook delivery with exponential backoff retry

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL with async SQLAlchemy
- **Cache**: Redis for caching and session management
- **Storage**: MinIO for file storage
- **Authentication**: JWT with refresh tokens, OAuth (Google/GitHub)
- **Real-time**: WebSocket support
- **Testing**: Pytest with async support
- **Container**: Docker Compose
- **AI**: OpenAI API
- **Payments**: Stripe
- **Security**: Bleach for HTML sanitization, security headers middleware

## Project Structure

```
medisync-pro/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── v1/         # v1 API endpoints
│   │   │   └── v2/         # v2 API endpoints (camelCase, OAuth)
│   │   ├── core/           # Core utilities (database, security, etc.)
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic (AI, billing, webhooks)
│   │   └── websocket/      # WebSocket handlers
│   ├── tests/              # Integration tests
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js app router pages
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   └── lib/            # Utilities and API client
│   └── package.json
└── docker-compose.yml      # Development environment
```

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/selam-feyisa/medisync-pro.git
cd medisync-pro

# 2. Set up environment variables
cp backend/.env.example backend/.env
# Edit .env with your configuration

# 3. Start services with Docker Compose
docker-compose up -d

# 4. Run database migrations (if needed)
cd backend
python -m alembic upgrade head

# 5. Seed demo data
python -m app.seed

# 6. Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. Start the frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with auto-reload
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

### Database & Cache
- `DATABASE_URL`: PostgreSQL connection string (default: `sqlite+aiosqlite:///./medisync.db`)
- `REDIS_URL`: Redis connection string (default: `redis://localhost:6379`)

### Security
- `SECRET_KEY`: FastAPI secret key (default: `development-secret-key`)
- `ENCRYPTION_KEY`: Encryption key for sensitive data (default: `development-encryption-key`)
- `ALGORITHM`: JWT algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration (default: `15`)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration (default: `7`)

### OAuth
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret
- `GITHUB_CLIENT_ID`: GitHub OAuth client ID
- `GITHUB_CLIENT_SECRET`: GitHub OAuth client secret

### AI
- `OPENAI_API_KEY`: OpenAI API key for AI features

### Billing
- `STRIPE_SECRET_KEY`: Stripe secret key for payments
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook secret for verification

### Storage
- `MINIO_URL`: MinIO endpoint (default: `localhost:9000`)
- `MINIO_ACCESS_KEY`: MinIO access key (default: `minioadmin`)
- `MINIO_SECRET_KEY`: MinIO secret key (default: `minioadmin`)
- `MINIO_BUCKET_NAME`: MinIO bucket name (default: `medisync`)

### Email (Optional)
- `SMTP_HOST`: SMTP server host
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `SMTP_TLS`: Use TLS (default: `False`)
- `SMTP_FROM`: From email address

### Frontend
- `FRONTEND_URL`: Frontend URL for OAuth callbacks (default: `http://localhost:3000`)

## Roadmap Completion

**All 25 days of the development roadmap have been completed:**

- ✅ Days 1-5: Foundation, Authentication, User Management
- ✅ Days 6-7: Workspaces, Projects, Boards, Sprints
- ✅ Days 8-9: Ticket Management, Search, Time Tracking
- ✅ Days 10-12: File Attachments, Notifications, Comments
- ✅ Days 13-15: Integration Tests, Caching, Rate Limiting
- ✅ Days 16-18: Frontend Layout, Components, API Integration
- ✅ Days 19-20: Drag & Drop, WebSocket, File Upload UI, Time Tracking UI
- ✅ Days 21-22: User Profile, Settings, Search, Filtering & Sorting
- ✅ Days 23-24: Team Management, Permissions, Analytics, Reports
- ✅ Day 25: Testing, Bug Fixes, Documentation

**Additional Features Implemented:**
- ✅ OAuth Authentication (Google/GitHub)
- ✅ Healthcare Role Standardization
- ✅ AI Assistant Module (OpenAI Integration)
- ✅ Billing & Subscriptions (Stripe Integration)
- ✅ Admin Panel (Audit Logs, Feature Flags, Health Checks)
- ✅ Public API v2 (OAuth Client Credentials, camelCase schemas)
- ✅ Webhooks (HMAC signing, exponential backoff retry)
- ✅ Security Hardening (Security headers, HTML sanitization)

## Testing

Integration tests are included for:
- Tickets CRUD operations
- Sprint management
- Notifications

Run tests with:
```bash
cd backend
pytest tests/ -v -o asyncio_mode=auto
```

Run code coverage:
```bash
pytest --cov=app --cov-report=html
```

## Deployment

### Production Deployment

1. Set environment variables for production
2. Build Docker images
3. Deploy to your preferred hosting platform
4. Configure PostgreSQL, Redis, and MinIO
5. Run database migrations
6. Start services

### Security Considerations

- All user-generated content is sanitized using Bleach
- Security headers are applied via middleware
- JWT tokens are used for authentication
- OAuth 2.0 client credentials grant for API v2
- HMAC SHA256 signing for webhooks
- Role-based access control (RBAC) with healthcare roles

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.