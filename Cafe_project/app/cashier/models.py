from app.extensions import db
from app.models import BaseModel


class AboutSetting(BaseModel):
    paragraph1 = db.Column(db.String(264), nullable=True)
    paragraph2 = db.Column(db.String(264), nullable=True)
    paragraph3 = db.Column(db.String(264), nullable=True)

    manager1 = db.Column(db.String(100), nullable=True)
    manager2 = db.Column(db.String(100), nullable=True)
    manager3 = db.Column(db.String(100), nullable=True)
    manager4 = db.Column(db.String(100), nullable=True)

    banner_url = db.Column(db.String(300), nullable=False)
