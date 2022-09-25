# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 14/09/2022

# ---------------------------------------------------------------
# IMPORTS

from .individuo import Individuo
from .visualizador import Visualizador

from dataclasses import dataclass, field
from math import sin, fabs, pi, sqrt, floor
from random import choices, random, randint, uniform, sample
from numpy import average, linspace
from pandas import DataFrame

# ---------------------------------------------------------------
# CLASSE


@dataclass
class AlgoritmoGenetico:
    ''' Classe para implementação de um algoritmo genético '''

    # Configuração
    conf: dict = field(repr=False, default_factory=dict)
    ''' Arquivo de configurações '''

    # Hiperparâmetros

    n_geracoes: int = 300
    ''' Nº de gerações para critério de parada '''

    n_pop: int = 50
    ''' Nº de indivíduos na população '''

    tx_crz: float = 0.5
    ''' Taxa de cruzamento dos indivíduos '''

    tx_mut: float = 0.05
    ''' Taxa de mutação dos indivíduos '''

    # Variáveis da função de aptidão

    v_max: float = field(repr=False, default=pi)
    ''' valor máximo '''

    v_min: float = field(repr=False, default=0)
    ''' valor minimo '''

    n_bits: int = field(repr=False, default=4*8)
    ''' tamanho dos cromossomos da população '''

    # Repositórios de métricas e medidas

    pop: list[Individuo] = field(repr=False, init=False, default_factory=list)
    ''' População atual de indivíduos '''

    melhor_individuo: dict = field(repr=True, init=False, default_factory=dict)
    ''' Resultados do melhor indivíduo '''

    metricas: dict = field(repr=False, init=False, default_factory=dict)
    ''' Resultados do melhor indivíduo '''

    def __post_init__(self):
        # Métricas para varredura
        self.metricas = {
            'n_geracoes_otimo': 0.0,
            'otimo_apt': 0.0
        }
        self.limites_varredura = {
            'tx_mut': (0.01, 0.06),
            'tx_crz': (0.05, 0.95),
            'n_pop': (10, 100)
        }

        # Registros para plot
        self.apt_media = list()
        self.apt_maxima = list()
        self.apt_minima = list()
        self.apt_best = list()
        self._visual = Visualizador(self.conf)

    # Propriedades

    @property
    def visual(self) -> Visualizador:
        ''' Interface para visualizador '''
        return self._visual

    # Métodos privados

    def _novoIndividuo(self,
                       cr=None):
        ''' Cria um novo indivíduo com os parâmetros conhecidos '''
        return Individuo(
            _cromossomo=cr,
            n_bits=self.n_bits,
            l_inf=self.v_min,
            l_sup=self.v_max
        )

    def _limpaRegistros(self):
        ''' Limpa os registros e listas para uma nova execução '''
        self.apt_media.clear()
        self.apt_maxima.clear()
        self.apt_minima.clear()
        self.apt_best.clear()
        self.melhor_individuo = {
            'aptidao': self.v_min,
            'geracao_encontrado': 0
        }

    def _objetivo(self,
                  valor: float) -> float:
        ''' Função objetivo, calcula a aptidão dos individuos '''
        return valor + fabs(sin(32*valor))

    def _selecao(self,
                 aptidoes: list) -> list:
        '''
        Seleciona dois individuos para cruzamento com base em sua aptidao
        '''
        i = choices(self.pop, weights=aptidoes, k=2)
        while i[0] == i[1]:
            i = choices(self.pop, weights=aptidoes, k=2)
        return i

    def _cruzamento(self,
                    geradores: list) -> list:
        ''' Define o resultado o cruzamento de dois geradores '''

        # salva os cromossomos originais
        cr1 = geradores[0].cromossomo
        cr2 = geradores[1].cromossomo

        # cria novos cromossomos
        cr_f1 = ''
        cr_f2 = ''

        # verifica a taxa de cruzamento
        if random() >= self.tx_crz:
            # se não houver cruzamento, descendentes são cópias
            cr_f1 = cr1
            cr_f2 = cr2
        else:
            # seleciona loci de cruzamento
            loci = sorted(sample(
                range(1, self.n_bits-2),
                k=randint(1, floor(sqrt(self.n_bits)))
            ))

            # adiciona o começo e o fim
            loci.insert(0, 0)
            loci.append(self.n_bits)

            # lista de tuplas com começo e fim dos pedaços
            slices = list(zip(loci[:-1], loci[1:]))

            # em cada par de loci
            for i, (a, b) in enumerate(slices):
                # mistura cromossomos
                if i % 2 == 0:
                    cr_f1 += cr1[a:b]
                    cr_f2 += cr2[a:b]
                else:
                    cr_f1 += cr2[a:b]
                    cr_f2 += cr1[a:b]

        # Retorna uma lista com os novos individuos
        return [
            self._novoIndividuo(cr=cr)
            for cr in [cr_f1, cr_f2]
        ]

    def _mutacao(self,
                 individuos: list) -> None:
        ''' Aplica mutação em todos os individuos da lista '''

        # para cada individuo da lista
        for ind in individuos:
            # checa probabilidade
            if random() < self.tx_mut:
                # escolhe um locus
                locus = randint(0, self.n_bits-1)
                cr = ind.cromossomo
                if cr[locus] == '1':
                    pos = '0'
                else:
                    pos = '1'

                # troca valor
                ind.cromossomo = pos.join([cr[:locus],cr[locus+1:]])

    # Métodos públicos

    def executa(self,
                plot=True) -> None:
        ''' Executa o algoritmo com base nos hiperparametros e individuos '''

        # Limpa tudo
        self._limpaRegistros()

        # Arruma pasta pra salvar imagens
        if plot:
            pasta = f'pop_{self.n_pop}_crz_{self.tx_crz}_mut_{self.tx_mut}'
            self._visual.setPasta(pasta, remove=True)

        # População inicial aleatória
        self.pop = [self._novoIndividuo() for _ in range(int(self.n_pop))]

        # Só pra complicar a vida do algoritmo
        for i in self.pop:
            i.valor = uniform(0, pi/4)

        # Loop de gerações
        for geracao in range(1, self.n_geracoes+1):
            # Calcula aptidao de toda população
            aptidoes = [self._objetivo(i.valor) for i in self.pop]

            # Registra o melhor individuo
            if max(aptidoes) > self.melhor_individuo['aptidao']:
                self.melhor_individuo = {
                    # 'individuo':self.pop[aptidoes.index(max(aptidoes))],
                    'aptidao': max(aptidoes),
                    'geracao_encontrado': geracao
                }

            # Registros para plotagem
            self.apt_media.append(average(aptidoes))
            if plot:
                self.apt_maxima.append(max(aptidoes))
                self.apt_minima.append(min(aptidoes))
                self.apt_best.append(self.melhor_individuo['aptidao'])
                if (
                    geracao == 1
                    or (geracao <= 20 and geracao % 5 == 0)
                    or geracao % 50 == 0
                    or geracao == self.n_geracoes
                ):
                    self._visual.cromossomos(
                        v_min=self.v_min,
                        v_max=self.v_max,
                        objetivo=self._objetivo,
                        pop=self.pop,
                        geracao=geracao
                    )
                    nome = f'cr_{str(geracao).zfill(3)}'
                    self._visual.salvarImagem(nome)

            # Nova população, descendentes
            nova_pop = list()

            # Preencher nova população
            while len(nova_pop) < self.n_pop:
                # Seleciona geradores
                geradores = self._selecao(aptidoes)

                # Realiza cruzamento
                descendentes = self._cruzamento(geradores)

                # Causa mutação
                self._mutacao(descendentes)

                # Adiciona na lista
                nova_pop.extend(descendentes)

            # Se tem muitos indivíduos, mata
            while len(nova_pop) > self.n_pop:
                nova_pop.pop(randint(0, len(nova_pop)-1))

            # Atualiza população
            self.pop = nova_pop

        if plot:
            # Linhas e áreas
            self._visual.aptidao(
                self.apt_media,
                self.apt_best,
                self.apt_maxima,
                self.apt_minima
            )

            # Salva imagem
            self._visual.salvarImagem('aptidao')

    def executa_n(self,
                  n: int = 10,
                  plot: bool = True,
                  label_params: list = []) -> None:
        '''
        Executa o AG n vezes
        Armazena as métricas para varredura
        Atualiza a aptidão média de acordo
        Plota o gráfico
        '''
        apt_media = None
        n_geracoes_otimo = []
        otimo_apt = []
        for _ in range(n):
            # Executa o AG
            self.executa(plot=False)

            # Atualiza lista das métricas
            n_geracoes_otimo.append(
                self.melhor_individuo['geracao_encontrado']
            )
            otimo_apt.append(
                self.melhor_individuo['aptidao']
            )

            # Somatório da aptidao média
            if plot:
                if not apt_media:
                    apt_media = self.apt_media
                else:
                    apt_media = [
                        a+b
                        for a, b in zip(apt_media, self.apt_media)
                    ]

        # Métricas
        self.metricas['n_geracoes_otimo'] = sum(n_geracoes_otimo)/n
        self.metricas['otimo_apt'] = sum(otimo_apt)/n

        # Gráfico da aptidão média
        if plot:
            label = 'default'
            if all([p in self.__dict__ for p in label_params]):
                label = ' | '.join(
                    [f'{p} : {self.__dict__[p]:g}' for p in label_params]
                )
            self._visual.plot_linha(
                data=[x/n for x in apt_media],
                label=label
            )

    def varredura_unidimensional(self,
                                 n: int = 10,
                                 param: str = 'tx_mut') -> None:
        '''
        Plota os valores da aptidão média para multiplas 
        execuções do AG ao longo de um espaço unidimensional
        dos hiperparâmetros
        '''

        assert(param in self.limites_varredura)
        assert(param in self.__dict__)

        # Cada hiperparâmetro é amostrado
        n_amostras = 6
        param_a = linspace(
            self.limites_varredura[param][0],
            self.limites_varredura[param][1],
            n_amostras
        )

        # Para cada amostra, executa n vezes
        for amostra in param_a:
            print(f"{amostra:g}, ", end='', flush=True)
            self.__dict__[param] = amostra
            self.executa_n(n=n, plot=True, label_params=[param])
        print('')

        # Salva o arquivo de imagem
        pasta = f'varredura_{param}_n_{n}_'
        pasta += '_'.join([
            f'{p}_{self.__dict__[p]}'
            if p != param else ''
            for p in ['n_pop', 'tx_mut', 'tx_crz']
        ])
        self._visual.setPasta(pasta, remove=True)
        self._visual.setVarreduraUni(param)
        self._visual.salvarImagem(pasta)

    def varredura_bidimensional(self,
                                n: int = 10,
                                param1: str = 'tx_mut',
                                param2: str = 'tx_crz') -> None:
        '''
        Busca o valor de métricas em um espaço bidimensional
        dos hiperparâmetros do AG e cria uma superfície
        para visualização
        '''
        assert(param1 in self.limites_varredura)
        assert(param1 in self.__dict__)
        assert(param2 in self.limites_varredura)
        assert(param2 in self.__dict__)

        # Cada hiperparâmetro é amostrado
        n_amostras = 11
        param1_a, param2_a = (
            linspace(self.limites_varredura[p][0],
                     self.limites_varredura[p][1],
                     n_amostras)
            for p in [param1, param2]
        )

        # Tabelas para varredura
        dfs = {
            metrica: DataFrame(
                index=param1_a,
                columns=param2_a,
                dtype=float
            ) for metrica in self.metricas
        }

        # Varredura dos eixos
        for amostra1 in param1_a:
            # Muda hiperparâmetro
            print(f'{param1} : {amostra1:g}')
            self.__dict__[param1] = amostra1
            for amostra2 in param2_a:
                # Muda hiperparâmetro
                print(f'|----{param2} : {amostra2:g}')
                self.__dict__[param2] = amostra2

                # Executa AG n vezes
                self.executa_n(n=n, plot=False)

                # Salva métricas na tabela
                for metrica in dfs:
                    dfs[metrica].loc[
                        amostra1,
                        amostra2
                    ] = self.metricas[metrica]

        for metrica in dfs:
            file_path = self.conf['result_dir']/metrica
            with open(file_path.with_suffix('.csv'), 'w') as file:
                dfs[metrica].to_csv(
                    file,
                    float_format='%.6f'
                )
