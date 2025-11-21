class ReportGenerator:
    """
    Gera relatório interpretável da análise empírica.
    """

    def __init__(self, time_analysis: dict, mem_analysis: dict):
        self.time = time_analysis
        self.mem = mem_analysis

    def generate_text_report(self):
        lines = []
        lines.append("=" * 60)
        lines.append(" RELATÓRIO DE COMPLEXIDADE EMPÍRICA ")
        lines.append("=" * 60)

        lines.append("\nCOMPLEXIDADE TEMPORAL:")
        lines.append("-" * 40)
        for algo, data in self.time.items():
            lines.append(
                f"{algo:20} | {data['complexidade_estimada']:25} | "
                f"Tempo médio: {data['tempo_medio']:.4f}s"
            )

        lines.append("\nCOMPLEXIDADE DE MEMÓRIA:")
        lines.append("-" * 40)
        for algo, data in self.mem.items():
            lines.append(
                f"{algo:20} | {data['complexidade_memoria']:25} | "
                f"Memória média: {data['memoria_media_mb']:.2f} MB"
            )

        return "\n".join(lines)

    def print_report(self):
        print(self.generate_text_report())
