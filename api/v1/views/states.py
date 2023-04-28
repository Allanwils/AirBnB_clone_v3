from flask import Blueprint, jsonify, request
from app import db
from models import State


states_bp = Blueprint('states', __name__, url_prefix='/api/v1/states')


@states_bp.route('', methods=['GET'])
def get_states():
    states = State.query.all()
    return jsonify([state.to_dict() for state in states])


@states_bp.route('/<int:state_id>', methods=['GET'])
def get_state(state_id):
    state = State.query.get_or_404(state_id)
    return jsonify(state.to_dict())


@states_bp.route('/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = State.query.get_or_404(state_id)
    db.session.delete(state)
    db.session.commit()
    return jsonify({}), 200


@states_bp.route('', methods=['POST'])
def create_state():
    data = request.json
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(name=data['name'])
    db.session.add(state)
    db.session.commit()
    return jsonify(state.to_dict()), 201


@states_bp.route('/<int:state_id>', methods=['PUT'])
def update_state(state_id):
    state = State.query.get_or_404(state_id)
    data = request.json
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at', 'deleted_at'):
            setattr(state, key, value)
    db.session.commit()
    return jsonify(state.to_dict()), 200
