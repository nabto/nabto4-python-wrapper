import argparse
import os
from cmd import Cmd
from time import sleep

import nabto_client
from example import NabtoDevice

# /home/../python-nabto-client/example
PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NABTO_HOME_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'share', 'nabto')
NABTO_QUERIES = os.path.join(PARENT_DIRECTORY, 'unabto_queries.xml')


class NabtoCmd(Cmd):
    prompt = 'nabto> '
    intro = 'Type ? to list commands'

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.user = None
        self.password = None

    def emptyline(self):
        pass

    def do_exit(self, args):
        """
        Exiting the CLI
        """
        print("Bye")
        return True

    def do_create_profile(self, args):
        """
        E.g. > create_profile user pass
        """
        user, password = args.split()
        nabto_client.createSelfSignedProfile(user, password)

    def do_get_fingerprint(self, user):
        """
        E.g. > get_fingerprint user
        """
        print(nabto_client.getFingerprint(user))

    def do_create_session(self, args):
        """
        E.g. > create_session user pass
        """
        user, password = args.split()
        with nabto_client.NabtoSession(user, password) as session:
            print('Session opened. Sleep for 5 seconds')
            sleep(5)

        self.user = user
        self.password = password

    def do_open_tunnel(self, remote_port):
        """
        E.g. > open_tunnel 8090
        """
        if not self.user:
            print('You must call `create_session` first')
            return

        with nabto_client.NabtoSession(self.user, self.password) as session:
            with open(NABTO_QUERIES) as file:
                session.RpcSetDefaultInterface(file.read())

            with nabto_client.NabtoTunnel(session, 0, self.device_name, 'localhost', int(remote_port)) as port:
                print(f'Opened tunnel on port {port}. Sleep for 30 seconds.')
                sleep(30)

    def do_add_user(self, args):
        """
        E.g. > add_user guest 34e0834b008f0ee3748de75ecee71802
        """
        user, fingerprint = args.split()
        if not self.user:
            print('You must call `create_session` first')
            return

        with nabto_client.NabtoSession(self.user, self.password) as session:
            with open(NABTO_QUERIES) as file:
                session.RpcSetDefaultInterface(file.read())
                dev = NabtoDevice(self.device_name, session)
                print(dev.addUser(user, fingerprint))

    def do_get_users(self, args):
        """
        E.g. > get_users
        """
        if not self.user:
            print('You must call `create_session` first')
            return

        with nabto_client.NabtoSession(self.user, self.password) as session:
            with open(NABTO_QUERIES) as file:
                session.RpcSetDefaultInterface(file.read())
                dev = NabtoDevice(self.device_name, session)
                print(dev.getUsers())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, required=True, help='Remote host')
    parser.add_argument('--home-dir', type=str, dest='home_dir', default=NABTO_HOME_DIRECTORY, help='Nabto home directory')
    args = parser.parse_args()
    print(f'Device: {args.device}')
    print(f'Nabto home directory: {args.home_dir}')

    nabto_client.startup(args.home_dir)
    NabtoCmd(args.device).cmdloop()
    nabto_client.shutdown()
