class BaseExtractor:
    def extract(self, html: str, url: str) -> dict:
        raise NotImplementedError
