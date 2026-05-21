from controlforge_web.database import (
    get_db_connection
)


def create_evidence_record(
    finding_id: str,
    client_slug: str,
    engagement_slug: str,
    original_filename: str,
    stored_filename: str,
    uploaded_by: str,
    upload_timestamp: str,
    file_hash: str,
    file_size: int,
    content_type: str
):

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO evidence_files (
            finding_id,
            client_slug,
            engagement_slug,
            original_filename,
            stored_filename,
            uploaded_by,
            upload_timestamp,
            file_hash,
            file_size,
            content_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            finding_id,
            client_slug,
            engagement_slug,
            original_filename,
            stored_filename,
            uploaded_by,
            upload_timestamp,
            file_hash,
            file_size,
            content_type
        )
    )

    connection.commit()
    connection.close()