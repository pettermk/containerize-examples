# Containerization examples
This project demonstrates different way of containerizing applications. The main focus 
is on how to get lightweight and secure image. It demonstrates both good and bad examples, and
the table below illustrates how the choice of base image and technical stack affects the size 
of there resulting image and its security posture in terms of vulnerabilities.

| Project     | Base image | Low | Medium | High | Critical | Size (MB) |
|-------------|------------|-----|--------|------|----------|-----------|
| python-pip-api | ubi9-micro-9-5 | 9 | 3 | 0 | 0 | 187.86 |
| python-poetry-api | ubi9-micro-9-5 | 9 | 3 | 0 | 0 | 299.62 |
| dotnetcore-api | None | 154 | 0 | 0 | 5 | 236.80 |
