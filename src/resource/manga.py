from flask import Blueprint, jsonify, request
from repository.mangas import Manga, Mangas
from service.get_chapters import get_manga_info


bp = Blueprint('mangas', __name__, url_prefix='/mangas')


def to_json(manga: list[Manga]):
    return list(map(lambda m: m.to_json(), manga))


@bp.route('/', methods=['GET'])
def getManga():
    try:
        return jsonify(to_json(Mangas().get_mangas()))
    except Exception as e:
        return {'message': f'{e}'}, 500


@bp.route('/', methods=['POST'])
def addManga():
    try:
        content = request.get_json()
        if not 'rssUrl' in content or not 'fileType' in content or not 'merge' in content:
           return {'message': 'Missing fields | [ rssUrl, fileType, merge ]'}, 400
        rssUrl = content['rssUrl']
        fileType = content['fileType']
        merge = content['merge']
        return jsonify(Mangas().add_manga(get_manga_info(rssUrl, fileType, merge)))
    except Exception as e:
        return {'message': f'{e}'}, 500


@bp.route('/<int:manga_id>', methods=['GET'])
def getMangaById(manga_id: int):
    try:
        return jsonify(Mangas().get_manga_by_id(manga_id).to_json())
    except Exception as e:
        return {'message': f'{e}'}, 500


@bp.route('/<int:manga_id>', methods=['DELETE'])
def deleteMangaById(manga_id: int):
    try:
        return jsonify(Mangas().delete_manga(manga_id))
    except Exception as e:
        return {'message': f'{e}'}, 500
