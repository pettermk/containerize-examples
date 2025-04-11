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

    template = None
    with open('../README.md.jinja2') as f:
        template = Template(f.read())
    output = template.render(projects=projects)
    with open('../README.md', "w") as fh:
        fh.write(output)


