import chalk


class Printer:
    """Utility class for printing styled terminal output using pychalk."""

    @staticmethod
    def _join(*args):
        return " ".join(map(str, args))

    @staticmethod
    def red(*args):
        print(chalk.red(Printer._join(*args)))

    @staticmethod
    def green(*args):
        print(chalk.green(Printer._join(*args)))

    @staticmethod
    def yellow(*args):
        print(chalk.yellow(Printer._join(*args)))

    @staticmethod
    def blue(*args):
        print(chalk.blue(Printer._join(*args)))

    @staticmethod
    def magenta(*args):
        print(chalk.magenta(Printer._join(*args)))

    @staticmethod
    def cyan(*args):
        print(chalk.cyan(Printer._join(*args)))

    @staticmethod
    def white(*args):
        print(chalk.white(Printer._join(*args)))

    @staticmethod
    def red_bold(*args):
        print(chalk.bold(chalk.red(Printer._join(*args))))

    @staticmethod
    def green_bold(*args):
        print(chalk.bold(chalk.green(Printer._join(*args))))

    @staticmethod
    def yellow_bold(*args):
        print(chalk.bold(chalk.yellow(Printer._join(*args))))

    @staticmethod
    def blue_bold(*args):
        print(chalk.bold(chalk.blue(Printer._join(*args))))

    @staticmethod
    def red_underline(*args):
        print(chalk.underline(chalk.red(Printer._join(*args))))

    @staticmethod
    def green_underline(*args):
        print(chalk.underline(chalk.green(Printer._join(*args))))

    @staticmethod
    def yellow_underline(*args):
        print(chalk.underline(chalk.yellow(Printer._join(*args))))

    @staticmethod
    def blue_underline(*args):
        print(chalk.underline(chalk.blue(Printer._join(*args))))

    @staticmethod
    def cyan_underline(*args):
        print(chalk.underline(chalk.cyan(Printer._join(*args))))

    @staticmethod
    def magenta_underline(*args):
        print(chalk.underline(chalk.magenta(Printer._join(*args))))
