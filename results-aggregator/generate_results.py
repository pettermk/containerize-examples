from typing import List

from jinja2 import Template
import duckdb

from models import ProjectInfo


def get_results() -> List[ProjectInfo]:
    conn = duckdb.connect('duckdb')

    query = f"""
    SELECT * FROM projects;
    """

    conn.execute(query)
    aggregated_result = conn.execute(query).fetchall()
    print([(row, len(row)) for row in aggregated_result])
    return [ProjectInfo(*row) for row in aggregated_result]


if __name__ == "__main__":
    projects = get_results()

    template = Template("""
| Project     | Low | Medium | High | Critical | Size (MB) |
|-------------|-----|--------|------|----------|-----------|
{% for p in projects -%}
| {{ p.name or "N/A" }} | {{ p.low }} | {{ p.medium }} | {{ p.high }} | {{ p.critical }} | {{ '%.2f' % p.size_mb() }} |
{% endfor %}
    """)
    
    output = template.render(projects=projects)
    print(output)


