import os
import re
import sys
import configparser
import argparse
from getpass import getpass
from rocket_monkey import RocketMonkey


def get_custom(arg):
    if arg.startswith('--custom-'):
        arg = arg[9:]
    return arg


parser = argparse.ArgumentParser(description='Rocket Monkey - Rocket.Chat CLI Manager')
targets = parser.add_subparsers(help='target', dest='target')
# Auth
parser.add_argument("-d", "--domain",
                    help='Rocket.Chat domain name')
parser.add_argument("-u", "--user",
                    help="Rocket.Chat username")
parser.add_argument("-p", "--password",
                    help="Rocket.Chat users password")
parser.add_argument("--debug",
                    action='store_true',
                    help="enable debug mode")
# Users
parser_user = targets.add_parser("user",
                                 help="manage users")
user_commands = parser_user.add_subparsers(help='command', dest='command')
# # Create
user_create = user_commands.add_parser("create",
                                       help='create user')
user_create.add_argument("email",
                         help="email")
user_create.add_argument("name",
                         help="full name")
user_create.add_argument("init_pass",
                         help="password")
user_create.add_argument("username",
                         help="username")
user_create.add_argument("--role",
                         nargs='*',
                         help="role")
# # Delete
user_delete = user_commands.add_parser("delete",
                                       help='delete user')
user_delete.add_argument("username",
                         help="username")
# # Set Avatar
user_set_avatar = user_commands.add_parser("set-avatar",
                                           help='set user\'s avatar')
user_set_avatar.add_argument("username",
                             help="username")
user_set_avatar.add_argument('url',
                             help='URL to avatar')
# Channels
parser_channel = targets.add_parser("channel",
                                    help="manage channels")
channel_commands = parser_channel.add_subparsers(help='command', dest='command')
# # Create
channel_create = channel_commands.add_parser("create",
                                             help='create channel')
channel_create.add_argument("name",
                            help="channel name")
channel_create.add_argument("--members",
                            help="add members to created room")
channel_create.add_argument("--read-only",
                            action='store_true',
                            help='make room readonly')
# # Delete
channel_delete = channel_commands.add_parser("delete",
                                             help='delete channel')
channel_delete.add_argument("name",
                            help="channel name")


def main():
    config_file = os.path.expanduser('~/.rocket-monkey')
    args, extras = parser.parse_known_args()
    config = configparser.ConfigParser()
    domain = None
    user = None
    password = None

    if os.path.isfile(config_file):
        config.read(config_file)
        if 'rocket-monkey' in config.sections():
            domain = config.get('rocket-monkey', 'domain')
            user = config.get('rocket-monkey', 'user')
            password = config.get('rocket-monkey', 'password')

    if hasattr(args, 'domain'):
        domain = getattr(args, 'domain')

    if hasattr(args, 'user'):
        user = getattr(args, 'user')

    if hasattr(args, 'password'):
        password = getattr(args, 'password')
        print(
            "Warning: Using a password on the command line interface can be insecure. But I'am only monkey.")

    if not domain:
        domain = 'localhost'
    if not user:
        user = os.getlogin()
    if not password:
        if sys.stdin.isatty():
            password = getpass('Password: ')
        else:
            print('Password: ')
            password = sys.stdin.readline().rstrip()

    if not re.match('^https?://', domain):
        url = "https://%s" % domain
    else:
        url = domain

    api = RocketMonkey(user=user, password=password, server_url=url)

    if args.target == 'user':
        if args.command == 'create':
            custom_fields = {get_custom(k): v for k, v in zip(extras[::2], extras[1::2])}
            role = getattr(args, 'role', []) or []
            role += ['user']
            print(api.users_create(
                args.email,
                args.name,
                args.init_pass,
                args.username,
                role=role,
                custom_fields=custom_fields
            ).json())
        elif args.command == 'delete':
            print(api.users_delete_by_name(args.username).json())
        elif args.command == 'set-avatar':
            print(api.users_set_avatar(args.url, username=args.username).json())
    elif args.target == 'channel':
        if args.command == 'create':
            members = getattr(args, 'members', []) or []
            members += ['rocket.cat']
            print(api.channels_create(args.name, members=members, read_only=args.read_only).json())
        elif args.command == 'delete':
            print(api.channels_delete(channel=args.name).json())
