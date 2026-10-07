"""Approved professional content, independent of rendering and file access."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    title: tuple[str, ...]
    subtitle: str
    period: str
    description: str
    outcomes: tuple[tuple[str, str], ...]
    bullets: tuple[str, ...]
    tags: tuple[str, ...]
    color: str


PROJECTS = (
    Project(
        title=("Hydraulic engineering", "platform"),
        subtitle="Engineering, sales & ERP workflows",
        period="Middle Full-stack · 2025–2026",
        description="Owned delivery from hydraulic calculations to quotation workflows.",
        outcomes=(("40–50", "platform users"), ("< 1 week", "lead to quotation")),
        bullets=(
            "Design updates: 10+ min to under 1 min.",
            "CPU/RAM usage: ~80% to ≤20% across 25 stress tests.",
            "Connected CRM, BOQ, inventory & quotations; corrections fell to ~1 in 10.",
        ),
        tags=("Python", "PostgreSQL", "ERP integration"),
        color="blue",
    ),
    Project(
        title=("Whole-slide image", "delivery"),
        subtitle="Browser viewing & NAS synchronization",
        period="Middle Full-stack · 2025–2026",
        description="Built browser viewing and background sync for around 400 SVS files.",
        outcomes=(("300–500 ms", "tile response"), ("< 50 MB", "transferred per test session")),
        bullets=(
            "Viewed 5–15 GB files without full downloads.",
            "OpenSlide tiles served through Nginx caching.",
            "Synced ~400 NAS files in 10–15 min through a PostgreSQL queue.",
        ),
        tags=("OpenSlide", "Nginx", "Background queues"),
        color="teal",
    ),
    Project(
        title=("HR analytics &", "system integrations"),
        subtitle="Contract monitoring & operational controls",
        period="Junior Full-stack · 2023–2025",
        description="Built employee monitoring and REST integrations across internal systems.",
        outcomes=(("~200", "employees supported"), ("Minutes", "document availability")),
        bullets=(
            "Contract reminders: no late detection observed in the next monitoring period.",
            "Validated working hours and timesheet overlaps.",
            "REST synchronization cut document delays from 3–5 days to minutes.",
        ),
        tags=("REST APIs", "HR analytics", "Automation"),
        color="lavender",
    ),
)


@dataclass(frozen=True)
class Competency:
    title: str
    logo: str
    skills: str


COMPETENCIES = (
    Competency("Frontend", "react", "JavaScript ES6+ · TypeScript · Astro · React.js · Next.js · OWL · HTML5 · CSS3 · Tailwind CSS · Responsive Web Design"),
    Competency("Backend & APIs", "python", "Node.js · Python · REST API Development & Integration · Strapi · ORM · Service Layer Architecture · Scheduled Jobs · Background Processing"),
    Competency("Database & data", "postgresql", "PostgreSQL · SQLite · Database Schema Design · SQL Queries & Indexing · Background Queues · Data Synchronization · Tree-Based Data Processing · Large File Processing"),
    Competency("Architecture & performance", "typescript", "Client-Server · Component-Based · Modular Architecture · Lazy Loading · Caching · Asynchronous Processing · Performance Optimization · Core Web Vitals Optimization"),
    Competency("Infrastructure & builds", "docker", "Docker · Nginx · Linux · VPS Deployment · Vercel · Vite · npm · pnpm"),
    Competency("Development tools", "git", "Git · GitHub · GitLab · Odoo · OpenSlide · QWeb · XLSX & ODT Reporting"),
)
