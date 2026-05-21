from controlforge_web.database import (
    get_db_connection
)


def load_evidence_for_finding(
    finding_id: str
):

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            original_filename,
            stored_filename,
            uploaded_by,
            upload_timestamp,
            file_hash,
            file_size,
            content_type
        FROM evidence_files
        WHERE finding_id = ?
        ORDER BY id DESC
        """,
        (finding_id,)
    ).fetchall()

    connection.close()

    return [
        {
            "id": row["id"],
            "original_filename": row["original_filename"],
            "stored_filename": row["stored_filename"],
            "uploaded_by": row["uploaded_by"],
            "upload_timestamp": row["upload_timestamp"],
            "file_hash": row["file_hash"],
            "file_size": row["file_size"],
            "content_type": row["content_type"]
        }
        for row in rows
    ]