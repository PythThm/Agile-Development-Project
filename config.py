from flask_uploads import UploadSet, IMAGES, configure_uploads
from itsdangerous import URLSafeTimedSerializer

# image upload 
# reference: https://pypi.org/project/Flask-Reuploaded/

photos = UploadSet('photos', IMAGES)

def configure_uploads_app(app):
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/productpics'
    configure_uploads(app, photos)


# generate email token

def generate_token(email):
    serializer = URLSafeTimedSerializer('sefesfseffs')
    return serializer.dumps(email, salt='sffwaeawef')


# confirm email token

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('sefesfseffs')
    try:
        email = serializer.loads(token, salt='sffwaeawef', max_age=expiration)
        return email
    except Exception:
        return False