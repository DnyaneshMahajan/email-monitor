"""
Database queries
"""

#
# emails
#

EMAIL_EXISTS = """
SELECT 
    1
FROM 
    emails
WHERE 
    provider = ?
    AND provider_message_id = ?
LIMIT 1;
"""


EMAIL_INSERT = """
INSERT INTO emails
(
    provider,
    provider_message_id,
    thread_id,
    sender,
    recipients_to,
    recipients_cc,
    recipients_bcc,
    reply_to,
    subject,
    body_text,
    body_html,
    received_on,
    processing_status,
    last_error,
    created_on,
    updated_on
)
VALUES
(
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
);
"""


EMAIL_SELECT_BY_ID = """
SELECT 
    *
FROM 
    emails
WHERE 
    id = ?;
"""


EMAIL_SELECT_BY_PROVIDER_MESSAGE_ID = """
SELECT
    *
FROM
    emails
WHERE
    provider = ?
    AND provider_message_id = ?
"""


EMAIL_UPDATE_STATUS = """
UPDATE
    emails
SET
    processing_status = ?,
    last_error = ?,
    updated_on = ?
WHERE
    id = ?
"""


EMAIL_DELETE_BY_ID = """
DELETE FROM
    emails
WHERE
    id = ?
"""