from odmantic.config import BaseODMConfig
from odmantic.field import ODMField, FieldProxy


def test_hash_passthrough():
    field = ODMField(primary_field=False, key_name="name", model_config=BaseODMConfig())
    proxy = FieldProxy(parent=None, field=field)

    assert hash(field) == hash(proxy)