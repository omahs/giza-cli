import copy
import json
import os
from pathlib import Path
from typing import Any, BinaryIO, Dict, Optional
from urllib.parse import urlparse

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from pydantic import SecretStr
from requests import Response, Session
from rich import print, print_json

from giza.schemas import users
from giza.schemas.token import TokenResponse
from giza.utils import echo
from giza.utils.decorators import auth

DEFAULT_API_VERSION = "v1"
GIZA_TOKEN_VARIABLE = "GIZA_TOKEN"


class ApiClient:
    """
    Implementation of the API client to interact with core-services
    """

    def __init__(
        self,
        host: str,
        token: Optional[str] = None,
        api_version: str = DEFAULT_API_VERSION,
        verify: bool = True,
        debug: Optional[bool] = False,
    ) -> None:
        self.session = Session()
        if host[-1] == "/":
            host = host[:-1]
        parsed_url = urlparse(host)

        self.url = f"{parsed_url.scheme}://{parsed_url.netloc}/api/{api_version}"

        if token is not None:
            headers = {"Authorization": "Bearer {token}", "Content-Type": "text/json"}
            self.token = token
        else:
            headers = {}

        self.debug = debug
        self.default_headers = {}
        self.default_headers.update(headers)
        self.verify = verify
        self.giza_dir = Path.home() / ".giza"
        self._default_credentials = self._load_credentials_file()

    def _echo_debug(self, message: str, json: bool = False) -> None:
        """
        Utility to log debug messages when debug is on

        Args:
            message (str): Message to print when debugging
            json (bool): indicates if the message is a json to treat it as such
        """

        if self.debug:
            print_json(message) if json else echo.debug(message)

    def _load_credentials_file(self) -> Dict:
        """
        Checks if the `~/.giza/.credentials.json` exists to retrieve existing credentials.
        Useful to reuse credentials that are still valid.

        Returns:
            Dict: if the file exists return the credentials from the file if not return an empty dict.
        """
        if (self.giza_dir / ".credentials.json").exists():
            with open(self.giza_dir / ".credentials.json") as f:
                credentials = json.load(f)
                self._echo_debug(
                    f"Credentials loaded from: {self.giza_dir / '.credentials.json'}",
                )
        else:
            credentials = {}
            self._echo_debug("Credentials not found in default directory")

        return credentials

    def _get_oauth(self, user: str, password: str) -> None:
        """
        Retrieve JWT token.

        Args:
            user (str): username used to retrieve the token
            password (str): password to authenticate agains the login endpoint

        Raises:
            json.JSONDecodeError: when the response does not have the expected body
        """

        user_login = users.UserLogin(username=user, password=SecretStr(password))
        response = self.session.post(
            f"{self.url}/login/access-token",
            data={
                "username": user_login.username,
                "password": user_login.password.get_secret_value(),
            },
        )
        response.raise_for_status()
        try:
            token = TokenResponse(**response.json())
        except json.JSONDecodeError:
            # TODO: if response is succesfull (2XX) do we need this?
            print(response.text)
            print(f"Status Code -> {response.status_code}")
            raise

        self.token = token.access_token
        self._echo_debug(response.json(), json=True)
        self._echo_debug(f"Token: {self.token}")

    def _write_credentials(self, **kwargs: Any) -> None:
        """
        Write credentials to the giza credentials file for later retrieval

        Args:
            kwargs(dict): extra keyword arguments to save with the credentials, usually `user`.
        """
        if self.token is not None:
            if not self.giza_dir.exists():
                echo("Creating default giza dir")
                self.giza_dir.mkdir()
            kwargs.update({"token": self.token})
            with open(self.giza_dir / ".credentials.json", "w") as f:
                json.dump(kwargs, f, indent=4)
            echo(f"Credentials written to: {self.giza_dir / '.credentials.json'}")

    def _is_expired(self, token: str) -> bool:
        """
        Check if the token is expired.

        Args:
            token (str): token to check expiry

        Returns:
            bool: if the token has expired
        """
        try:
            jwt.decode(
                token,
                "",
                algorithms=["HS256"],
                options={"verify_signature": False},
            )
            return False
        except ExpiredSignatureError:
            self._echo_debug("Token is expired")
            return True

    def retrieve_token(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        renew: bool = False,
    ) -> None:
        """
        Get the JWT token.

        First,  it will try to get it from GIZA_TOKEN.
        Second, from ~/.giza/.credentials.json.
        And finally it will try to retrieve it from the API login the user in.

        Args:
            user: if provided it will be used to check against current credentials
                  and if provided with `password` used to retrieve a new token.
            password: if provided with `user` it will be used to retrieve a new token.
            renew: for renewal of the JWT token by user login.

        Raises:
            Exception: if token could not be retrieved in any way
        """

        token = os.environ.get(GIZA_TOKEN_VARIABLE)
        if token is None:
            self._echo_debug(
                f"No token found in environment variable {GIZA_TOKEN_VARIABLE}",
            )
        if token is None and len(self._default_credentials) != 0 and not renew:
            # Try with the home folder
            if "token" in self._default_credentials:
                token = self._default_credentials.get("token")
                user_cred = self._default_credentials.get("user")

                # Different users but credentials file exists make sure we ask for the new JWT
                if user is not None and user != user_cred:
                    self._echo_debug(
                        "Logging as a different user, need to retrieve a new token",
                    )
                    token = None

        if token is not None and not self._is_expired(token) and not renew:
            self.token = token
            echo("Token is still valid, re-using it from ~/.giza")

        if (
            getattr(self, "token", None) is None
            and user is not None
            and password is not None
        ):
            self._get_oauth(user, password)
            self._write_credentials(user=user)

        if getattr(self, "token", None) is None:
            raise Exception(
                "Token is expired or could not retrieve it. "
                "Please get a new one using `user` and `password`.",
            )


class UsersClient(ApiClient):
    """
    Client to interact with `users` endpoint.
    """

    USERS_ENDPOINT = "users"

    def create(self, user: users.UserCreate) -> users.UserResponse:
        """
        Call the API to create a new user

        Args:
            user (users.UserCreate): information used to create a new user

        Returns:
            users.UserResponse: the created user information
        """
        response = self.session.post(
            f"{self.url}/{self.USERS_ENDPOINT}/",
            json=user.dict(exclude_unset=True),
        )

        response.raise_for_status()
        body = response.json()
        self._echo_debug(body, json=True)
        return users.UserResponse(**body)

    @auth
    def me(self) -> users.UserResponse:
        """
        Retrieve information about the current user.
        Must have a valid token to perform the operation, enforced by `@auth`

        Returns:
            users.UserResponse: User information from the server
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(
            {"Authorization": f"Bearer {self.token}", "Content-Type": "text/json"},
        )
        response = self.session.get(
            f"{self.url}/{self.USERS_ENDPOINT}/me",
            headers=headers,
        )
        self._echo_debug(response.json(), json=True)
        return users.UserResponse(**response.json())


class TranspileClient(ApiClient):
    """
    Client to interact with `users` endpoint.
    """

    TRANSPILE_ENDPOINT = "transpile"

    @auth
    def transpile(self, f: BinaryIO) -> Response:
        """
        Make a call to the API transpile endpoint with the model as a file.

        Args:
            f (BinaryIO): model to send for transpilation

        Returns:
            Response: raw response from the server with the transpiled model as a zip
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(
            {"Authorization": f"Bearer {self.token}"},
        )
        response = self.session.post(
            f"{self.url}/{self.TRANSPILE_ENDPOINT}",
            files={"file": f},
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()
        return response