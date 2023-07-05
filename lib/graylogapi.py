#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Philipp Fromme
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import requests
import json
import sys
import logging

if sys.version_info < (3, 0):
    raise ImportError("This library does not work with python2")

class GraylogApi:
    def __init__(self, api_token, url='http://127.0.0.1:9000/api/'):
        self.url = url
        self.api_token = api_token
        self.api_token_password = 'token'
        self.headers = {'Content-Type': 'application/json', 'X-Requested-By': 'cli'}
        self.logger = logging.getLogger("graylogapi")
        self.logger.setLevel(logging.WARNING)

    def get_request(self, operation):
        request_url = urllib.parse.urljoin(self.url, operation)
        response = requests.get(request_url, headers=self.headers, auth=(self.api_token, self.api_token_password))
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    def post_request(self):
        pass

    def put_request(self, operation, data):
        request_url = urllib.parse.urljoin(self.url, operation)
        response = requests.put(request_url, json=data, headers=self.headers, auth=(self.api_token, self.api_token_password))
        return response.status_code

    def del_request(self, operation):
        request_url = urllib.parse.urljoin(self.url, operation)
        reponse = requests.delete(request_url, headers=self.headers, auth=(self.api_token, self.api_token_password))
        return response.status_code

    def get_streams(self):
        return self.get_request('streams')['streams']

    def delete_users_id(self, user_id):
        status_code = self.del_request('users/id/{}'.format(user_id))
        if status_code == 400:
            return False
        else:
            return True

    def get_users(self):
        return self.get_request('users')

    def get_users_username(self, username):
        return self.get_request('users/{}'.format(username))

    def put_users_permissions(self, username, permissions):
        json_data = {"permissions": permissions}
        status_code = self.put_request('users/{}/permissions'.format(username), json_data)
        if status_code == 400:
            return False
        else:
            return True
