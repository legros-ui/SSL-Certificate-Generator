 # SSL Certificate Generator with AI-Enhanced Features
# Created by Thomas Legros
# Repository: https://github.com/legros-ui/SSL-Certificate-Generator

import os
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import openai  # For AI-driven functionality (Requires OpenAI API Key)

# Initialize OpenAI (AI-based logging, summarization, or customization suggestions)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_private_key():
    """
    Generate a private RSA key with a 2048-bit length.
    """
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

def generate_self_signed_cert(private_key, common_name="Thomas Legros SSL Cert", expiration_days=365):
    """
    Generate a self-signed SSL certificate.
    """
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Virginia"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Lynchburg"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Thomas Legros Corp"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False)
        .sign(private_key, hashes.SHA256(), default_backend())
    )
    
    return cert

def save_certificate_and_key(cert, private_key, cert_filename="cert.pem", key_filename="key.pem"):
    """
    Save certificate and private key to files.
    """
    with open(cert_filename, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(key_filename, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    print(f"Certificate and key saved as {cert_filename} and {key_filename}")

def ai_log_summarize(cert_info):
    """
    Use OpenAI to generate a summary of the generated certificate details for logging.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following SSL certificate information for logging:\n{cert_info}",
        max_tokens=100
    )
    print("AI-generated summary:", response.choices[0].text.strip())

# Main function
def main():
    print("Starting SSL Certificate Generation...")
    
    # Step 1: Generate RSA Private Key
    private_key = generate_private_key()
    
    # Step 2: Generate Self-Signed Certificate
    cert = generate_self_signed_cert(private_key)
    
    # Step 3: Save Certificate and Key
    save_certificate_and_key(cert, private_key)
    
    # Step 4: Log Certificate Information using AI
    cert_info = cert.subject
    ai_log_summarize(cert_info)

if __name__ == "__main__":
    main()
