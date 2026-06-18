"""Application constants."""

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# User Roles
ADMIN_ROLE = "admin"
DOCTOR_ROLE = "doctor"
NURSE_ROLE = "nurse"
RECEPTIONIST_ROLE = "receptionist"
PATIENT_ROLE = "patient"

# Member Roles
OWNER_ROLE = "owner"
ADMIN_ROLE = "admin"
MEMBER_ROLE = "member"
VIEWER_ROLE = "viewer"

# Board Types
KANBAN_TYPE = "kanban"
SCRUM_TYPE = "scrum"

# Sprint Statuses
SPRINT_PLANNING = "planning"
SPRINT_ACTIVE = "active"
SPRINT_COMPLETED = "completed"

# Visibility
PUBLIC_VISIBILITY = "public"
PRIVATE_VISIBILITY = "private"

# Timezones
DEFAULT_TIMEZONE = "UTC"

# Token Expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# File Upload
MAX_FILE_SIZE_MB = 10
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
AVATAR_MAX_SIZE = 256  # pixels

# Ticket related constants
TICKET_PRIORITY_CHOICES = ["low", "medium", "high", "critical"]
TICKET_STATUS_CHOICES = ["todo", "in_progress", "review", "done"]

# Board & Sprint constants (if not already there)
BOARD_TYPES = ["kanban", "scrum"]
SPRINT_STATUSES = ["planning", "active", "completed"]

# Time Tracking Constants
TIME_ENTRY_STATUSES = ["running", "logged", "submitted", "approved", "rejected"]
TIME_ENTRY_MAX_DURATION_HOURS = 24
BILLABLE_DEFAULT = True
