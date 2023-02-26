
class Person:
    """
    håller name, socket client och IP address
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        """
        sätter namnet på personen
        :param name: str
        :return: inget
        """
        self.name = name

    def __repr__(self):
        return f"Person({self.addr}, {self.name})"