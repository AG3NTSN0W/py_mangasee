from resource.utils import to_json
from flask import Blueprint, jsonify, request
from repository.chapters_DB import MangaChapter, Mangachapters

bp = Blueprint('chapter', __name__, url_prefix='/chapters')


@bp.route('/<int:manga_id>', methods=['GET'])
def getChapters(manga_id: int):
    try:
        return jsonify(to_json(Mangachapters().get_manga_chapter(manga_id)))
    except Exception as e:
        return {'message': f'{e}'}, 500


@bp.route('/titles/<int:manga_id>', methods=['GET'])
def getAllChaptersTitles(manga_id: int):
    try:
        return jsonify(Mangachapters().get_all_manga_chapters(manga_id))
    except Exception as e:
        return {'message': f'{e}'}, 500
