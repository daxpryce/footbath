from collections.abc import Mapping
from typing import Any, ClassVar, Self

import humps

__all__ = ["ZeepOps"]

"""
zeep dynamically generates classes and objects based on what it gets back as a result
it makes for some very weak typing, and we need to rely on dunder attributes for making it work for our data models

this class is primarily used to introduce a classmethod on all dataclass models we have that will convert from a 
zeep returned object to our own model. by convention we will use all of the same names as the waleg returns,
but converting the PascalCase field names into lower_snake_case, and occasionally mapping invalid names (to python) to 
valid names.
"""


class ZeepOps:
    """
    Some of the field names returned by Washington State Legislature have reserved words as their name
    (e.g.: Amendment(..., Type = 'Floor', ...))

    As `type` is reserved, we aren't going to allow it as an attribute name on our data model

    See `Amendment` as an example for our override mapping.
    """

    zeep_aliases: ClassVar[
        Mapping[str, str]
    ] = {}  # empty by default, but dataclasses that mix this in can override

    @classmethod
    def from_zeep(cls, item: Mapping[str, Any]) -> Self:
        renamed = {
            cls.zeep_aliases.get(
                snake_name := humps.decamelize(key),
                snake_name,
            ): value
            for key, value in item.items()
        }

        # Python's type system cannot describe the dynamically generated
        # dataclass constructor arguments here.
        return cls(**renamed)  # type: ignore[call-arg]
