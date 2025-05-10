import os

from pyhanko import sign
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec


def sign_pdf(input_pdf: str, output_pdf: str, pkcs12_certificate_path: str, pkcs12_certificate_password: str,
             show_signature_info: bool = False):
    """
    Digitally signs a PDF using a FNMT .p12 certificate and optionally adds visible signature info.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path to save the signed PDF.
        pkcs12_certificate_path (str): Path to the .p12 certificate file.
        pkcs12_certificate_password (str): Password for the .p12 certificate.
        show_signature_info (bool): If True, displays a visible signature field in the PDF.
    """
    input_pdf = os.path.expanduser(input_pdf)
    output_pdf = os.path.expanduser(output_pdf)
    pkcs12_certificate_path = os.path.expanduser(pkcs12_certificate_path)

    signer = sign.signers.SimpleSigner.load_pkcs12(
        pfx_file=pkcs12_certificate_path,
        passphrase=pkcs12_certificate_password.encode("utf-8")
    )

    if signer is None:
        raise ValueError("Could not load .p12 certificate. Verify the path and password.")

    signature_meta = sign.PdfSignatureMetadata(
        field_name="signature",
    )

    pdf_signer = sign.PdfSigner(
        signature_meta=signature_meta,
        signer=signer,
        new_field_spec=SigFieldSpec(sig_field_name="signature", box=(346, 80, 496, 98)) if show_signature_info else None
    )

    with open(input_pdf, 'rb') as inf:
        writer = IncrementalPdfFileWriter(inf)
        with open(output_pdf, 'wb') as outf:
            pdf_signer.sign_pdf(writer, output=outf)

    print(f"✅ Certificate signed and saved as: {output_pdf}")
