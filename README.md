# backend

## Получение токена
- POST /api/v1/auth/token
  - request {"username": "email созданного пользователя", "password": "пароль пользователя"}
  - response {"access": "токен", "refresh": "refresh токен, чтобы обновить истёкший access токен (у него срок истечения - неделя)"}
- POST /api/v1/auth/refresh-token (быть авторизованным не обязательно)
  - request {"refresh": "refresh токен, полученный в прошлом пункте"}
  - response {"access": "новый access токен"}
