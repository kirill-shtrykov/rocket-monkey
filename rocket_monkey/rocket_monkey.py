#!/usr/bin/env python

################################################################
# Package: Rocket Monkey - Rocket.Chat API Extension and CLI
# Version: 0.0.5
# Author: Kirill Shtrykov <kirill@shtrykov.com>
# Website: https://shtrykov.com
################################################################

from rocketchat_API.rocketchat import RocketChat


class RocketMonkey(RocketChat):
    """Extends Rocket.Chat Python API"""
    # Users
    def users_exists(self, username):
        """
        Check that user exists

        :param username: username
        :return: True if exists otherwise False
        """
        for member in self.users_list().json().get('users'):
            if member['username'] == username:
                return True
        return False

    def users_get_id(self, username):
        """
        Get user ID by name

        :param username: username
        :return: user ID or None
        """
        member_id = None
        for member in self.users_list().json().get('users'):
            if member['username'] == username:
                member_id = member['_id']
        return member_id

    def users_delete_by_name(self, username):
        """
        Delete user by username

        :param username: username
        :return: request result
        """
        user_id = self.users_get_id(username)
        return self.users_delete(user_id)

    # Channels
    def channels_get_id(self, channel_name):
        """
        Get channel ID by name

        :param channel_name: channel name
        :return: channel ID or None
        """
        room_id = None
        for room in self.channels_list().json().get('channels'):
            if room['name'] == channel_name:
                room_id = room['_id']
        return room_id

    # Groups
    def groups_get_id(self, group_name):
        """
        Get group ID by name

        :param group_name: group name
        :return: group ID or None
        """
        room_id = None
        for room in self.groups_list().json().get('groups'):
            if room['name'] == group_name:
                room_id = room['_id']
        return room_id
