# Employee RESTful API

![python 3.9.7](https://img.shields.io/badge/python-3.9.7-blue.svg)
![django 2.2.24](https://img.shields.io/badge/django-2.2.24-blue.svg)

## Overview
An RESTful API with methods required as below
- POST: create user
- GET: get user info
- PUT: update user info
- DELETE: delete user

## json data structure example as below
```json
{
    "email": "xxxx@smartclouds.com",
    "mobile": "0972088292",
    "position": {
        "department": "Development",
        "title": "09xx-xxx-xxx"
    }
}
```

## Packages
- [pyproject](./pyproject.toml)

## Documents
- [Environment Variable](./docs/environment-variable.md)
- [Deployment](./docs/deployment.md)
