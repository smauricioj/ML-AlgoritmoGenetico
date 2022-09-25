# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 14/09/2022

# ---------------------------------------------------------------
# IMPORTS

from dataclasses import dataclass, field
from random import randint

# ---------------------------------------------------------------
# CLASS

@dataclass
class Individuo:
    ''' Classe para conter informações sobre soluções individuais '''
    
    n_bits: int = field(repr=False, default=4*8, kw_only=True)
    ''' nº de bits no cromossomo '''

    l_sup: float = field(repr=False, default=100, kw_only=True)
    ''' limite superior da aptidão'''

    l_inf: float = field(repr=False, default=0, kw_only=True)
    ''' limite infeior da aptidão'''

    _cromossomo: str | None = field(default=None)
    ''' cromossomo na base 02 = genes'''

    _valor: int | None = field(init=False, default=None)
    ''' cromossomo na base 10 = valor interno'''

    def __post_init__(self):
        # Qual maior _valor possível representar com n_bits?
        self._vmax = 2**self.n_bits - 1

        '''
        Um indivíduo pode ser construído com
        um cromossomo
        ou sem nada, que gera de forma aleatória
        '''
        if self._cromossomo:
            # Individuo criado com base em um cromossomo, falta valor
            assert(len(self._cromossomo) == self.n_bits)
            self._valor = self._bits_to_int(self._cromossomo)
        else:
            # Individuo criado sem nada, aleatório
            self._valor = randint(0, self._vmax)
            self._cromossomo = self._int_to_bits(self._valor)

    @property
    def cromossomo(self) -> str:
        ''' getter de cromossomo '''
        return self._cromossomo

    @cromossomo.setter
    def cromossomo(self, cromossomo: str) -> None:
        ''' setter de cromossomo '''

        # Verifica bounds
        assert(len(cromossomo) == self.n_bits)

        # Atualiza cromossomo
        self._cromossomo = cromossomo

        # Atualiza valor de acordo com o novo cromossomo
        self._valor = self._bits_to_int(cromossomo) 

    @property
    def valor(self) -> float:
        ''' getter de valor '''

        # m é a inclinação da reta que contém (0, l_inf) e (_vmax, l_sup)
        # (_valor = _vmax) <-> (valor = l_sup)
        # (_valor = 0)     <-> (valor = l_inf)
        m = (self.l_sup - self.l_inf) / self._vmax
        return (m * (self._valor - self._vmax)) + self.l_sup

    @valor.setter
    def valor(self, v: float) -> None:
        ''' setter de cromossomo '''

        # Verifica bounds
        assert(self.l_inf <= v <= self.l_sup)

        # Atualiza valor
        m = self._vmax / (self.l_sup - self.l_inf)
        self._valor = (m * (v - self.l_sup)) + self._vmax

        # Atualiza cromossomo de acordo com o novo valor
        self._cromossomo = self._int_to_bits(int(self._valor))

    def _bits_to_int(self, bits):
        ''' transforma string de bits em inteiro '''
        return sum([
            int(bit) * (2**i)
            for i, bit in enumerate(bits)
        ])

    def _int_to_bits(self, x):
        ''' transforma inteiro em string de bits '''

        return ''.join([
            '1' if x & (2**bit) > 0
            else '0'
            for bit in range(self.n_bits)
        ])
    
    


