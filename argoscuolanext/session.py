# This file is a part of ArgoScuolaNext Python API
#
# Copyright (c) 2018 The ArgoScuolaNext Python API Authors (see AUTHORS)
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
import time
from typing import Any, Callable, Dict, Optional

import requests

from .errors import AuthenticationFailedError, NotLoggedInError

_argo_key = "ax6542sdru3217t4eesd9"
"""
It represents the Argo Secret Key, used to make requests
to the REST API endpoint.
"""

_argo_version = "2.0.2"
"""
It represents the Argo REST API version.
"""

_rest_api_endpoint = "https://www.portaleargo.it/famiglia/api/rest/"
"""
It represents the REST API endpoint.
"""

_user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
"""
It represents the User Agent that is used to send requests to the
REST API endpoint.
"""


class Session:
    """
    Main session object
    """

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

    def __init__(self, school_code: str, username: str, password: str):
        """
        Initialize the object and login the user.

        :param school_code: Ministerial school code
        :type school_code: str
        :param username: The user's username
        :type username: str
        :param password: The user's password
        :type password: str
        """

        # Login request
        login_request = requests.get(
            url=_rest_api_endpoint + "login",
            headers={
                "x-key-app": _argo_key,
                "x-version": _argo_version,
                "user-agent": _user_agent,
                "x-cod-min": school_code,
                "x-user-id": username,
                "x-pwd": password
            },
            params={
                "_dc": round(time.time() * 1000)
            }
        )

        # Error checking & handling
        if login_request.status_code != requests.codes.ok:
            raise AuthenticationFailedError("Bad credentials or request.")

        result = login_request.json()  # Decode the JSON result

        self.logged_in, token = True, result['token']

        # Get the information about the user
        information_request = requests.get(
            url=_rest_api_endpoint + "schede",
            headers={
                "x-key-app": _argo_key,
                "x-version": _argo_version,
                "user-agent": _user_agent,
                "x-cod-min": school_code,
                "x-auth-token": token
            },
            params={
                "_dc": round(time.time() * 1000)
            }
        )

        # Error checking & handling
        if information_request.status_code != requests.codes.ok:
            raise AuthenticationFailedError("Bad credentials or request.")

        information = information_request.json()  # Decode the JSON result
        self.information = information[0]  # Get the user's information

    def __call__(self, method: str, date: Optional[datetime.datetime] = datetime.datetime.now().strftime("%Y-%m-%d")) \
            -> Dict[Any, Any]:
        """
        It calls an Argoscuolanext REST API method.

        :param method: The method you want to call.
        :type method: str
        :param date: The date you want to use during the call.
        :type date: datetime.datetime
        :return: The decode REST API response
        :rtype: Dict[Any, Any]
        """

        # Check that the user is logged in
        if not self.logged_in:
            raise NotLoggedInError("You must be logged in to use this method.")

        # Check if the date is defined and if not define it.
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")

        request = requests.get(
            url=_rest_api_endpoint + method,
            headers={
                "x-key-app": _argo_key,
                "x-version": _argo_version,
                "user-agent": _user_agent,
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

        # Error checking & handling
        if request.status_code != requests.codes.ok:
            raise AuthenticationFailedError("Bad credentials or request.")

        return request.json()  # Return the decoded response

    def __getattr__(self, method: str) -> Callable:
        """
        It returns the function used to call
        the method passed as argument.`.

        :param method: The method.
        :type method: str
        :return: The function used to call the method.
        :rtype: Callable
        """

        # Create the function used to call the method
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
            return self.__call__(method, date)

        return call_method  # Return the function
