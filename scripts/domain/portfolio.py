"""Approved professional content, independent of rendering and file access."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    title: tuple[str, ...]
    subtitle: str
    period: str
    description: str
    outcomes: tuple[tuple[str, str], ...]
    story: tuple[tuple[str, str], ...]
    tags: tuple[str, ...]
    color: str


PROJECTS = (
    Project(
        title=("From hydraulic design", "to a ready-to-send quotation."),
        subtitle="Hydraulic engineering platform",
        period="Middle Full-stack · 2025–Present",
        description="A calculation change used to take more than ten minutes, and turning a lead into a quotation took about two weeks. I owned delivery of a platform that brings engineering calculations and commercial workflows together.",
        outcomes=(("40–50", "platform users"), ("< 1 week", "lead to quotation · previously ~2 weeks")),
        story=(
            ("Keep editing responsive.", "I separated interactive work from heavy calculations using server-side services, lazy loading, and tree-based processing. Design updates now complete in under a minute."),
            ("Connect the whole workflow.", "CRM, calculations, BOQ, stock, margins, quotations, and project management share connected data models. Corrections fell from nearly every quotation to about one in ten."),
            ("Validate under load.", "Across 25 stress tests, CPU/RAM usage fell from ~80% to ≤20%, and failures from 16 to ~2–5. Stress-test duration fell from 60+ minutes to at most 30 minutes."),
            ("Check calculation accuracy.", "Results showed ~2% deviation across nearly 30 stack scenarios, enabling an internal replacement for Keidel DrainStar. The platform supports around 20 leads and 200 stack calculations each month."),
        ),
        tags=("Python", "PostgreSQL", "ERP integration"),
        color="blue",
    ),
    Project(
        title=("Gigabyte-scale images.", "Browser-scale interaction."),
        subtitle="Whole-slide images & NAS synchronization",
        period="Middle Full-stack · 2025–Present",
        description="For around 400 SVS files, each 5–15 GB, downloading the source was impractical. I built tiled browser delivery with OpenSlide and Nginx caching so sessions transfer only the image data they need.",
        outcomes=(("300–500 ms", "tile response"), ("< 50 MB", "transferred per test session")),
        story=(("Keep administration responsive.", "A PostgreSQL-backed queue synchronizes around 400 NAS files in 10–15 minutes without blocking the administration interface."),),
        tags=("OpenSlide", "Nginx", "Background queues"),
        color="teal",
    ),
    Project(
        title=("Make operational gaps", "visible—and actionable."),
        subtitle="HR analytics & internal integrations",
        period="Junior Full-stack · 2023–2025",
        description="I built contract visibility and automated reminders for around 200 employees. No late contract detection was observed in the following monitoring period, compared with 6–7 of 10 previously.",
        outcomes=(),
        story=(
            ("Close the validation gap.", "Working-hour and overlap checks addressed excessive or overlapping entries previously found in ~7–8 of 10 timesheets."),
            ("Make records available sooner.", "REST integrations made tender, vendor, and legal documents available in minutes instead of 3–5 days, supporting up to around 15 processes per month."),
            ("Deliver across business domains.", "I maintained modules across HR, projects, tender, HSE, and e-learning, collaborating with analysts, domain experts, and UI/UX teams."),
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
