class Debug:
    def print_timed(message, elapsed):
        """Imprime el mensaje con el tiempo coloreado según el valor."""
        # ANSI colors: green, yellow, red
        if elapsed < 0.5:
            color = "\033[92m"  # green
        elif elapsed < 1.0:
            color = "\033[93m"  # yellow
        else:
            color = "\033[91m"  # red
        reset = "\033[0m"
        # Ancho fijo para el mensaje, alineado a la izquierda (como setw en C++)
        width = 60
        print(f"{message:<{width}}: {color}{elapsed:.2f} segundos{reset}")
