from datetime import datetime, timedelta
from functools import wraps
from typing import List

import requests
from bs4 import BeautifulSoup
from requests import Session, Response

from api import Urls
from api.exceptions import TokenNotFoundException, DataNotFoundException


class Api:
    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password
        print(username, password)
        self.token: str or None = None
        self.headers: dict = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
        }

        self.teams = {
            "P4D": "2841",
            "P3H": "2842",
            "P1D": "2728",
            "P2H": "2974"
        }

        self.session: Session = Session()

        self.last_auth_time: datetime = datetime.now()
        self.session_time = timedelta(days=5)
        self.authenticate()

    # Authentication
    def authenticate(self) -> None:
        """
        Used to update cookies following authentication.
        :return:
        """

        print("call")

        url: str = Urls.login_url()

        response: Response = self.session.get(url)

        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        try:
            token: str = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        except (TypeError, KeyError):
            raise TokenNotFoundException()

        self.token: str = token

        login_payload: dict = {
            'UserName': self.username,
            'Password': self.password,
            'RememberMe': False,
            '__RequestVerificationToken': token
        }

        self.session.post(url, data=login_payload, allow_redirects=False)

    def set_token(self, url: str, session=None) -> None:
        """
        Used to update cookies (the token) before making a request to the portal.
        :param session:
        :param url:
        :return:
        """
        if not session:
            response: Response = self.session.get(url)
        else:
            response: Response = session.get(url)

        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        try:
            token: str = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        except (TypeError, KeyError):
            raise TokenNotFoundException()

        self.token: str = token
        self.session.cookies.set("__RequestVerificationToken", token)

    def check_token_expiry(self) -> None:
        """
        Checks if the token has expired (more than 5 days since last authentication),
        and re-authenticates if necessary.
        """
        if (datetime.now() - self.last_auth_time) > self.session_time:
            self.authenticate()

    @staticmethod
    def token_refresh_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.check_token_expiry()
            return func(self, *args, **kwargs)

        return wrapper

    # Api methods
    @token_refresh_required
    def get_member(self, member_id: int) -> dict:
        """
        Get a specific member by member_id.
        :param member_id:
        :return:
        """

        self.set_token(Urls.member_token_url(member_id))

        response: Response = self.session.post(Urls.member_url(member_id), data={
            "sort": "",
            "group": "",
            "filter": "",
            "currentOnly": False
        }, headers=self.headers)

        data: dict = response.json().get('Data')

        if not data:
            raise DataNotFoundException()

        return data[0]

    @token_refresh_required
    def get_members(self) -> List[dict]:
        """
        Get all members.
        :return:
        """

        url: str = Urls.members_url()
        response: Response = self.session.post(
            url,
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "currentOnly": False
            },
            headers=self.headers
        )

        data: List[dict] = response.json().get('Data')

        if not data:
            raise DataNotFoundException()

        return data

    @token_refresh_required
    def get_affiliates(self) -> List[dict]:
        """
        Get all club members with more details.
        :return:
        """

        self.set_token(Urls.affiliates_token_url())
        response: Response = self.session.post(
            Urls.affiliates_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "searchTerm": "",
                "currentOnly": True
            },
            headers=self.headers
        )

        data: List[dict] = response.json().get('Data')

        if not data:
            raise DataNotFoundException()

        return data

    @token_refresh_required
    def get_calendar(self, team: str = None):
        session = requests.Session()
        session.cookies.set("SelectedSeasonId", "1906")
        session.cookies.set("PortailSelectedSeasonId", "1982")
        self.set_token(Urls.calendar_token_url(), session=session)
        response: Response = session.post(
            Urls.calendar_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "searchTerm": "",
                "districtId": "3",
                "championshipId": self.teams[team] if team else None,
                "clubId": "1673",

                "teamId": "0" if team else None,
                "dateFrom": "-1",
                "dateTo": "-1"
            },
            headers=self.headers
        )

        return response.json()
        # print(response.json())
        # data: List[dict] = response.json().get('Data')
        #
        # if not data:
        #     raise DataNotFoundException()
        #
        # return data
