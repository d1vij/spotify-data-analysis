from IPython.core.magic import Magics, magics_class, line_magic
from pathlib import Path
from IPython import get_ipython


@magics_class
class LoadNextMagics(Magics):
    """
    Custom magic command which reads and pastes the content of any file into the current notebook cell
    """

    @line_magic
    def loadnext(self, path):
        path = path.strip()
        text = Path(path).read_text(encoding="utf8")

        # Insert the file's content into the NEXT cell
        ip = get_ipython()
        ip.set_next_input(text, replace=True)

        return


ip = get_ipython()
ip.register_magics(LoadNextMagics)
