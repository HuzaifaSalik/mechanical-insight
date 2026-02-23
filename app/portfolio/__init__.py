from flask import Blueprint

portfolio = Blueprint('portfolio', __name__, url_prefix='/portfolio')

from app.portfolio import routes
