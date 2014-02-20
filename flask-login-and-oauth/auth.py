from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer

from settings import SECRET_KEY

login_serializer = URLSafeTimedSerializer(SECRET_KEY)
