# API Usage

#### /api/users/
```
GET /api/users/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "email": "first_user@example.com"},
  {"id": 2, "email": "second_user@example.com"},
  {"id": 3, "email": "third_user@example.com"} ]
```

#### /api/users/?search={query}
```
GET /api/users/?search={query}
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "email": "first_user_with_query@example.com"},
  {"id": 2, "email": "second_user_with_query@example.com"} ]
```

#### /api/projects/
```
GET /api/projects/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "name": "first_project"},
  {"id": 2, "name": "second_project"},
  {"id": 3, "name": "third_project"} ]
```

#### /api/projects/?search={query}
```
GET /api/projects/?search={query}
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "name": "first_project_with_query"},
  {"id": 2, "name": "second_project_with_query"} ]
```

#### /api/teams/
```
GET /api/teams/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "name": "first_team"},
  {"id": 2, "name": "second_team"},
  {"id": 3, "name": "third_team"} ]
```

#### /api/teams/?search={query}
```
GET /api/teams/?search={query}
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "name": "first_team_with_query"},
  {"id": 2, "name": "second_team_with_query"} ]
```

#### /api/teams/TEAM_NAME/
```
GET /api/teams/<teamname>/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

{"id": <teamid>, "name": "<teamname>"}
```

```
GET /api/teams/<invalid_teamname>/
```
```
HTTP/1.0 404 OK
Content-Type: application/json

{"detail": "Not found"}
```

#### /api/teams/TEAM_NAME/users/
```
GET /api/teams/<teamname>/users/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "email": "first_user_in_team@example.com"},
  {"id": 2, "email": "second_user_in_team@example.com"},
  {"id": 3, "email": "third_user_in_team@example.com"} ]
```

```
GET /api/teams/<teamname_with_no_user>/users/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[]
```

```
GET /api/teams/<invalid_teamname>/users/
```
```
HTTP/1.0 404 OK
Content-Type: application/json

{"detail": "Not found"}
```

#### /api/teams/TEAM_NAME/users/?search={query}
```
GET /api/teams/<teamname>/users/?search={query}
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "email": "first_user_with_query_in_team@example.com"},
  {"id": 2, "email": "second_user_with_query_in_team@example.com"} ]
```

#### /api/teams/TEAM_NAME/projects/
```
GET /api/teams/<teamname>/projects/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[ {"id": 1, "name": "first_project_in_team"},
  {"id": 2, "name": "second_project_in_team"},
  {"id": 3, "name": "third_project_in_team"} ]
```

```
GET /api/teams/<teamname_with_no_project>/projects/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

[]
```

```
GET /api/teams/<invalid_teamname>/projects/
```
```
HTTP/1.0 404 OK
Content-Type: application/json

{"detail": "Not found"}
```
