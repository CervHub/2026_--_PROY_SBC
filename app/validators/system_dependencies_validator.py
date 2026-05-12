import shutil


class SystemDependenciesValidator:
    @staticmethod
    def validate_poppler():
        if shutil.which("pdftoppm") is None:
            raise RuntimeError("Poppler no instalado")