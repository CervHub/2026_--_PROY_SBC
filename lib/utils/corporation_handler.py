class CorporationHandler:
    CUAJONE = "cuajone"
    ILO = "ilo"
    TOQUEPALA = "toquepala"

    @staticmethod
    def get_by_id(id_):
        mapping = {
            1: CorporationHandler.CUAJONE,
            2: CorporationHandler.ILO,
            3: CorporationHandler.TOQUEPALA,
        }
        return mapping.get(id_)