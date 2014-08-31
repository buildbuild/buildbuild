API
---

# API Usage

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

```
GET /api/teams/<teamname>/
```
```
HTTP/1.0 200 OK
Content-Type: application/json

{"id": <teamid>, "name": "<teamname>"}
```

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
