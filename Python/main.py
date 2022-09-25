# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 14/09/2022

# ---------------------------------------------------------------
# IMPORTS

from json import load
from pathlib import Path

from algoritmogenetico import AlgoritmoGenetico

# ---------------------------------------------------------------
# MAIN

def main():
    # Dicionário de configurações -------------------------
    with open(Path.cwd()/'conf.json',
              encoding='utf-8') as conf_file:
        conf = load(conf_file)
    # -----------------------------------------------------

    # Diretórios ------------------------------------------
    conf['main_dir'] = Path.cwd().parent
    conf['result_dir'] = conf['main_dir']/'Resultados'
    conf['result_dir'].mkdir(exist_ok=True)
    # -----------------------------------------------------

    # Wolfram alpha ---------------------------------------
    # from math import pi, atan, sqrt, sin, fabs
    # for n in range(10,20):
    #     x = (pi*n)/16 - (1/16)*atan(sqrt(31/33))
    #     y = x + fabs(sin(32*x))
    #     print( f'{x} -> {y}' )
    # return
    # -----------------------------------------------------

    # Instâncias ------------------------------------------
    ag = AlgoritmoGenetico(conf=conf)
    # -----------------------------------------------------

    # Testa -----------------------------------------------
    # ag.executa()
    # -----------------------------------------------------

    # Testa n ---------------------------------------------
    # for mut in [0.001, 0.01, 0.1]:
    #     ag = AlgoritmoGenetico(conf=conf)
    #     ag.tx_mut = mut
    #     ag.executa()

    # for crz in [0.05, 0.2, 0.7]:
    #     ag = AlgoritmoGenetico(conf=conf)
    #     ag.tx_crz = crz
    #     ag.executa()

    # for pop in [10, 30, 50]:
    #     ag = AlgoritmoGenetico(conf=conf)
    #     ag.n_pop = pop
    #     ag.executa()
    # -----------------------------------------------------

    # Varredura unidimensional ----------------------------
    # ag.n_pop = 55
    # ag.tx_mut = 0.06
    # ag.varredura_unidimensional(n=30, param='tx_crz')
    # -----------------------------------------------------

    # Varredura bidimensional -----------------------------
    # ag.n_geracoes = 200
    # ag.varredura_bidimensional(
    #     n=30,
    #     param1='tx_mut',
    #     param2='n_pop'
    # )
    # ag.visual.superficie_varredura(
    #     'otimo_apt',
    #     show=False
    # )
    # ag.visual.superficie_varredura(
    #     'n_geracoes_otimo',
    #     show=False
    # )
    # -----------------------------------------------------

    # Ponto ótimo da varredura dimimensional --------------
    # ag.n_geracoes = 140
    # ag.tx_mut = 0.03
    # ag.n_pop = 91
    # ag.varredura_unidimensional(n=150, param='tx_crz')
    # -----------------------------------------------------


if __name__ == '__main__':
    main()