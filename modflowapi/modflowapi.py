from collections.abc import Sequence
from os import PathLike

from xmipy import Xmi, XmiWrapper

from .util import amend_libmf6_path

# the BMI extensions the MODFLOW API needs
EXTENSIONS = ("xmi",)


class ModflowApi(XmiWrapper):
    """
    The BMI of libmf6, from xmipy's XmiWrapper, with the extensions the
    MODFLOW API uses requested by default.

    The XMI is the extension ``mf6.xmi``.
    """

    def __init__(
        self,
        lib_path: str | PathLike,
        lib_dependency: str | None = None,
        working_directory: str = ".",
        timing: bool = False,
        logger_level: int | str = 0,
    ):
        super().__init__(
            amend_libmf6_path(lib_path),
            lib_dependency=lib_dependency,
            working_directory=working_directory,
            timing=timing,
            logger_level=logger_level,
        )

    def initialize(
        self,
        config_file: str | PathLike = "",
        requested_extensions: Sequence[str] = EXTENSIONS,
    ) -> tuple[str, ...]:
        supported = super().initialize(config_file, requested_extensions)
        missing = set(requested_extensions) - set(supported)
        if missing:
            raise RuntimeError(f"libmf6 does not support {sorted(missing)}")
        return supported

    @property
    def xmi(self) -> Xmi:
        """The XMI extension."""
        return self.get_extension("xmi")
