
class LoginService:
    """
    Serviço responsável pela lógica de autenticação.
    """

    def __init__(
        self,
        username=None,
        password=None,
        valid_username="admin",
        valid_password="123",
        submitted_value = None
    ):
        self.username = username
        self.password = password

        self.valid_username = valid_username
        self.valid_password = valid_password

        self.submitted_value = submitted_value

    def authenticate(self) -> bool:
        """
        Retorna True se as credenciais forem válidas.
        """
        return (
            self.username == self.valid_username and
            self.password == self.valid_password
        )
