from urllib.parse import urljoin


class Urls:
    BASE_URL: str = "https://www.portailfvwb.be/"

    @staticmethod
    def login_url() -> str:
        return urljoin(Urls.BASE_URL, "Account/Login")

    @staticmethod
    def member_token_url(member_id: int) -> str:
        return urljoin(Urls.BASE_URL, f"Member/Edit/{member_id}")

    @staticmethod
    def member_url(member_id: int) -> str:
        return urljoin(Urls.BASE_URL, f"Affiliates/PagingAffiliates?callingPage=Member&filterId={member_id}")

    @staticmethod
    def affiliates_token_url() -> str:
        return urljoin(Urls.BASE_URL, "Home/Index")

    @staticmethod
    def affiliates_url() -> str:
        return urljoin(Urls.BASE_URL, "Affiliates/PagingAffiliates?callingPage=OriginalPage&filterId=0")

    @staticmethod
    def members_url() -> str:
        return urljoin(Urls.BASE_URL, "Member/PagingMembersGrid")

    @staticmethod
    def calendar_token_url() -> str:
        return urljoin(Urls.BASE_URL, "Portail/Calendar")

    @staticmethod
    def calendar_url() -> str:
        return urljoin(Urls.BASE_URL, "Portail/PagingCalendar")

    @staticmethod
    def ranking_token_url() -> str:
        return urljoin(Urls.BASE_URL, "Portail/Ranking")

    @staticmethod
    def ranking_url() -> str:
        return urljoin(Urls.BASE_URL, "Portail/PagingRanking")

    @staticmethod
    def ranking_synoptic_url() -> str:
        return urljoin(Urls.BASE_URL, "Portail/PagingSynopticTable")

    @staticmethod
    def ranking_reserve_url() -> str:
        return urljoin(Urls.BASE_URL, "Portail/PagingRankingReserve")

    @staticmethod
    def referee_fee_token_url() -> str:
        return urljoin(Urls.BASE_URL, "RefereeExpense/Index")

    @staticmethod
    def referee_fee_url() -> str:
        return urljoin(Urls.BASE_URL, "RefereeExpense/PagingRefereeExpenses/0?callingPage=OriginalPage")

    @staticmethod
    def team_token_url() -> str:
        return urljoin(Urls.BASE_URL, "Team/Index")

    @staticmethod
    def team_url() -> str:
        return urljoin(Urls.BASE_URL, "Team/PagingElements/0?callingPage=OriginalPage")

    @staticmethod
    def player_token_url() -> str:
        return urljoin(Urls.BASE_URL, "Player/Index")

    @staticmethod
    def player_url() -> str:
        return urljoin(Urls.BASE_URL, "Player/PagingTeamAffiliates/0?callingPage=Player")
