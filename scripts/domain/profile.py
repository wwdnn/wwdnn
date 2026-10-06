from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    name: str
    username: str
    role: str
    frontend: str
    backend: str
    database: str
    focus: str


WILDAN = Profile(
    name="Wildan Setya Nugraha",
    username="wwdnn",
    role="Full-stack Developer",
    frontend="TypeScript · React · Next.js",
    backend="Python · Odoo ERP",
    database="PostgreSQL",
    focus="Web applications and ERP systems",
)

