from follow_check import username_and_follows_you


class FakeLink:
    def __init__(self, href: str) -> None:
        self.href = href

    def get_attribute(self, name: str) -> str:
        assert name == "href"
        return self.href


class FakeItem:
    def __init__(self, href: str | None, text: str) -> None:
        self.href = href
        self.text = text

    def find_elements(self, *_args):
        return [FakeLink(self.href)] if self.href else []


def test_username_and_follows_you_reads_profile_link_and_status() -> None:
    item = FakeItem("https://www.instagram.com/example_user/", "Example User\nFollows you")

    assert username_and_follows_you(item) == ("example_user", True)


def test_username_and_follows_you_ignores_navigation_links() -> None:
    assert username_and_follows_you(FakeItem("https://www.instagram.com/explore/", "Explore")) is None
