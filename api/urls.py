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
