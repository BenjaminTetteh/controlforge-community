from datetime import datetime

from controlforge.evidence.filenames import (
    generate_secure_filename
)

from controlforge.evidence.hashing import (
    calculate_file_hash
)

from controlforge.evidence.storage import (
    get_engagement_evidence_path
)

from controlforge.evidence.validation import (
    validate_upload_file
)

from controlforge.repositories.evidence_repository import (
    create_evidence_record
)


def process_evidence_upload(
    uploaded_file,
    client_slug,
    engagement_slug,
    finding_id,
    uploaded_by
):

    validation_result, message = (
        validate_upload_file(
            uploaded_file.filename
        )
    )

    if not validation_result:
        return False, message

    storage_path = (
        get_engagement_evidence_path(
            client_slug,
            engagement_slug
        )
    )

    secure_filename = (
        generate_secure_filename(
            uploaded_file.filename
        )
    )

    saved_file_path = (
        storage_path
        / secure_filename
    )

    uploaded_file.save(
        saved_file_path
    )

    file_hash = calculate_file_hash(
        saved_file_path
    )

    file_size = (
        saved_file_path.stat().st_size
    )

    create_evidence_record(
        finding_id=finding_id,
        client_slug=client_slug,
        engagement_slug=engagement_slug,
        original_filename=uploaded_file.filename,
        stored_filename=secure_filename,
        uploaded_by=uploaded_by,
        upload_timestamp=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        file_hash=file_hash,
        file_size=file_size,
        content_type=uploaded_file.content_type
    )

    return True, "Evidence uploaded successfully."