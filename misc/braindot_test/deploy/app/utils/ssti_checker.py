import re

SSTI_REGEX = re.compile(
    r"""
    ({{\s*.*?\s*}})         |  # Jinja2 expression
    ({%\s*.*?\s*%})         |  # Jinja2 block
    (\[\s*['"]?.*?['"]?\s*\]) |  # Index access
    (__\w+__)               |  # Dunder names like __class__, __globals__
    (\bimport\b|\beval\b|\bexec\b|\bos\b|\bsys\b|\bopen\b|\bsubprocess\b)  # Dangerous keywords
    """,
    re.VERBOSE | re.IGNORECASE
)

def is_safe_input(user_input: str) -> bool:
    return not SSTI_REGEX.search(user_input)