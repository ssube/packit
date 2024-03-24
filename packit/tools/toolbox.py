from .utils import prepare_tools


class Toolbox:
    """
    Container for the paired dict and list needed to manage tools.
    """

    callbacks: dict[str, callable]
    definitions: list[dict]

    def __init__(self, tools: list[callable]):
        """
        Initialize the toolbox with a list of tools.
        """
        self.definitions, self.callbacks = prepare_tools(tools)
