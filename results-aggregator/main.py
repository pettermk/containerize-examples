import duckdb
import json
import dataclasses
import argparse

from models import ProjectInfo


def get_project_info(folder: str) -> ProjectInfo:
    query_vulnerabilities = """
    CREATE TABLE vulnerabilities
        AS SELECT * FROM 'snyk.json';
    """
    
    # Execute the query to get vulnerability data and perform aggregations
    in_memory = duckdb.connect()
    in_memory.execute(query_vulnerabilities)
    
    aggregation_query = """
    SELECT severity, COUNT(DISTINCT id) AS issue_count
    FROM memory.vulnerabilities
    GROUP BY severity;
    """
    aggregated_result = in_memory.execute(aggregation_query).fetchall()
    
    project_info: ProjectInfo = ProjectInfo()
    for row in aggregated_result:
        setattr(project_info, row[0], row[1])

    # Get docker image size
    with open('image.json') as f:
        image = json.load(f)
    project_info.size = image[0]['Size']
    project_info.name = image[0]['RepoTags'][0].split(':')[0]
    history = []
    with open(f'../{folder}/Dockerfile') as f:
        history = f.readlines()
    try:
        # Get the line containing FROM in the docker build history, and parse out the base image
        base_image_event = next(h for h in reversed(history) if "FROM" in h)
        print(base_image_event)
        base_image = base_image_event.split(" ")[1]
        project_info.base_image = base_image.strip()
    except Exception as e:
        print(f'Error, {str(e)}')
    
    # Close the connection after queries
    in_memory.close()
    return project_info


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
    parser = argparse.ArgumentParser(description='Get project information')
    parser.add_argument('folder', help='The currently processed code folder')
    args = parser.parse_args()
    project_info: ProjectInfo = get_project_info(args.folder)
    print(project_info)
    add_project_to_db(project_info)

