class CorporationHandler:
    CERV = "cerv"
    CUAJONE = "cuajone"
    ILO = "ilo"
    TOQUEPALA = "toquepala"

    @staticmethod
    def get_by_id(id_):
        mapping = {
            1: CorporationHandler.CERV,
            2: CorporationHandler.CUAJONE,
            3: CorporationHandler.ILO,
            4: CorporationHandler.TOQUEPALA,
        }
        return mapping.get(id_)