import {
  AlertTriangle,
  CalendarDays,
  CheckCircle2,
  Clock3,
  FileText,
  FolderKanban,
  LayoutDashboard,
  ListChecks,
  Users,
} from "lucide-react";

export const navigationItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/projects", label: "Projects", icon: FolderKanban },
  { href: "/tickets", label: "Tickets", icon: ListChecks },
  { href: "/time-tracking", label: "Time Tracking", icon: Clock3 },
  { href: "/documents", label: "Documents", icon: FileText },
];

export const dashboardStats = [
  { label: "Today's Appointments", value: "14", trend: "+3 vs yesterday", icon: CalendarDays },
  { label: "Open Tickets", value: "7", trend: "2 urgent", icon: AlertTriangle },
  { label: "Hours Logged", value: "8.5h", trend: "71% billable", icon: Clock3 },
  { label: "Active Patients", value: "23", trend: "+5 this week", icon: Users },
];

export const activeProjects = [
  {
    name: "Clinic Intake Modernization",
    key: "CIM",
    status: "On track",
    progress: 68,
    owner: "Dr. Selam",
    due: "Jul 12",
    tickets: 18,
  },
  {
    name: "Radiology Document Flow",
    key: "RDF",
    status: "Needs review",
    progress: 42,
    owner: "Nurse Hana",
    due: "Jul 18",
    tickets: 11,
  },
  {
    name: "AfterQuery Silver Prep",
    key: "AQS",
    status: "Focused",
    progress: 54,
    owner: "Selam",
    due: "Jul 04",
    tickets: 24,
  },
];

export const ticketColumns = [
  {
    title: "Backlog",
    count: 3,
    tickets: [
      { id: "MS-108", title: "Add attachment quota validation", priority: "High", assignee: "Selam" },
      { id: "MS-112", title: "Document workspace invitation flow", priority: "Medium", assignee: "Hana" },
      { id: "MS-119", title: "Create audit log filters", priority: "Low", assignee: "Abel" },
    ],
  },
  {
    title: "In Progress",
    count: 2,
    tickets: [
      { id: "MS-124", title: "Wire dashboard to project metrics", priority: "High", assignee: "Selam" },
      { id: "MS-127", title: "Improve file upload response payload", priority: "Medium", assignee: "Marta" },
    ],
  },
  {
    title: "Review",
    count: 2,
    tickets: [
      { id: "MS-130", title: "Time summary acceptance tests", priority: "High", assignee: "Selam" },
      { id: "MS-131", title: "Fix broken frontend icon encoding", priority: "Medium", assignee: "Hana" },
    ],
  },
  {
    title: "Done",
    count: 4,
    tickets: [
      { id: "MS-101", title: "JWT login and register flow", priority: "High", assignee: "Selam" },
      { id: "MS-104", title: "Ticket labels and assignees", priority: "Medium", assignee: "Abel" },
    ],
  },
];

export const recentActivity = [
  { label: "Attachment upload API hardened", time: "09:20", icon: CheckCircle2 },
  { label: "Time tracking weekly summary reviewed", time: "10:05", icon: Clock3 },
  { label: "Silver roadmap progress checked", time: "10:40", icon: FileText },
];

export const documents = [
  { name: "Patient Records", files: 42, size: "2.3 GB", type: "Clinical" },
  { name: "X-Ray Images", files: 18, size: "870 MB", type: "Imaging" },
  { name: "Prescriptions", files: 31, size: "126 MB", type: "Pharmacy" },
  { name: "AfterQuery Evidence", files: 9, size: "44 MB", type: "Review" },
];

export const timeEntries = [
  { ticket: "MS-124", task: "Dashboard metrics polish", duration: "2h 10m", status: "Submitted" },
  { ticket: "MS-130", task: "Weekly summary tests", duration: "1h 35m", status: "Draft" },
  { ticket: "MS-127", task: "Attachment response review", duration: "55m", status: "Approved" },
];
