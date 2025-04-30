from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.backends import TokenBackend
from config.settings import SECRET_KEY
import jwt

User = get_user_model()

# @database_sync_to_async
# def get_user(validated_token):
#     try:
#         user_id = int(validated_token["user_id"])
#         return User.objects.get(id=user_id)
#     except (User.DoesNotExist, TypeError) as e:
#         print("Type Error: ==============================>", e)
#         return AnonymousUser()

# class JWTAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         query_string = scope["query_string"].decode()
#         token = parse_qs(query_string).get("token", [None])[0]

#         if token is None:
#             scope["user"] = AnonymousUser()
#             return await super().__call__(scope, receive, send)

#         try:
#             token_backend = TokenBackend(algorithm='HS256', signing_key=SECRET_KEY)
#             validated_data = token_backend.decode(token, verify=True)
#             print("VALIDATED DATA: =======================> ", validated_data)

#             user = await get_user(validated_data)
#             scope["user"] = user
#             # validated_token = UntypedToken(token)
#             # print("VALIDATED TOKEN: =======================> ", validated_token.payload)
#             # user = await get_user(validated_token)
#             # scope["user"] = user
#         except (InvalidToken, TokenError, TypeError) as e:
#             print("JWT Error: ==============================>", e)
#             scope["user"] = AnonymousUser()

#         return await super().__call__(scope, receive, send)


# @database_sync_to_async
# def get_user(user_id):
#     try:
#         return User.objects.get(id=int(user_id))
#     except User.DoesNotExist:
#         return AnonymousUser()


# class JWTAuthMiddleware(BaseMiddleware):
#     """
#     Custom middleware for JWT Authentication with Django Channels
#     """
#     async def __call__(self, scope, receive, send):

#         version = scope.get("http_version")
#         if isinstance(version, str):
#             try:
#                 scope["http_version"] = float(version)
#             except ValueError:
#                 try:
#                     scope["http_version"] = int(version)
#                 except ValueError:
#                     pass

#         query_string = scope["query_string"].decode()
#         token = parse_qs(query_string).get("token", [None])[0]

#         if token is None:
#             scope["user"] = AnonymousUser()
#             return await super().__call__(scope, receive, send)

#         try:
#             # Decode the JWT token
#             # token_backend = TokenBackend(
#             #     algorithm='HS256',  # Match your SIMPLE_JWT setting
#             #     signing_key=settings.SECRET_KEY
#             # )
#             token_backend = TokenBackend(
#                 algorithm=settings.SIMPLE_JWT["ALGORITHM"],
#                 signing_key=settings.SIMPLE_JWT["SIGNING_KEY"],
#             )
#             validated_data = token_backend.decode(token, verify=True)
#             print("VALIDATED DATA:", validated_data)

#             user_id = validated_data.get(("user_id"))
#             user = await get_user(int(user_id))
#             scope["user"] = user
#         except (InvalidToken, TokenError, jwt.DecodeError, Exception) as e:
#             print("JWT Middleware Error:", str(e))
#             scope["user"] = AnonymousUser()

#         return await super().__call__(scope, receive, send)



# import jwt
# from urllib.parse import parse_qs

# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser

# from channels.middleware import BaseMiddleware
# from channels.db import database_sync_to_async

# from rest_framework_simplejwt.backends import TokenBackend
# from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# # import os
# # print("LOADED MIDDLEWARE FROM:", os.path.abspath(__file__))
# # print("SCOPE HTTP VERSION:", scope.get("http_version"))

# User = get_user_model()

# @database_sync_to_async
# def get_user(user_id):
#     try:
#         return User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return AnonymousUser()

# class JWTAuthMiddleware(BaseMiddleware):
#     """
#     1) Сразу приводим scope['http_version'] к float (или ставим дефолт 1.1),
#        чтобы Channels не падал на сравнении строк/None.
#     2) Декодим JWT через TokenBackend и записываем scope['user'].
#     """
#     async def __call__(self, scope, receive, send):
#         # --- 1) Приведение http_version к числу ---
#         ver = scope.get("http_version", "1.1")
#         try:
#             scope["http_version"] = float(ver)
#         except (ValueError, TypeError):
#             scope["http_version"] = 1.1

#         # --- 2) JWT-аутентификация ---
#         query_string = scope.get("query_string", b"").decode()
#         token = parse_qs(query_string).get("token", [None])[0]

#         if not token:
#             scope["user"] = AnonymousUser()
#             return await super().__call__(scope, receive, send)

#         try:
#             token_backend = TokenBackend(
#                 algorithm=getattr(settings, "SIMPLE_JWT", {}).get("ALGORITHM", "HS256"),
#                 signing_key=getattr(settings, "SIMPLE_JWT", {}).get("SIGNING_KEY", settings.SECRET_KEY),
#             )
#             validated = token_backend.decode(token, verify=True)
#             user_id = validated.get("user_id")
#             scope["user"] = await get_user(user_id)
#         except (InvalidToken, TokenError, jwt.DecodeError, Exception):
#             scope["user"] = AnonymousUser()

#         # --- 3) Подаём дальше в Channels ---
#         if isinstance(scope.get("http_version"), str):
#             try:
#                 scope["http_version"] = float(scope["http_version"])
#             except ValueError:
#                 scope["http_version"] = 1.1

#         return await super().__call__(scope, receive, send)


import jwt
import time
from urllib.parse import parse_qs

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware для аутентификации WebSocket через JWT.
    Также приводит http_version к float, чтобы избежать ошибок сравнений.
    """
    async def __call__(self, scope, receive, send):
        # Приводим http_version к числу
        ver = scope.get("http_version", "1.1")
        try:
            scope["http_version"] = float(ver)
        except (ValueError, TypeError):
            scope["http_version"] = 1.1

        # Получаем токен из query string
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if not token:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            token_backend = TokenBackend(
                algorithm=getattr(settings, "SIMPLE_JWT", {}).get("ALGORITHM", "HS256"),
                signing_key=getattr(settings, "SIMPLE_JWT", {}).get("SIGNING_KEY", settings.SECRET_KEY),
            )
            validated = token_backend.decode(token, verify=True)

            # ✅ Проверка exp с приведением к int
            exp = validated.get("exp")
            if exp is not None and int(exp) <= int(time.time()):
                raise InvalidToken("Token has expired")

            user_id = validated.get("user_id")
            scope["user"] = await get_user(user_id)
        except (InvalidToken, TokenError, jwt.DecodeError, Exception):
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)








# from urllib.parse import parse_qs
# from django.contrib.auth.models import AnonymousUser
# from channels.middleware import BaseMiddleware
# from channels.db import database_sync_to_async
# from rest_framework_simplejwt.tokens import UntypedToken
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework_simplejwt.backends import TokenBackend
# from django.conf import settings
# from django.contrib.auth import get_user_model

# User = get_user_model()

# @database_sync_to_async
# def get_user(validated_token):
#     try:
#         user_id = validated_token["user_id"]
#         return User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return AnonymousUser()

# class JWTAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         query_string = scope["query_string"].decode()
#         token = parse_qs(query_string).get("token", [None])[0]

#         if token is None:
#             scope["user"] = AnonymousUser()
#             return await super().__call__(scope, receive, send)

#         try:
#             validated_token = UntypedToken(token)
#             user = await get_user(validated_token)
#             scope["user"] = user
#         except (InvalidToken, TokenError):
#             scope["user"] = AnonymousUser()

#         return await super().__call__(scope, receive, send)







# from urllib.parse import parse_qs
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import AnonymousUser
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import AccessToken

# User = get_user_model()

# @database_sync_to_async
# def get_user(token):
#     try:
#         access_token = AccessToken(token)
#         return User.objects.get(id=access_token['user_id'])
#     except Exception:
#         return AnonymousUser()


# class JWTAuthMiddleware:
#     """
#     Обёртка, которая при подключении по WebSocket кладёт в scope['user']
#     пользователя из JWT-токена (параметр ?token=).
#     """
#     def __init__(self, inner):
#         self.inner = inner

#     def __call__(self, scope):
#         # Возвращаем экземпляр, у которого есть async __call__(receive, send)
#         return JWTAuthMiddlewareInstance(scope, self.inner)


# class JWTAuthMiddlewareInstance:
#     def __init__(self, scope, inner):
#         # Копируем scope, чтобы не мутировать оригинал
#         self.scope = dict(scope)
#         self.inner = inner

#     async def __call__(self, receive, send):
#         # Парсим токен из query_string
#         qs = parse_qs(self.scope.get('query_string', b'').decode())
#         token = qs.get('token', [None])[0]

#         if token:
#             self.scope['user'] = await get_user(token)
#         else:
#             self.scope['user'] = AnonymousUser()

#         # Передаём управление дальше по ASGI-конвейеру
#         return await self.inner(self.scope)(receive, send)