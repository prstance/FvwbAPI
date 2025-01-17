from datetime import datetime, timedelta
from functools import wraps
from typing import List

import requests
from bs4 import BeautifulSoup
from requests import Session, Response

from api import Urls
from api.exceptions import TokenNotFoundException


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

        self.club_id = 1673
        self.district_id = 3
        self.season_id = 1982  # PortailSelectedSeasonId
        self.season_id_ = 1906  # SelectedSeasonId
        self.teams = {
            "calendar": {
                "P4D": "2841",
                "P3H": "2842",
                "P1D": "2728",
                "P2H": "2974"
            },
            # "ranking": {
            #     "P4D": "2556",
            #     "P3H": "2557",
            #     "P2D": "2443",
            #     "P2H": "2449"
            # },
            "ranking": {
                "P4D": "2841",
                "P3H": "2842",
                "P1D": "2728",
                "P2H": "2974"
            }
        }

        self.session: Session = Session()
        self.session.cookies.set("SelectedSeasonId", str(self.season_id_))
        self.session.cookies.set("PortailSelectedSeasonId", str(self.season_id))

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

        return response.json()

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

        return response.json()

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

        return response.json()

    def get_calendar(self, team: str = None):
        session = requests.Session()
        session.cookies.set("SelectedSeasonId", str(self.season_id_))
        session.cookies.set("PortailSelectedSeasonId", str(self.season_id))
        self.set_token(Urls.calendar_token_url(), session=session)
        response: Response = session.post(
            Urls.calendar_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "searchTerm": "",
                "districtId": str(self.district_id),
                "championshipId": self.teams['calendar'][team] if team else None,
                "clubId": str(self.club_id),
                "teamId": "0" if team else None,
                "dateFrom": "-1",
                "dateTo": "-1"
            },
            headers=self.headers
        )

        return response.json()

    def get_ranking(self, team: str = None):
        session = requests.Session()
        session.cookies.set("SelectedSeasonId", str(self.season_id_))
        session.cookies.set("PortailSelectedSeasonId", str(self.season_id))
        self.set_token(Urls.ranking_token_url(), session=session)
        # ranking
        response: Response = session.post(
            Urls.ranking_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "districtId": str(self.district_id),
                "championshipId": self.teams['ranking'][team] if team else None,
                "clubId": str(self.club_id),
                "teamId": "0" if team else None,
            },
            headers=self.headers
        )

        data_ranking: List[dict] = response.json()

        # ranking reserve
        response: Response = session.post(
            Urls.ranking_reserve_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "districtId": str(self.district_id),
                "championshipId": self.teams['ranking'][team] if team else None,
                "clubId": str(self.club_id),
                "teamId": "0" if team else None,
            },
            headers=self.headers
        )

        data_ranking_reserve: List[dict] = response.json()

        return {
            "main": data_ranking,
            "reserve": data_ranking_reserve
        }

    @token_refresh_required
    def get_referee_fee(self):
        self.set_token(Urls.referee_fee_token_url())
        response: Response = self.session.post(
            Urls.referee_fee_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "searchTerm": "",
                "isPaid": False
            },
            headers=self.headers
        )
        return response.json()

    @token_refresh_required
    def get_team(self):
        self.set_token(Urls.team_token_url())
        response: Response = self.session.post(
            Urls.team_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
            },
            headers=self.headers
        )
        return response.json()

    @token_refresh_required
    def get_player(self):
        self.set_token(Urls.player_token_url())
        response: Response = self.session.post(
            Urls.player_url(),
            data={
                "sort": "",
                "group": "",
                "filter": "",
                "searchTerm": "",
                "inErrorOnly": False
            },
            headers=self.headers
        )
        return response.json()
