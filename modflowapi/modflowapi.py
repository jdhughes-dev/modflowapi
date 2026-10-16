from collections.abc import Sequence
from os import PathLike

from bmipy import BmiPointers
from xmipy import Xmi, XmiWrapper

from .util import amend_libmf6_path

# the BMI extensions the MODFLOW API needs
EXTENSIONS = ("xmi", "bmi:pointers")


class ModflowApi(XmiWrapper):
    """
    The BMI of libmf6, from xmipy's XmiWrapper, with the extensions the
    MODFLOW API uses requested by default.

    The XMI is the extension ``mf6.xmi`` and pointers to libmf6 memory come
    from ``mf6.pointers``. A pointer is valid from initialize to finalize
    unless the variable is in the ``"bmi:pointers:transient"`` set.
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

    @property
    def pointers(self) -> BmiPointers:
        """The pointers extension."""
        return self.get_extension("bmi:pointers")

    def is_transient(self, address: str) -> bool:
        """True if a pointer to the variable must be fetched again after any
        call that changes the model state."""
        return address in self.get_varset_members("bmi:pointers:transient")
