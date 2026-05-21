ALLOWED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt"
}


BLOCKED_EXTENSIONS = {
    ".exe",
    ".bat",
    ".cmd",
    ".sh",
    ".js",
    ".php",
    ".py",
    ".jar",
    ".msi",
    ".dll"
}


def is_allowed_extension(
    filename: str
):

    filename = filename.lower()

    for extension in BLOCKED_EXTENSIONS:

        if filename.endswith(
            extension
        ):
            return False

    return any(
        filename.endswith(
            extension
        )
        for extension in ALLOWED_EXTENSIONS
    )


def validate_upload_file(
    filename: str
):

    if not filename:
        return False, "Missing filename."

    if not is_allowed_extension(
        filename
    ):
        return False, "File type is not allowed."

    return True, "File is valid."