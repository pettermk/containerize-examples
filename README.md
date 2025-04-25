# Containerization examples
This project demonstrates different way of containerizing applications. The main focus 
is on how to get lightweight and secure image. It demonstrates both good and bad examples, and
the table below illustrates how the choice of base image and technical stack affects the size 
of there resulting image and its security posture in terms of vulnerabilities.

| Project     | Base image | Low | Medium | High | Critical | Size (MB) |
|-------------|------------|-----|--------|------|----------|-----------|
| python-pip | registry.access.redhat.com/ubi9/ubi-micro | 9 | 3 | 0 | 0 | 187.87 |
| python-pip-debian-slim | python:3.13-slim | 38 | 0 | 0 | 1 | 176.34 |
| python-pip-debian | python:3.13 | 209 | 1 | 2 | 1 | 1073.74 |
| python-poetry | registry.access.redhat.com/ubi9/ubi-micro | 9 | 3 | 0 | 0 | 299.53 |
| dotnetcore | mcr.microsoft.com/dotnet/aspnet:8.0 | 36 | 0 | 0 | 1 | 236.80 |
| dotnetcore-chiseled | mcr.microsoft.com/dotnet/aspnet:8.0-jammy-chiseled | 4 | 0 | 0 | 0 | 128.85 |
