# This file is a part of ArgoScuolaNext Python API
#
# Copyright (c) 2017 The ArgoScuolaNext Python API Authors (see AUTHORS)
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


import json
import re
import datetime
from json.decoder import JSONDecodeError
from urllib.parse import quote_plus
import time

import requests

from .utils import Utils
from .errors import AuthenticationFailedError, NotLoggedInError


class Session:
    """
    Main session object
    """
    rest_api_url = "https://www.portaleargo.it/famiglia/api/rest/"
    argo_key = "ax6542sdru3217t4eesd9"
    argo_version = "2.0.2"
    utils = Utils()

    def __init__(self):
        self.logged_in = False
        self.username = None
        self.password = None
        self.schoolCode = None
        self.token = None
    def login(self, schoolCode: str=None, username: str=None, password=None):
        """
        Login to ArgoScuolaNext
        :param schoolCode: Ministerial school code
        :param username: ArgoScuolaNext username
        :param password: ArgoScuolaNext password
        :type schoolCode: bool
        :type username: str
        :type password: str
        :return: Info about the user
        :rtype: dict
        """
        r = requests.get(
            url=self.rest_api_url + "login",
            headers={
                "x-key-app": self.argo_key,
                "x-version": self.argo_version,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                "x-cod-min": schoolCode,
                "x-user-id": username,
                "x-pwd": password
            },
            params={
                "_dc": round(time.time() * 1000)
            }
        )
        if r.status_code != requests.codes.ok:
            raise AuthenticationFailedError()
        result = json.loads(r.text)
        self.logged_in = True
        self.token = result['token']
        self.username = username
        self.password = password
        self.schoolCode = schoolCode
        j = requests.get(
            url=self.rest_api_url + "schede",
            headers={
                "x-key-app": self.argo_key,
                "x-version": self.argo_version,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                "x-cod-min": schoolCode,
                "x-auth-token": self.token
            },
            params={
                "_dc": round(time.time() * 1000)
            }
        )
        if j.status_code != requests.codes.ok:
            raise AuthenticationFailedError()
        jr = json.loads(j.text)
        for f, j in jr[0].items():
            setattr(self, f, j)
        return jr

    def logout(self):
        """
        Logout from ArgoScuolaNext
        :return: Always True
        :rtype: bool
        """
        self.logged_in = False
        self.username = None
        self.password = None
        self.token = None
        return True

    def _request(self, method=None, argu=datetime.datetime.now().strftime("%Y-%m-%d")):
        if not self.logged_in:
            raise NotLoggedInError()

        if argu is None:
            argu = datetime.datetime.now().strftime("%Y-%m-%d")
        url = self.rest_api_url + method
        r = requests.get(
            url=url,
            headers={
                "x-key-app": self.argo_key,
                "x-version": self.argo_version,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                "x-auth-token": self.token,
                "x-cod-min": self.schoolCode,
                "x-prg-alunno": self.prgAlunno,
                "x-prg-scheda": self.prgScheda,
                "x-prg-scuola": self.prgScuola
            },
            params={
                "_dc": round(time.time() * 1000),
                "datGiorno": argu
            }
        )

        if r.status_code != requests.codes.ok:
            raise AuthenticationFailedError()
        try:
            return json.loads(r.text)
        except JSONDecodeError:
            return r.text
    def assenze(self):
        """
        Get the student's absences
        :return: student's absences
        :rtype: dict
        """
        return self._request("assenze")
    def oggi(self, date=None):
        """
        Get what's happening today
        :return list of what's happening today
        :rtype: dict
        """
        return self._request("oggi", date)
    def notedisciplinari(self):
        """
        Get the student's annotations
        :return student's annotation
        :rtype: dict
        """
        return self._request("notedisciplinari")
    def votigiornalieri(self):
        """
        Get the student's marks
        :return student's marks
        :rtype dict
        """
        return self._request("votigiornalieri")
    def votiscrutinio(self):
        """
        Get the final student's marks
        :return final student's marks
        :rtype dict
        """
        return self._request("votiscrutinio")
    def compiti(self):
        """
        Get the student's homeworks
        :return student's homeworks
        :rtype dict
        """
        return self._request("compiti")
    def argomenti(self):
        """
        Get what a student has done
        :return what a student has done
        :rtype dict
        """
        return self._request("argomenti")
    def promemoria(self):
        """
        Get the student's notes
        :return student's notes
        :rtype dict
        """
        return self._request("promemoria")
    def orario(self):
        """
        Get the student's timetable
        :return student's timetable
        :rtype dict
        """
        return self._request("orario")
    def docenticlasse(self):
        """
        Get the student's teachers
        :return student's teachers
        :rtype dict
        """
        return self._request("docenticlasse")
