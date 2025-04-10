import duckdb
import json
import dataclasses

from models import ProjectInfo


def get_project_info() -> ProjectInfo:
    query_vulnerabilities = """
    CREATE TABLE vulnerabilities
        AS SELECT * FROM 'snyk.json';
    """
    
    # Execute the query to get vulnerability data and perform aggregations
    in_memory = duckdb.connect()
    in_memory.execute(query_vulnerabilities)
    
    aggregation_query = """
    SELECT severity, COUNT(*) AS issue_count
    FROM memory.vulnerabilities
    GROUP BY severity;
    """
    aggregated_result = in_memory.execute(aggregation_query).fetchall()
    
    results: ProjectInfo = ProjectInfo()
    for row in aggregated_result:
        setattr(results, row[0], row[1])

    # Get docker image size
    with open('image.json') as f:
        image = json.load(f)
    results.size = image[0]['Size']
    results.name = image[0]['RepoTags'][0].split(':')[0]
    print(results)
    
    # Close the connection after queries
    in_memory.close()
    return results


def add_project_to_db(project_info: ProjectInfo):
    conn = duckdb.connect('duckdb')
    def to_sql(field, project_info) -> str:
        if type(field) == str:
            return f"'{getattr(project_info, field)}' as {field}"
        return f"{getattr(project_info, field)} as {field}"

    fields = dataclasses.fields(project_info)
    insert = ', '.join([to_sql(field.name, project_info) for field in fields])
    query = f"""
    INSERT INTO projects BY NAME (SELECT {insert})
    """

    conn.execute(query)


if __name__ == "__main__":
    project_info: ProjectInfo = get_project_info()
    add_project_to_db(project_info)


