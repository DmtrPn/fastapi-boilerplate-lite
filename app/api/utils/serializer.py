from itsdangerous import URLSafeSerializer
from app.config import settings


SECRET_KEY = settings.COOKIE_SECRET_KEY
COOKIE_NAME = settings.COOKIE_NAME

serializer = URLSafeSerializer(SECRET_KEY)
