<!-- markdownlint-disable -->

# API Overview

## Modules

- [`callbacks`](./callbacks.md#module-callbacks)
- [`cli`](./cli.md#module-cli)
- [`client`](./client.md#module-client)
- [`commands`](./commands.md#module-commands)
- [`commands.models`](./commands.models.md#module-commandsmodels)
- [`commands.prove`](./commands.prove.md#module-commandsprove)
- [`commands.reset_password`](./commands.reset_password.md#module-commandsreset_password)
- [`commands.users`](./commands.users.md#module-commandsusers)
- [`commands.version`](./commands.version.md#module-commandsversion)
- [`commands.versions`](./commands.versions.md#module-commandsversions)
- [`exceptions`](./exceptions.md#module-exceptions)
- [`options`](./options.md#module-options)
- [`utils`](./utils.md#module-utils)
- [`utils.decorators`](./utils.decorators.md#module-utilsdecorators)
- [`utils.echo`](./utils.echo.md#module-utilsecho)
- [`utils.enums`](./utils.enums.md#module-utilsenums)
- [`utils.misc`](./utils.misc.md#module-utilsmisc)

## Classes

- [`client.ApiClient`](./client.md#class-apiclient): Implementation of the API client to interact with core-services
- [`client.JobsClient`](./client.md#class-jobsclient): Client to interact with `jobs` endpoint.
- [`client.ModelsClient`](./client.md#class-modelsclient): Client to interact with `models` endpoint.
- [`client.ProofsClient`](./client.md#class-proofsclient): Client to interact with `proofs` endpoint.
- [`client.TranspileClient`](./client.md#class-transpileclient): Client to interact with `users` endpoint.
- [`client.UsersClient`](./client.md#class-usersclient): Client to interact with `users` endpoint.
- [`client.VersionsClient`](./client.md#class-versionsclient): Client to interact with `versions` endpoint.
- [`exceptions.PasswordError`](./exceptions.md#class-passworderror)
- [`echo.Echo`](./utils.echo.md#class-echo): Helper class to use when printin output of the CLI.
- [`enums.JobSize`](./utils.enums.md#class-jobsize)
- [`enums.JobStatus`](./utils.enums.md#class-jobstatus)
- [`enums.VersionStatus`](./utils.enums.md#class-versionstatus)

## Functions

- [`callbacks.debug_callback`](./callbacks.md#function-debug_callback): If a call adds the `--debug` flag debugging mode is activated for external requests and API Clients.
- [`callbacks.version_callback`](./callbacks.md#function-version_callback): Prints the current version when `--version` flag is added to a call.
- [`cli.entrypoint`](./cli.md#function-entrypoint)
- [`models.get`](./commands.models.md#function-get): Command to create a user. Asks for the new users information and validates the input,
- [`models.list`](./commands.models.md#function-list): Command to list all models.
- [`prove.prove`](./commands.prove.md#function-prove): Command to prove as spceific cairo program, previously converted to CASM.
- [`reset_password.handle_http_error`](./commands.reset_password.md#function-handle_http_error): Handle an HTTP error.
- [`reset_password.prompt_for_input`](./commands.reset_password.md#function-prompt_for_input): Prompt the user for input.
- [`reset_password.request_reset_password_token`](./commands.reset_password.md#function-request_reset_password_token): Request a password reset token for a given email.
- [`reset_password.reset_password`](./commands.reset_password.md#function-reset_password): Reset the password for a user using a reset token.
- [`users.create`](./commands.users.md#function-create): Command to create a user. Asks for the new users information and validates the input,
- [`users.login`](./commands.users.md#function-login): Logs the current user into Giza. Under the hood this will retrieve the token for the next requests.
- [`users.me`](./commands.users.md#function-me): Retrieve information about the current user and print it as json to stdout.
- [`users.resend_email`](./commands.users.md#function-resend_email): Command to resend verification email. Asks for the user's email and sends the request to the API
- [`version.version_entrypoint`](./commands.version.md#function-version_entrypoint): Prints the current CLI version.
- [`versions.download`](./commands.versions.md#function-download): Retrieve information about the current user and print it as json to stdout.
- [`versions.get`](./commands.versions.md#function-get)
- [`versions.list`](./commands.versions.md#function-list)
- [`versions.transpile`](./commands.versions.md#function-transpile): This function is responsible for transpiling a model. The overall objective is to prepare a model for use by converting it into a different format (transpiling).
- [`versions.update`](./commands.versions.md#function-update)
- [`utils.get_response_info`](./utils.md#function-get_response_info): Utility to retrieve information of the client response.
- [`decorators.auth`](./utils.decorators.md#function-auth): Check that we have the token and it is not expired before executing
