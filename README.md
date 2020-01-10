# python-nabto-client

Python Wrapper for Nabto Client

## Requirements

* Python 3.6+
* `python3-dev` package for Debian distributions

## Installation

Install using `pip`...

    pip install -i https://test.pypi.org/simple/ nabto-client

## Example

Let's take a look at a quick example of using `nabto_client` to open a session and a tunnel.

    import nabto_client
    
    NABTO_HOME_DIRECTORY = "/home/nabto/example"

    USER = "user"
    PASSWORD = "password"
    
    LOCAL_PORT = 7000
    NABTO_HOST = "example.appmyproduct.com"
    REMOTE_HOST = "localhost"
    REMOTE_PORT = 8000

    # Initializes the Nabto client API
    nabto_client.startup(NABTO_HOME_DIRECTORY)
    
    # Creates a Nabto self signed profile
    nabto_client.createSelfSignedProfile(USER, PASSWORD)
    
    with nabto_client.NabtoSession(USER, PASSWORD) as session:
        with nabto_client.NabtoTunnel(session, LOCAL_PORT, NABTO_HOST, REMOTE_HOST, REMOTE_PORT) as port:
            print(f'Opened tunnel on port {port}')
            ...
            
    # Releases any resources held by the Nabto client API
    nabto_client.shutdown()

You can also run `example/cli.py` for an interactive example.

    python example/cli.py --device example.appmyproduct.com
