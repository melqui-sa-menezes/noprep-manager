from typing import Self

from .base import BaseEnum

__all__ = ["BrazilStatesEnum"]


class BrazilStatesEnum(BaseEnum):
    AA = ("--", "--", None)    # Default value
    AC = ("Acre", "AC", "https://static.mundoeducacao.uol.com.br/mundoeducacao/2021/01/bandeira-do-estado-do-acre.jpg")
    AL = ("Alagoas", "AL", None)
    AP = ("Amapá", "AP", None)
    AM = ("Amazonas", "AM", None)
    BA = ("Bahia", "BA", None)
    CE = ("Ceará", "CE", None)
    DF = ("Distrito Federal", "DF", None)
    ES = ("Espírito Santo", "ES", None)
    GO = ("Goiás", "GO", None)
    MA = ("Maranhão", "MA", None)
    MT = ("Mato Grosso", "MT", None)
    MS = ("Mato Grosso do Sul", "MS", None)
    MG = ("Minas Gerais", "MG", None)
    PA = ("Pará", "PA", None)
    PB = ("Paraíba", "PB", None)
    PR = ("Paraná", "PR", None)
    PE = ("Pernambuco", "PE", None)
    PI = ("Piauí", "PI", None)
    RJ = ("Rio de Janeiro", "RJ", None)
    RN = ("Rio Grande do Norte", "RN", None)
    RS = ("Rio Grande do Sul", "RS", None)
    RO = ("Rondônia", "RO", None)
    RR = ("Roraima", "RR", None)
    SC = ("Santa Catarina", "SC", None)
    SP = ("São Paulo", "SP", None)
    SE = (
        "Sergipe",
        "SE",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Bandeira_de_Sergipe.svg/800px-Bandeira_de_Sergipe.svg.png"
    )
    TO = ("Tocantins", "TO", None)

    def __new__(cls, state_name: str, state_symbol: str, flag: str | None) -> Self:
        obj = object.__new__(cls)
        obj._value_ = state_name
        obj.state_name = state_name
        obj.state_symbol = state_symbol
        obj.flag = (
            flag if flag else "https://s1.static.brasilescola.uol.com.br/be/conteudo/images/2-bandeira-do-brasil.jpg"
        )
        return obj

    def __str__(self) -> str:
        return self.state_symbol
