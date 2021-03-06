from typing import Optional

import click

from lean.click import LeanCommand
from lean.container import container


@click.command(cls=LeanCommand)
@click.option("--user-id", "-u", type=str, help="QuantConnect.com user id")
@click.option("--api-token", "-t", type=str, help="QuantConnect.com API token")
def login(user_id: Optional[str], api_token: Optional[str]) -> None:
    """Log in with a QuantConnect account.

    If user id or API token is not provided an interactive prompt will show.

    Credentials are stored in ~/.lean/credentials and are removed upon running `lean logout`.
    """
    logger = container.logger()
    credentials_storage = container.credentials_storage()

    if user_id is None or api_token is None:
        logger.info("Your user id and API token are needed to make authenticated requests to the QuantConnect API")
        logger.info("You can request these credentials on https://www.quantconnect.com/account")
        logger.info(f"Both will be saved in {credentials_storage.file}")

    if user_id is None:
        user_id = click.prompt("User id")

    if api_token is None:
        api_token = click.prompt("API token")

    api_client = container.api_client(user_id=user_id, api_token=api_token)
    if not api_client.is_authenticated():
        raise RuntimeError("Credentials are invalid")

    cli_config_manager = container.cli_config_manager()
    cli_config_manager.user_id.set_value(user_id)
    cli_config_manager.api_token.set_value(api_token)

    logger.info("Successfully logged in")
