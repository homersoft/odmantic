import re
from typing import TYPE_CHECKING, Any, Dict, Pattern, Sequence, Union

if TYPE_CHECKING:
    from odmantic.field import FieldProxy


class QueryExpression(Dict[str, Any]):
    """Base object used to build queries.

    All comparison and logical operators returns `QueryExpression` objects.

    The `|` and `&` operators are supported for respectively the
    [or][odmantic.query.or_] and the [and][odmantic.query.and_] logical operators.

    Warning:
        When using those operators make sure to correctly bracket the expressions
        to avoid python operator precedence issues.
    """

    # def __repr__(self):
    #     parent_repr = super().__repr__()
    #     if parent_repr == "{}":
    #         parent_repr = ""
    #     return f"QueryExpression({parent_repr})"

    def __or__(self, other: "QueryExpression") -> "QueryExpression":
        return or_(self, other)

    def __and__(self, other: "QueryExpression") -> "QueryExpression":
        return and_(self, other)


def and_(*elements: Union[QueryExpression, bool]) -> QueryExpression:
    """Logical **AND** operation between multiple `QueryExpression` objects."""
    return QueryExpression({"$and": elements})


def or_(*elements: Union[QueryExpression, bool]) -> QueryExpression:
    """Logical **OR** operation between multiple `QueryExpression` objects."""
    return QueryExpression({"$or": elements})


def nor_(*elements: Union[QueryExpression, bool]) -> QueryExpression:
    """Logical **NOR** operation between multiple `QueryExpression` objects."""
    return QueryExpression({"$nor": elements})


def _cmp_expression(f: "FieldProxy", op: str, cmp_value: Any) -> QueryExpression:
    # FIXME 🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮
    from odmantic.model import EmbeddedModel

    if isinstance(cmp_value, EmbeddedModel):
        value = cmp_value.doc()
    else:
        value = cmp_value
    return QueryExpression({+f: {op: value}})


FieldProxyAny = Union["FieldProxy", Any]


def eq(field: FieldProxyAny, value: Any) -> QueryExpression:
    """Equality comparison operator."""
    return _cmp_expression(field, "$eq", value)


def ne(field: FieldProxyAny, value: Any) -> QueryExpression:
    """Inequality comparison operator (includes documents not containing the field)."""
    return _cmp_expression(field, "$ne", value)


def gt(field: FieldProxyAny, value: Any) -> QueryExpression:
    """Greater than (strict) comparison operator (i.e. >)."""
    return _cmp_expression(field, "$gt", value)


def gte(field: FieldProxyAny, value: Any) -> QueryExpression:
    """Greater than or equal comparison operator (i.e. >=)."""
    return _cmp_expression(field, "$gte", value)


def lt(field: FieldProxyAny, value: Any) -> QueryExpression:
    """Less than (strict) comparison operator (i.e. <)."""
    return _cmp_expression(field, "$lt", value)


def lte(field: FieldProxyAny, value: Any) -> QueryExpression:
    """Less than or equal comparison operator (i.e. <=)."""
    return _cmp_expression(field, "$lte", value)


def in_(field: FieldProxyAny, sequence: Sequence) -> QueryExpression:
    """Select instances where `field` is contained in `sequence`."""
    return _cmp_expression(field, "$in", sequence)


def not_in(field: FieldProxyAny, sequence: Sequence) -> QueryExpression:
    """Select instances where `field` is **not** contained in `sequence`."""
    return _cmp_expression(field, "$nin", sequence)


def match(field: FieldProxyAny, pattern: Union[Pattern, str]) -> QueryExpression:
    """Select instances where `field` matches the `pattern` regular expression."""
    # FIXME might create incompatibilities
    # https://docs.mongodb.com/manual/reference/operator/query/regex/#regex-and-not
    if isinstance(pattern, str):
        r = re.compile(pattern)
    else:
        r = pattern
    return QueryExpression({+field: r})