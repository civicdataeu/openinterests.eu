from flask import Blueprint, render_template, request
from werkzeug.exceptions import NotFound

from grano.service import search_entities
from grano.lib.pager import Pager
from grano.model import Entity


entities = Blueprint('entities', __name__, static_folder='../static', template_folder='../templates')


@entities.route('/entities')
def search():
    searcher = search_entities(request.args)
    pager = Pager(searcher, 'search')
    return render_template('search.html', searcher=searcher, pager=pager)

@entities.route('/entities/<id>')
def view(id):
    entity = Entity.by_id(id)
    if entity is None:
        raise NotFound()
    inbound_sections = []
    for schema in entity.inbound_schemata:
        pager_name = schema.name + '_in'
        pager = Pager(entity.inbound_by_schema(schema), pager_name, id=id)
        inbound_sections.append((schema, pager))
    outbound_sections = []
    for schema in entity.outbound_schemata:
        pager_name = schema.name + '_out'
        pager = Pager(entity.outbound_by_schema(schema), pager_name, id=id)
        outbound_sections.append((schema, pager))
    return render_template('entity.html', entity=entity,
        inbound_sections=inbound_sections,
        outbound_sections=outbound_sections)