# Containerization examples
This project demonstrates different way of containerizing applications. The main focus 
is on how to get lightweight and secure image. It demonstrates both good and bad examples, and
the table below illustrates how the choice of base image and technical stack affects the size 
of there resulting image and its security posture in terms of vulnerabilities.

| Project     | Base image | Low | Medium | High | Critical | Size (MB) |
|-------------|------------|-----|--------|------|----------|-----------|
| python-pip-api | registry.access.redhat.com/ubi9/ubi-micro | 9 | 3 | 0 | 0 | 187.86 |
| python-poetry-api | registry.access.redhat.com/ubi9/ubi-micro | 9 | 3 | 0 | 0 | 299.62 |
| dotnetcore-api | mcr.microsoft.com/dotnet/aspnet:8.0 | 36 | 0 | 0 | 1 | 236.80 |
