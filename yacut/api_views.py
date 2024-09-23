import re
import random
import string
from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from yacut.models import URLMap


MAX_LEN_SHORT = '{1,6}'
MAX_LEN_ORIDINAL = '{1,16}'
SYMVOLS = string.ascii_letters + string.digits


def get_unique_short_id():
    return ''.join(random.choices(SYMVOLS, k=6))


@app.route('/api/id/', methods=['POST'])
def creat_short_href():
    if not request.get_json(silent=True):
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    hrefs = URLMap()
    hrefs.original = data['url']
    if 'custom_id' not in data or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')
    if not re.match(
        # r'^[\w]{}$'.format(MAX_LEN_ORIDINAL, MAX_LEN_SHORT),
        r'^[\w]{}$'.format(MAX_LEN_ORIDINAL),
        data['custom_id']
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    for test in list(data['custom_id']):
        if test not in list(SYMVOLS):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        continue
    hrefs.short = data['custom_id']
    db.session.add(hrefs)
    db.session.commit()
    dict_url = {
        'url': hrefs.original,
        'short_link': f'http://localhost/{hrefs.short}'
    }
    return jsonify(dict_url), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def update_opinion(short_id):
    hrefs = URLMap.query.filter_by(short=short_id).first()
    if hrefs is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(
        {'url': hrefs.original}
    ), 200
