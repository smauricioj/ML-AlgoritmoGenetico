# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 21/09/2022

# ---------------------------------------------------------------
# IMPORTS


import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d  # necessário!
from pandas import read_csv
from numpy import arange, linspace, array, meshgrid
from shutil import rmtree
from time import sleep
from typing import Callable

# ---------------------------------------------------------------
# CLASSE


class Visualizador:
    ''' Interface para plotagem de gráficos de AG '''

    def __init__(self,
                 conf: dict):
        self.conf = conf
        self.caminho = conf['result_dir']/'default'
        self.ext = '.png'

    def setPasta(self,
                 pasta: str,
                 remove=False) -> None:
        ''' Ajusta uma pasta para salvar imagens '''

        caminho = self.conf['result_dir']/pasta
        if remove and caminho.is_dir():
            rmtree(str(caminho))
            sleep(0.5)
        caminho.mkdir(exist_ok=True)
        self.caminho = caminho

    def salvarImagem(self,
                     nome: str) -> None:
        ''' Salva a imagem corrente e limpa a memória '''

        nome += self.ext
        plt.legend()
        plt.grid()
        plt.savefig(self.caminho/nome)
        plt.clf()

    def superficie_varredura(self,
                             metrica: str,
                             show=True) -> None:
        ''' 
        Plota um objeto 3d para visualização da superfície de varredura
        armazenada em memória
        '''

        opt = 4.09299358937553  # Wolfram Alpha

        # Procura dados
        file_path = self.conf['result_dir']/metrica
        with open(file_path.with_suffix('.csv'), 'r') as file:
            df = read_csv(
                file,
                index_col=0,
                dtype=float
            )
        df.index = df.index.astype("float")
        df.columns = df.columns.astype("float")

        # Criação da figura
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        # Eixos de plotagem
        x, y = meshgrid(arange(len(df.columns)), arange(len(df.index)))

        # Dados para plot no eizo z
        z = array([[df[c][i] for c in df.columns] for i in df.index])

        # Se é aptidão ótima, plota o % em relação ao ótimo conhecido
        if metrica == 'otimo_apt':
            z = 100*z/opt
            ax.set_zlim(60, 100)
            ax.set_zticks(arange(60, 110, 10))
            ax.set_zticklabels([f'{x:.3g}%' for x in arange(60, 110, 10)])

        # Nomes dos eixos
        plt.xlabel('n_pop')
        plt.ylabel('tx_mut')
        
        surf = ax.plot_surface(x, y, z,
                               cmap='viridis',
                               edgecolor='none')
        plt.xticks(
            ticks=arange(len(df.columns)),
            labels=[f'{x:.3g}' for x in df.columns]
        )
        plt.yticks(
            ticks=arange(len(df.index)),
            labels=[f'{x:.3g}' for x in df.index]
        )
        # fig.colorbar(
        #     surf,
        #     shrink=0.5,
        #     aspect=5,
        #     location='top'
        # )

        if show:
            plt.show()
        else:
            # Salva em arquivo
            self.setPasta('Metricas')
            self.salvarImagem(metrica)

    def cromossomos(self,
                    v_min: float,
                    v_max: float,
                    objetivo: Callable,
                    pop: list,
                    geracao: int) -> None:
        '''
        Plota uma imagem com os cromossomos da população contra a função de aptidão
        '''

        # Domínio dos indivíduos
        x = linspace(v_min, v_max, 600)

        # Função de aptidão
        plt.plot(x, [objetivo(v) for v in x], label='f(x)')

        # Cada ponto é um indivíduo
        i_valores = [i.valor for i in pop]
        aptidoes = [objetivo(i.valor) for i in pop]
        plt.plot(i_valores, aptidoes, 'ro',
                 alpha=0.5,
                 label='Cromossosmo')

        # Zoom
        if any([a >= 3.6 for a in aptidoes]):
            # Insere novo eixo em cima do atual
            # Vértice inf esq e tamanho
            ax = plt.gca()
            axins = ax.inset_axes([0.5, 0.04, 0.35, 0.48])

            # Plot dentro do zoom
            # Poderia re-amostrar pra melhorar definição
            # Preguiça
            axins.plot(x, [objetivo(v) for v in x])
            axins.plot(i_valores, aptidoes, 'ro', alpha=0.5)

            # Subregião de zoom
            x1, x2, y1, y2 = 2.8, 3.15, 3.6, 4.15
            axins.set_xlim(x1, x2)
            axins.set_ylim(y1, y2)
            axins.set_xticklabels([])
            axins.set_yticklabels([])
            axins.set_xticks([])
            axins.set_yticks([])

            # Linhas pra conectar eixos
            ax.indicate_inset_zoom(axins, edgecolor="black")

        # Adornos
        plt.title(f'Cromossosmos na geração {geracao}')
        plt.xlabel('Valor x')
        plt.ylabel('Aptidão')

    def aptidao(self,
                media: list,
                melhor: list,
                maxima: list,
                minima: list) -> None:
        plt.plot(media, label='Média')
        plt.plot(melhor, label='Melhor')
        plt.fill_between(
            x=list(range(len(maxima))),
            y1=maxima,
            y2=media,
            label='Máxima',
            alpha=0.5
        )
        plt.fill_between(
            x=list(range(len(maxima))),
            y1=minima,
            y2=media,
            label='Mínima',
            alpha=0.5
        )

        plt.xlabel('Geração')
        plt.ylabel('Aptidão')
        plt.title('Desempenho do AG')

    def plot_linha(self,
                   data: list,
                   label: str) -> None:
        plt.plot(data, label=label)

    def setVarreduraUni(self,
                        param: str) -> None:
        plt.xlabel('Geração')
        plt.ylabel('Aptidão')
        plt.title(f'Comparação de valores de {param}')
