# Benchmark de Algoritmos para Clique Máxima

Este projeto implementa um framework modular em Python para testar, comparar e avaliar algoritmos de clique máxima em grafos de diferentes tipos e tamanhos, medindo desempenho em tempo de execução, uso de memória e robustez (tratamento de timeouts e erros).

O projeto inclui:
- Algoritmos exatos (forca_bruta, backtracking, divide_conquer, programacao_dinamica)
- Heurísticas e metaheurísticas (guloso, coloring, busca_local, genetic_algorithm)
- Geração automática de grafos aleatórios, scale-free e com cliques embutidas
- Coleta e processamento de resultados

---

## Estrutura do Projeto
```

clique-problem/
├── algorithms/          # Implementações dos algoritmos
├── benchmarks/          # Benchmark e geração de suítes de teste
├── data/                # Resultados processados e brutos
│   ├── results/
│       ├── raw/         # Resultados brutos do benchmark
│       └── processed/   # Resultados processados em JSON/CSV
│ 
│   ├── empirical_analysis/ # modulo para realizar analise 
│ 
├── graphs/              # Geradores de grafos
├── main.py              # Script principal para rodar benchmarks
├── requirements.txt
└── README.md
```
---

## Requisitos

- Python 3.10+
- Dependências listadas em requirements.txt:
- 
```
pip install -r requirements.txt
```
---

## Como Executar

1. Rode o benchmark principal:
```
python3 main.py
```
2. O fluxo principal:
   - Gera as suítes de grafos (TestSuiteGenerator)
   - Executa os algoritmos definidos em main.py (TestBenchmark)
   - Salva os resultados brutos em data/results/raw/
   - Processa os resultados com DataCollector, gerando dataframes para executar a analise de dados
   - Empirical analysis, calcula o tempo médio e gasto médio de memório por algoritmo e determina sua ordem assintótica
   - Plotter gera graficos comparitivos entre os algoritmos 

---

## Licença

Projeto para fins acadêmicos e de estudo.
