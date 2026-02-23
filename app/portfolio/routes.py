from flask import render_template
from app.portfolio import portfolio

@portfolio.route('/')
def portfolio_list():
    return render_template('portfolio/portfolio_list.html')
