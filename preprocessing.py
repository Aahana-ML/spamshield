
from pathlib import Path
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import html
import re


def extract_body(email_source):

    if isinstance(email_source, bytes):
        raw_email = email_source
        
    else:
        email_path = Path(email_source)
        
        with open(email_path, "rb") as f:
            raw_email = f.read()

    parsed = BytesParser(policy=policy.default).parsebytes(raw_email)

    subject = str(parsed["Subject"]) if parsed["Subject"] else ""

    body = parsed.get_body(preferencelist=("plain", "html"))

    if body is None:
        return subject, ""

    try:
        body_text = body.get_content()

    except LookupError:
        payload = body.get_payload(decode=True)

        if payload is None:
            return subject, ""

        body_text = payload.decode("utf-8", errors="replace")

    if body.get_content_type() == "text/html":

        soup = BeautifulSoup(body_text, "html.parser")

        links = soup.find_all("a", href=True)

        url_tokens = ["URL" for url in links]

        url_str = " ".join(url_tokens)

        clean_text = soup.get_text(separator=" ", strip=True)

        body_text = clean_text + " " + url_str

    body_text = html.unescape(body_text)

    body_text = re.sub(r"https?://\S+", "URL", body_text)

    body_text = re.sub(r"\d+", "NUMBER", body_text)

    body_text = re.sub(r"\s+", " ", body_text).strip()

    return subject, body_text


def preprocess_text(subject, body_text):

    combined_text = subject + " " + body_text

    combined_text = re.sub(r"https?://\S+", "URL", combined_text)

    combined_text = re.sub(r"\d+", "NUMBER", combined_text)

    combined_text = re.sub(r"\s+", " ", combined_text).strip()

    return combined_text


def preprocess_email(email_path):

    subject, body_text = extract_body(email_path)

    return preprocess_text(subject, body_text)


def preprocess_uploaded_email(email_bytes):

    subject, body_text = extract_body(email_bytes)

    return preprocess_text(subject, body_text)
