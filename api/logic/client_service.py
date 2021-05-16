
from api.service.service import ClientService
from api.database import DatabaseOperations
from api.input_valdiation import validate_input_data


class ClientServiceImplementation(ClientService):

    def __init__(self, model=None):
        self._database_operations = DatabaseOperations(model=model)

    @validate_input_data("id", "name", "image")
    def create(self, **new_client_body_request):
        """
        Creates a new client and inserts it into the DB.

        Keyword Arguments:
            id (int): client account.
            name (str): client's name.
        """
        #  TODO - need to fix a bug where adding automatically id to each client does not work.
        self._database_operations.insert(**new_client_body_request)
        client_model = self._database_operations.model

        return {"id": client_model.id, "name": client_model.name, "image": client_model.image}

    def get_one(self, client_id):
        """
        Gets the client by ID from the DB.

        Args:
            client_id (str): client ID.
        """
        client_model = self._database_operations.get(primary_key_value=client_id, resource_type="Client")
        return {"id": client_model.id, "name": client_model.name, "image": client_model.image}

    def get_many(self):
        """
        Gets all the available clients from the DB.
        """
        response = []

        all_clients = self._database_operations.get_all()
        for client in all_clients:
            response.append({"name": client.name, "image": client.image})

        return response
