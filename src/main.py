import os
import datetime
import uuid

from config.settings import Settings as settings
from src.create_certificate import create_execution_certificate
from src.sign_pdf import sign_pdf



def delete_tmp_file(filename: str) -> None:
    try:
        filename = os.path.expanduser(filename)
        os.remove(filename)
        print(f"✅ TMP PDF deleted: {filename}")
    except OSError as e:
        print(f"❌ Error deleting tmp PDF: {e}")


def process_certificates() -> None:
    document_id = uuid.uuid4()
    print(f"🚀 Generating new document {document_id}")
    tmp_certificate_path = f"{settings.working_dir}/tmp_{document_id}_certificate.pdf"
    create_execution_certificate(
        signer_full_name="Felipe Alvarado Rodríguez",
        signer_dni="87654321F",
        signer_role="Técnico de Formación",
        signer_organization="3P Ventures S.L.",
        signer_organization_id="B12345678",
        participant_full_name="Juan Diego Pereiro Areán",
        participant_dni="45671234Z",
        course_title="Creación automatizada de certificados desde Python",
        course_sepe_code="SSCE0110",
        professional_family="Lenguajes de programación",
        professional_area="Tecnologías de la información",
        course_start_date="04/03/2025",
        course_end_date="15/04/2025",
        total_course_hours=380,
        presential_hours=380,
        webinar_hours=0,
        online_hours=0,
        header_logo_path="examples/tu-formacion-importa-logo.png",
        output_pdf_path=tmp_certificate_path,
        output_pdf_uuid=document_id,
        course_internal_code="FEH25468339",
        presential_town="Monterroso",
        presential_province="Lugo",
        is_draft=False
    )
    sign_pdf(
        input_pdf=tmp_certificate_path,
        output_pdf=f"{settings.working_dir}/wekab_certificate_{document_id}_signed.pdf",
        pkcs12_certificate_path=settings.fnmt_certificate_path,
        pkcs12_certificate_password=settings.fnmt_certificate_password or os.environ.get("FNMT_CERTIFICATE_PASSWORD"),
        show_signature_info=False
    )
    delete_tmp_file(tmp_certificate_path)


if __name__ == '__main__':
    process_certificates()
