from typing import Self
from common.helpers.enums import BaseEnum

__all__ = ["CategoryEnum", "FederationEnum"]


class CategoryEnum(BaseEnum):
    _DEFAULT = "--"
    PAR_A = "PAR-A - Piloto de Arrancada"
    PAR_B = "PAR-B - Piloto de Arrancada"
    PARDJ = "PARDJ - Piloto de Arrancada Drag Junior"
    PPNE_AR = "PPNE-AR - Piloto Portador de Necessidades Especiais - Arrancada"
    LPU_AR = "LPU-AR - Licença Prova Única - Arrancada"


class FederationEnum(BaseEnum):
    _DEFAULT = ("--", "--")
    FSA = ("FSA", "Federação Sergipana de Automobilismo")
    FAAES = ("FAAES", "Federação de Automobilismo do Estado do Espírito Santo")
    FAB = ("FAB", "Federação de Automobilismo da Bahia")
    FAEP = ("FAEP", "Federação de Automobilismo do Estado da Paraíba")
    FASP = ("FASP", "Federação de Automobilismo de São Paulo")
    FAERJ = ("FAERJ", "Federação de Automobilismo do Estado do Rio de Janeiro")
    FAUESC = ("FAUESC", "Federação de Automobilismo do Estado de Santa Catarina")
    FCA = ("FCA", "Federação Cearense de Automobilismo")
    FAMS = ("FAMS", "Federação de Automobilismo de Mato Grosso do Sul")
    FGA = ("FGA", "Federação Gaúcha de Automobilismo")
    FMA = ("FMA", "Federação Mineira de Automobilismo")
    FEPAUTO = ("FEPAUTO", "Federação Paraense de Automobilismo")
    FPEA = ("FPEA", "Federação Pernambucana de Automobilismo")
    FPARN = ("FPARN", "Federação Potiguar de Automobilismo")
    FPRA = ("FPRA", "Federação Paranaense de Automobilismo")
    FAUGO = ("FAUGO", "Federação Goiana de Automobilismo")
    FADF = ("FADF", "Federação de Automobilismo do Distrito Federal")
    FAEM = ("FAEM", "Federação de Automobilismo do Estado do Maranhão")
    FAA = ("FAA", "Federação Alagoana de Automobilismo")
    FAT = ("FAT", "Federação De Automobilismo Do Estado Do Tocantins")
    FAEMT = ("FAEMT", "Federação de Automobilismo do Estado de Mato Grosso")
    FAEPI = ("FAEPI", "Federação de Automobilismo do Estado do Piauí")
    MMC = ("MMC", "Manaus Motor Clube")

    federation_name: str

    def __new__(cls, federation_symbol: str, federation_name: str) -> Self:
        obj = object.__new__(cls)
        obj._value_ = federation_symbol
        obj.federation_symbol = federation_symbol
        obj.federation_name = federation_name
        return obj
