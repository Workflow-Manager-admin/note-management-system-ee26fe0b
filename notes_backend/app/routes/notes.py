from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from app.models import db, Note
from app.schemas import NoteSchema

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Operations on Notes"
)

@blp.route("/")
class NotesListResource(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema(many=True), description="List all notes")
    def get(self):
        """Get all notes in the system."""
        notes = Note.query.order_by(Note.created_at.desc()).all()
        return notes

    # PUBLIC_INTERFACE
    @blp.arguments(NoteSchema, location="json")
    @blp.response(201, NoteSchema, description="Create a new note")
    def post(self, new_note_data):
        """Create a new note with title and optional content."""
        note = Note(**new_note_data)
        db.session.add(note)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Integrity error while creating note.")
        return note

@blp.route("/<int:note_id>")
class NoteResource(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema, description="Retrieve a note by ID")
    def get(self, note_id):
        """Get a note by its ID."""
        note = Note.query.get(note_id)
        if not note:
            abort(404, message="Note not found")
        return note

    # PUBLIC_INTERFACE
    @blp.arguments(NoteSchema(partial=True), location="json")
    @blp.response(200, NoteSchema, description="Update a note")
    def put(self, update_data, note_id):
        """Update a note by its ID."""
        note = Note.query.get(note_id)
        if not note:
            abort(404, message="Note not found")
        if 'title' in update_data:
            note.title = update_data['title']
        if 'content' in update_data:
            note.content = update_data['content']
        db.session.commit()
        return note

    # PUBLIC_INTERFACE
    @blp.response(204, description="Delete a note")
    def delete(self, note_id):
        """Delete a note by ID."""
        note = Note.query.get(note_id)
        if not note:
            abort(404, message="Note not found")
        db.session.delete(note)
        db.session.commit()
        return ""
