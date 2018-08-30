#!/usr/bin/env python

################################################################
# Package: Rocket Monkey - Rocket.Chat API Extension and CLI
# Version: 0.0.3
# Author: Kirill Shtrykov <kirill@shtrykov.com>
# Website: https://shtrykov.com
################################################################

import os
import logging.handlers
from rocketchat_API.rocketchat import RocketChat


class RocketMonkey(RocketChat):
    """Extends Rocket.Chat Python API"""
    # Users
    def users_get_id(self, username):
        member_id = None
        for member in self.users_list().json().get('users'):
            if member['username'] == username:
                member_id = member['_id']
        return member_id

    def users_delete_by_name(self, username):
        user_id = self.users_get_id(username)
        return self.users_delete(user_id)

    # Channels
    def channels_get_id(self, channel_name):
        room_id = None
        for room in self.channels_list().json().get('channels'):
            if room['name'] == channel_name:
                room_id = room['_id']
        return room_id

    # Groups
    def groups_get_id(self, group_name):
        room_id = None
        for room in self.groups_list().json().get('groups'):
            if room['name'] == group_name:
                room_id = room['_id']
        return room_id
