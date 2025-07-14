from marshmallow import Schema, fields

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for serializing a Note."""
    id = fields.Int(dump_only=True, description="ID of the note")
    title = fields.Str(required=True, description="Title of the note")
    content = fields.Str(description="Content of the note")
    created_at = fields.DateTime(dump_only=True, description="Creation timestamp")
    updated_at = fields.DateTime(dump_only=True, description="Last update timestamp")
