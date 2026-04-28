import lib.models.ilo_abastecimientos_almacenes_y_trafico_v01 as ilo_aayt_v01
import lib.models.ilo_ferrocarril_industrial_v02 as ilo_fi_v02
import lib.models.ilo_fundicion_v05 as ilo_f_v05

class ManagementHandler:
	@staticmethod
	def get_by_corporation_and_id(corporation, management_id):
		handler_map = {
			"cuajone": CuajoneManagementVersion,
			"ilo": IloManagementVersion,
			"toquepala": ToquepalaManagementVersion,
		}
		handler = handler_map.get(corporation)
		if handler:
			return handler.get_by_id(management_id)
		return None

	@staticmethod
	def get_model_by_corporation_and_id(corporation, management_id, version):
		handler_map = {
			"cuajone": CuajoneManagementVersion,
			"ilo": IloManagementVersion,
			"toquepala": ToquepalaManagementVersion,
		}
		handler = handler_map.get(corporation)
		if handler:
			return handler.get_model(management_id, version)
		return None

class CuajoneManagementVersion:
	CONCENTRADORA = "concentradora"
	MANTENIMIENTO = "mantenimiento"
	MINA = "mina"

	@staticmethod
	def get_by_id(management_id):
		mapping = {
			1: CuajoneManagementVersion.CONCENTRADORA,
			2: CuajoneManagementVersion.MANTENIMIENTO,
			3: CuajoneManagementVersion.MINA,
		}
		return mapping.get(management_id)

	@staticmethod
	def get_model(management_id, version): 
		mapping = {
			(1, "v06"): None,
			(2, "v03"): None,
			(3, "v04"): None,
		}
		return mapping.get((management_id, version))


class IloManagementVersion:
	ABASTECIMIENTOS = "abastecimientos_almacenes_y_trafico"
	FERROCARRIL = "ferrocarril_industrial"
	FUNDICION = "fundicion"
	MANTENIMIENTO = "mantenimiento"
	REFINERIA = "refineria"

	@staticmethod
	def get_by_id(management_id):
		mapping = {
			1: IloManagementVersion.ABASTECIMIENTOS,
			2: IloManagementVersion.FERROCARRIL,
			3: IloManagementVersion.FUNDICION,
			4: IloManagementVersion.MANTENIMIENTO,
			5: IloManagementVersion.REFINERIA,
		}
		return mapping.get(management_id)

	@staticmethod
	def get_model(management_id, version): 
		mapping = {
			(1, "v01"): ilo_aayt_v01.IloAbastecimientoAlmacenesYTraficoV1,
			(2, "v02"): ilo_fi_v02.IloFerrocarrilIndustrialV02,
			(3, "v05"): ilo_f_v05.IloFundicionV05,
			(4, "v--"): None,
			(5, "v04"): None,
		}
		return mapping.get((management_id, version))


class ToquepalaManagementVersion:
	LESDE = "lesde"
	MANTENIMIENTOC = "mantenimiento_concentradora"
	MANTENIMIENTOM = "mantenimiento_mina"
	OPERACIONESM = "operaciones_mina"
	OPERACIONESMV = "operaciones_mina_volquetes"
	QUEBRADA = "quebrada_honda"

	@staticmethod
	def get_by_id(management_id):
		mapping = {
			1: ToquepalaManagementVersion.LESDE,
			2: ToquepalaManagementVersion.MANTENIMIENTOC,
			3: ToquepalaManagementVersion.MANTENIMIENTOM,
			4: ToquepalaManagementVersion.OPERACIONESM,
			5: ToquepalaManagementVersion.OPERACIONESMV,
			6: ToquepalaManagementVersion.QUEBRADA,
		}
		return mapping.get(management_id)

	@staticmethod
	def get_model(management_id, version): 
		mapping = {
			(1, "v--"): None,
			(2, "v--"): None,
			(3, "v--"): None,
			(4, "v--"): None,
			(5, "v--"): None,
			(6, "v--"): None,
		}
		return mapping.get((management_id, version))