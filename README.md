# Benchmark de Algoritmos para Clique Máxima

Este projeto implementa um framework modular em Python para testar, comparar e avaliar algoritmos de clique máxima em grafos de diferentes tipos e tamanhos, medindo desempenho em tempo de execução, uso de memória e robustez (tratamento de timeouts e erros).

O projeto inclui:
- Algoritmos exatos (forca_bruta, backtracking, divide_conquer, programacao_dinamica)
- Heurísticas e metaheurísticas (guloso, coloring, busca_local, genetic_algorithm)
- Geração automática de grafos aleatórios, scale-free e com cliques embutidas
- Coleta e processamento de resultados em JSON e CSV

---

## Estrutura do Projeto

clique-problem/
├── algorithms/          # Implementações dos algoritmos
├── benchmarks/          # Benchmark e geração de suítes de teste
├── data/                # Resultados processados e brutos
│   ├── results/
│       ├── raw/         # Resultados brutos do benchmark
│       └── processed/   # Resultados processados em JSON/CSV
├── graphs/              # Geradores de grafos
├── main.py              # Script principal para rodar benchmarks
├── requirements.txt
└── README.md

---

## Requisitos

- Python 3.10+
- Dependências listadas em requirements.txt:

pip install -r requirements.txt

---

## Como Executar

1. Rode o benchmark principal:

python3 main.py

2. O fluxo principal:
   - Gera as suítes de grafos (TestSuiteGenerator)
   - Executa os algoritmos definidos em main.py (TestBenchmark)
   - Salva os resultados brutos em data/results/raw/benchmark_output.json
   - Processa os resultados com DataCollector, gerando JSON e CSV em data/results/processed/

3. Resultados processados incluem:
   - grafo_id: índice do grafo na suíte
   - algoritmo: nome do algoritmo
   - tamanho_clique: tamanho da clique encontrada
   - tempo_execucao: tempo em segundos
   - uso_memoria: memória usada em bytes
   - timeout: se ocorreu timeout
   - erro: se ocorreu algum erro

---

## Customização

- É possível adicionar novos algoritmos ao dicionário algorithms em main.py
- Você pode ajustar o timeout individual de cada execução com o parâmetro timeout_per_run em run_benchmarks()

---

## Licença

Projeto para fins acadêmicos e de estudo.
