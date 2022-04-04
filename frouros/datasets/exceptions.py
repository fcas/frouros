"""Dataset exception module."""


class AllNaNValuesError(Exception):
    """All NaN values exception."""


class DownloadError(Exception):
    """Download exception."""


class InvalidFilePathError(Exception):
    """Invalid file path exception."""


class InvalidURLError(Exception):
    """Invalid URL exception."""


class RequestFileError(Exception):
    """Request file exception."""


class ReadFileError(Exception):
    """Read file exception."""