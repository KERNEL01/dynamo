from client.client import DynamoClient
from persistence import constants
from tests.preflight import preflight


def main():
    # conduct our runtime checks
    preflight()
    
    # run the client
    client = DynamoClient()
    client.run(constants.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
