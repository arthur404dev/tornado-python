from marshmallow import Schema, fields


class PayloadSchema(Schema):
    serial = fields.Str(required=True)
    datahora_inicio = fields.DateTime(required=True)
    datahora_fim = fields.DateTime(required=True)
