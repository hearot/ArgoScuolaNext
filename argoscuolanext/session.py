# This file is a part of ArgoScuolaNext Python API
#
# Copyright (c) 2019 The ArgoScuolaNext Python API Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import datetime
import re
import requests
import time

from json.decoder import JSONDecodeError
from typing import Any, Callable, Dict, Optional, Union

from .errors import AuthenticationFailedError, NotLoggedInError

_argo_key = "ax6542sdru3217t4eesd9"
"""
It represents the Argo Secret Key, used to make requests
to the REST API endpoint.
"""

_argo_version = "2.1.0"
"""
It represents the Argo REST API version.
"""

_app_code = "APF"
"""
The client code. Required since version 2.0.12
"""

_app_company = "ARGO Software s.r.l. - Ragusa"
"""
The company that developed the Argo REST API.
Required since version 2.0.12
"""

_rest_api_endpoint = "https://www.portaleargo.it/famiglia/api/rest/"
"""
It represents the REST API endpoint.
"""

_user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
"""
It represents the User Agent that is used to
send requests to the REST API endpoint.
"""

_version_regex = re.compile(r"([\d.])+")
"""
It represents the regex object that is being
used to get the new version of the APIs.
"""


class Session:
    """The object which represents a Student
    session on ArgoScuolaNext."""

    information: Dict[str, Any]
    """
    It contains the user's information,
    used to make requests to the REST
    API endpoint.
    """

    logged_in: bool = False
    """
    It represents if the user is
    logged in.
    """

    version: str
    """
    It represents which version of
    ArgoScuolaNext is being used.
    """

    def __init__(self, school_code: str, username: str, password: str, version: str = _argo_version):
        """
        Initialize the object and login the user.

        :param school_code: The ministerial school code
        :type school_code: str
        :param username: The user's username
        :type username: str
        :param password: The user's password
        :type password: str
        :param version: The version of the ArgoScuolaNext REST API
        :type version: str
        """
        global _argo_version

        login_request = requests.get(
            url=_rest_api_endpoint + "login",
            headers={
                "x-key-app": _argo_key,
                "x-version": version,
                "x-produttore-software": _app_company,
                "x-app-code": _app_code,
                "user-agent": _user_agent,
                "x-cod-min": school_code,
                "x-user-id": username,
                "x-pwd": password
            },
            params={
                "_dc": round(time.time() * 1000)
            }
        )

        if login_request.status_code != requests.codes.ok:
            try:
                version = _version_regex.search(login_request.json()['value']).group(0)
                self.information = Session(school_code, username, password, version).information
                _argo_version = version
            except (AttributeError, JSONDecodeError, KeyError):
                raise AuthenticationFailedError("Bad credentials or request.")
        else:
            self.information = self.get_information(school_code,
                                                    login_request.json()['token'],
                                                    version)[0]

        self.logged_in = True
        self.version = version

    def __call__(self, method: str, date: Optional[Union[datetime.datetime, str]] = None) \
            -> Dict[Any, Any]:
        """
        It calls an Argoscuolanext REST API method.

        :param method: The method you want to call.
        :type method: str
        :param date: The date you want to employ for the query.
        :type date: Optional[Union[datetime.datetime, str]]
        :return: The decode REST API response
        :rtype: Dict[Any, Any]
        """
        global _argo_version

        if not self.logged_in:
            raise NotLoggedInError("You must be logged in to use this method.")

        if date is None:
            date = datetime.datetime.now()

        if isinstance(date, datetime.datetime):
            date = date.strftime("%Y-%m-%d")

        request = requests.get(
            url=_rest_api_endpoint + method,
            headers={
                "x-key-app": _argo_key,
                "x-version": self.version,
                "user-agent": _user_agent,
                "x-produttore-software": _app_company,
                "x-app-code": _app_code,
                "x-auth-token": self.information['authToken'],
                "x-cod-min": self.information['codMin'],
                "x-prg-alunno": str(self.information['prgAlunno']),
                "x-prg-scheda": str(self.information['prgScheda']),
                "x-prg-scuola": str(self.information['prgScuola'])
            },
            params={
                "_dc": round(time.time() * 1000),
                "datGiorno": date
            }
        )

        if request.status_code != requests.codes.ok:
            try:
                self.version = _argo_version = _version_regex.search(request.json()['value']).group(0)
                return self(method, date)
            except (AttributeError, JSONDecodeError, KeyError):
                raise AuthenticationFailedError("Bad credentials or request.")

        return request.json()

    def __getattr__(self, method: str) -> Callable:
        """
        It returns the function used to call
        the method passed as argument.`.

        :param method: The method.
        :type method: str
        :return: The function used to call the method.
        :rtype: Callable
        """
        def call_method(date: Optional[datetime.datetime] = datetime.datetime.now().strftime("%Y-%m-%d")) \
                -> Dict[Any, Any]:
            """
            It represents the function that can be
            used to call an Argoscuolanext REST API
            method.

            :param date: The date you want to use during the call.
            :type date: datetime.datetime
            :return: The decode REST API response
            :rtype: Dict[Any, Any]
            """
            return self(method, date)

        return call_method

    @staticmethod
    def from_token(school_code: str, token: str, version: str = _argo_version) -> 'Session':
        """
        Create a session using a token and a school code.

        :param school_code: The ministerial school code
        :type school_code: str
        :param token: The ArgoScuolaNext REST API token
        :type token: str
        :param version: The version of the ArgoScuolaNext REST API
        :type version: str
        :return: A session that represents an already logged in user
        :rtype: Session
        """
        session = Session.__new__(Session)

        session.information = session.get_information(school_code, token)[0]
        session.logged_in = True
        session.version = version

        return session

    @staticmethod
    def get_information(school_code: str, token: str, version: str = _argo_version) -> Dict[Any, Any]:
        """
        It returns all the user's ArgoScuolaNext datas.

        :param school_code: The ministerial school code
        :type school_code: str
        :param token: The ArgoScuolaNext REST API token
        :type token: str
        :param version: The version of the ArgoScuolaNext REST API
        :type version: str
        :return: The user's information
        :rtype: Dict[Any, Any]
        """
        global _argo_version

        information_request = requests.get(
            url=_rest_api_endpoint + "schede",
            headers={
                "x-key-app": _argo_key,
                "x-version": version,
                "x-produttore-software": _app_company,
                "x-app-code": _app_code,
                "user-agent": _user_agent,
                "x-cod-min": school_code,
                "x-auth-token": token
            },
            params={
                "_dc": round(time.time() * 1000)
            }
        )

        if information_request.status_code != requests.codes.ok:
            try:
                _argo_version = _version_regex.search(information_request.json()['value']).group(0)
                return Session.get_information(school_code, token, version)
            except (AttributeError, JSONDecodeError, KeyError):
                raise AuthenticationFailedError("Bad credentials or request.")

        return information_request.json()

    @property
    def token(self) -> str:
        """
        Returns the user's token

        :return: The user's token
        :rtype: str
        """
        return self.information['authToken']
