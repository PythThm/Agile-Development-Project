from flask_uploads import UploadSet, IMAGES, configure_uploads

# image upload 
# reference: https://pypi.org/project/Flask-Reuploaded/

photos = UploadSet('photos', IMAGES)

def configure_uploads_app(app):
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/productpics'
    configure_uploads(app, photos)

