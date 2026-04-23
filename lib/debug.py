class Debug:
    @staticmethod
    def print_timed(message, elapsed, width=60):
        """Imprime el mensaje con el tiempo coloreado según el valor."""
        # ANSI colors: green, yellow, red
        if elapsed < 0.5:
            color = "\033[92m"  # green
        elif elapsed < 1.0:
            color = "\033[93m"  # yellow
        else:
            color = "\033[91m"  # red
        reset = "\033[0m"
        print(f"{message:<{width}}: {color}{elapsed:.2f} segundos{reset}")

    @staticmethod
    def time(callback, message=None):
        """
        Ejecuta un callback sin argumentos (tipo VoidCallback), mide su tiempo de ejecución
        y muestra el resultado usando print_timed.
        """
        import time
        start = time.time()
        callback()
        elapsed = time.time() - start
        Debug.print_timed(message or callback.__name__, elapsed)