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
import pytest


def test_absences():
    assert pytest.session.assenze() is not None


def test_class_reminders():
    assert pytest.session.promemoria() is not None


def test_class_schedule():
    assert pytest.session.orario() is not None


def test_disciplinary_notes():
    assert pytest.session.notedisciplinari() is not None


def test_daily_marks():
    assert pytest.session.votigiornalieri() is not None


def test_final_marks():
    assert pytest.session.votiscrutinio() is not None


def test_homework():
    assert pytest.session.compiti() is not None


def test_lesson_topics():
    assert pytest.session.votiscrutinio() is not None


def test_teachers():
    assert pytest.session.docenticlasse() is not None


def test_today_activities():
    assert pytest.session.oggi() is not None


def test_yesterday_activities():
    assert pytest.session.oggi((datetime.datetime.now() - datetime.timedelta(days=1)
                                ).strftime("%Y-%m-%d")) is not None