# ML-AlgoritmoGenetico

## Objetivos do projeto

Repositório dos codigos desenvolvidos na disciplina de Aprendizagem de Máquina, no tópico de Algoritmo Genético

## O que está incluso?

### (De)Codificação Personalizada

Indivíduos possuem um cromossomo de tamanho variável. Com a implementação da (de)codificação personalizada, todos os loci são significativos na representação do código genético.

### Seleção, Cruzamento e Mutação

As operações do AG são implementadas fazendo uso de python nativo. Método de seleção da roleta, cruzamento de múltiplos segmentos e mutação simples.

### Testes

Um estudo de caso está implementado. A função de aptidão é $g(y) = y + |sen(32y)|, 0 \le y \le pi$, onde $y$ representa um valor real. Diversos testes são realizados sobre esse caso, incluindo varreduras (unidimensional e bidimensional) no espaço dos hiper parâmetros.

### Visualização gráfica

Uma classe especializada para visualizar os resultados também está presente. Gráficos de linhas representando aptidão média, distribuição dos cromossosmos no domínio de aptidão e superfícies de varredura podem ser criados com facilidade.

## Estrutura do projeto

```text
ML-AlgoritmoGenetico/
├── Python/
│   ├── algoritmogenetico/
│   │   ├── __init__.py
│   │   ├── algoritmogenetico.py
│   │   ├── individuo.py
│   │   └── visualizador.py
│   ├── requirements.txt
│   ├── conf.json
│   └── main.py
├── README.md
├── LICENSE.md
└── .gitignore
```
