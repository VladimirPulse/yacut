from flask import abort, flash, redirect, render_template

from yacut.constans import BASE_URL
from yacut.utils import get_unique_short_id

from . import app, db
from .forms import HrefForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = HrefForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        if short == '' or short is None:
            short = get_unique_short_id()
        hrefs = URLMap(
            original=form.original_link.data,
            short=short,
        )
        url = f'{BASE_URL}/{hrefs.short}'
        db.session.add(hrefs)
        db.session.commit()
        flash('Ваша новая ссылка готова:')
        return render_template(
            'index.html',
            form=form,
            url=url,
        )
    return render_template('index.html', form=form)


@app.route('/<short_url>')
def redirect_to_original(short_url):
    href = URLMap.query.filter_by(short=short_url).first()
    if href:
        return redirect(href.original)
    else:
        abort(404)
