import os
import uuid
from datetime import datetime

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable, ListItem, ListFlowable
)


def set_background_logos(canvas, doc):
    """Draws organization logos at fixed positions on the PDF canvas background."""
    wekab_logo_path = os.path.expanduser("media/wekab_verified.png")
    keystore_logo_path = os.path.expanduser("media/keystore.png")

    wekab_logo = Image(wekab_logo_path, width=4 * cm, height=4 * cm)
    keystore_logo = Image(keystore_logo_path, width=1.5 * cm, height=2 * cm)

    wekab_logo.left = 13 * cm
    wekab_logo.bottom = 2.5 * cm
    keystore_logo.left = 4 * cm
    keystore_logo.bottom = 3.75 * cm

    wekab_logo.drawOn(canvas, wekab_logo.left, wekab_logo.bottom)
    keystore_logo.drawOn(canvas, keystore_logo.left, keystore_logo.bottom)


def set_vertical_doc_id(canvas, doc, document_id: uuid.UUID):
    """Displays a vertically rotated document ID with styling on the PDF canvas."""
    canvas.saveState()
    canvas.translate(1 * cm, 3.5 * cm)
    canvas.rotate(90)

    canvas.setFont("Helvetica-Oblique", 12)
    canvas.setFillColor(colors.black)
    docid_label = "DocID: "
    canvas.drawString(0, 0, docid_label)

    docid_width = canvas.stringWidth(docid_label, "Helvetica-Oblique", 12)

    canvas.setFillColor(colors.HexColor("#d32f2f"))
    canvas.drawString(docid_width, 0, "[")

    uuid_value = str(document_id)
    uuid_width = canvas.stringWidth(uuid_value, "Helvetica-Oblique", 12)

    canvas.setFillColor(colors.black)
    canvas.setFont("Helvetica-Oblique", 12)
    canvas.drawString(docid_width + 8, 0, uuid_value)

    canvas.setFillColor(colors.HexColor("#d32f2f"))
    canvas.setFont("Helvetica-Oblique", 12)
    canvas.drawString(docid_width + 8 + uuid_width + 2, 0, "]")

    canvas.restoreState()


# Callback to print special parts out of the layout
def build_document_callback_manager(document_id: uuid.UUID):
    """Returns a callback function to render background elements and document ID during PDF build."""

    def callback(canvas, doc):
        set_vertical_doc_id(canvas, doc, document_id)
        set_background_logos(canvas, doc)

    return callback


def create_execution_certificate(
        signer_full_name: str,
        signer_dni: str,
        signer_role: str,
        signer_organization: str,
        signer_organization_id: str,
        participant_full_name: str,
        participant_dni: str,
        course_title: str,
        course_start_date: str,
        course_end_date: str,
        total_course_hours: int,
        presential_hours: int,
        webinar_hours: int,
        online_hours: int,
        header_logo_path: str,
        output_pdf_path: str,
        output_pdf_uuid: uuid.UUID,
        course_code: str = None,
        professional_family: str = None,
        professional_area: str = None,

):
    """
    Generates a styled PDF certificate verifying the delivery of a course, including details about the
    instructor, course, and signer, with visual elements and validation info.

    Args:
        signer_full_name (str): Full name of the person issuing the certificate.
        signer_dni (str): National ID of the signer.
        signer_role (str): Role of the signer within the organization.
        signer_organization (str): Name of the organization the signer represents.
        signer_organization_id (str): Tax or business ID of the signer's organization.
        participant_full_name (str): Full name of the course instructor (participant).
        participant_dni (str): National ID of the participant.
        course_title (str): Title of the delivered course.
        course_start_date (str): Start date of the course.
        course_end_date (str): End date of the course.
        total_course_hours (int): Total number of hours taught in the course.
        presential_hours (int): Number of in-person teaching hours.
        webinar_hours (int): Number of hours taught via webinars or virtual sessions.
        online_hours (int): Number of hours taught via online tutoring.
        header_logo_path (str): File path to the header logo image.
        output_pdf_path (str): Destination file path to save the generated PDF certificate.
        output_pdf_uuid (uuid.UUID): Unique identifier of the certificate for tracking.
        course_code (str, optional): Course identification code.
        professional_family (str, optional): Professional family the course belongs to.
        professional_area (str, optional): Professional area the course is related to.
    """

    output_pdf_path = os.path.expanduser(output_pdf_path)

    # Setup styles
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle("normal_style", parent=styles["Normal"], fontName="Helvetica", fontSize=12,
                                  leading=18, alignment=TA_JUSTIFY)
    normal_style_spacer = ParagraphStyle("normal_style_spacer", parent=normal_style, leftIndent=0.2 * cm)
    title_style = ParagraphStyle("title_style", parent=normal_style, fontName="Helvetica", fontSize=21,
                                 alignment=TA_CENTER,
                                 textColor=colors.HexColor("#009CDE"), spaceAfter=8, spaceBefore=4, leading=30)
    footer_style = ParagraphStyle("small", parent=normal_style, fontSize=9, alignment=TA_CENTER, leading=12)
    right_align_title = ParagraphStyle('right_align_title', parent=normal_style, alignment=TA_RIGHT)
    small = ParagraphStyle('small', parent=normal_style, fontSize=10)

    # Setup document layout
    document = SimpleDocTemplate(output_pdf_path, pagesize=A4, rightMargin=2.2 * cm, leftMargin=2.2 * cm,
                                 topMargin=0.6 * cm, bottomMargin=0.2 * cm)

    content_elements = []

    # Calculate header logo ratio to be responsive
    max_width = 6 * cm
    max_height = 3.8 * cm
    with PILImage.open(header_logo_path) as img:
        orig_width, orig_height = img.size
        ratio = min(max_width / orig_width, max_height / orig_height)
        final_width = orig_width * ratio
        final_height = orig_height * ratio
    header_logo = Image(header_logo_path, width=final_width, height=final_height)

    # Setup header section
    title = Paragraph("CERTIFICADO<br/>DE IMPARTICIÓN", title_style)
    header_table = Table(
        [[header_logo, title]],
        colWidths=[6 * cm, 10 * cm],
        rowHeights=[3.8 * cm]
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("TEXTCOLOR", (1, 0), (1, 0), colors.black),
    ]))
    content_elements.append(header_table)
    content_elements.append(HRFlowable(width="90%", thickness=1.5, color=colors.HexColor("#009CDE")))
    content_elements.append(Spacer(1, 25))

    # Section intro with max height
    intro_section_max_height = 2.5 * cm
    fixed_height_paragraph = Paragraph(
        f"<b>{signer_full_name}</b>, con DNI <b>{signer_dni}</b>, usuario registrado en WeKAb en calidad de <b>{signer_role}</b> de <b>{signer_organization}</b> con CIF <b>{signer_organization_id}</b>",
        normal_style
    )
    fixed_height_table = Table(
        [[fixed_height_paragraph]],
        rowHeights=[intro_section_max_height]
    )
    fixed_height_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (0, 0), "TOP"),  # o "MIDDLE" o "BOTTOM"
    ]))
    content_elements.append(fixed_height_table)

    # Section certified
    content_elements.append(Paragraph("<u>Certifica que:</u>", normal_style_spacer))
    content_elements.append(Spacer(1, 16))

    # Section course intro certified
    course_section_intro_max_height = 1.8 * cm
    fixed_height_paragraph = Paragraph(
        f"<b>{participant_full_name}</b>, con DNI {participant_dni}, <b>ha impartido</b> el curso cuyos datos se indican a continuación:",
        normal_style
    )
    fixed_height_table = Table(
        [[fixed_height_paragraph]],
        rowHeights=[course_section_intro_max_height]
    )
    fixed_height_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (0, 0), "TOP"),  # o "MIDDLE" o "BOTTOM"
    ]))
    content_elements.append(fixed_height_table)

    # Section course info
    list_items = []
    if course_title:
        title = f"Título del curso: <b>{course_title}</b>"
        if course_code:
            title += f" (<b>{course_code}</b>)"
        list_items.append(title)
    if professional_family:
        list_items.append(f"Familia Profesional: <b>{professional_family}</b>")
    if professional_area:
        list_items.append(f"Área Profesional: <b>{professional_area}</b>")
    list_items += [
        f"Fechas de impartición: del <b>{course_start_date}</b> al <b>{course_end_date}</b>",
        f"Horas totales impartidas: <b>{total_course_hours}</b> horas",
        "Horas impartidas por modalidad:"
    ]
    sublist_items = [
        f"Presencial: {presential_hours} horas",
        f"Webinar/presencial virtual: {webinar_hours} horas",
        f"Tutorízación online: {online_hours} horas",
    ]
    sublist = [
        ListItem(Paragraph(f"{item}", normal_style), leftIndent=30) for item in sublist_items
    ]
    main_list = ListFlowable(
        [ListItem(Paragraph(f"{item}", normal_style)) for item in list_items] + sublist,
        bulletFontName="Helvetica-Bold",
        bulletColor=colors.black,
        bulletType="bullet",
        leftIndent=10,
        spaceBefore=6,
        spaceAfter=0
    )
    course_section_list_max_height = 8.1 * cm
    fixed_height_table = Table(
        [[main_list]],
        rowHeights=[course_section_list_max_height]
    )
    fixed_height_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (0, 0), "TOP"),  # o "MIDDLE" o "BOTTOM"
    ]))
    content_elements.append(fixed_height_table)

    # Section conclusion
    content_elements.append(Paragraph(
        "Se expide el presente certificado a través de la plataforma <b>WeKAb.com</b> "
        "para la acreditación de la experiencia docente.",
        normal_style_spacer
    ))
    content_elements.append(Spacer(1, 52))

    # Section signatures
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    signed_by_paragraph = Paragraph(
        f"{signer_full_name}<br/>"
        f"DNI: {signer_dni}<br/>"
        f"Fecha y hora: {current_datetime}",
        normal_style
    )
    signed_by_title = Paragraph("<i>Emitido por:</i><br/><br/>", normal_style)
    verified_paragraph = Paragraph(
        f"<i>3P Ventures S.L. - WeKAb.com con CIF B27464593 el día {current_datetime} y firmado con un certificado emitido por FNMT</i>",
        small
    )
    verified_paragraph_title = Paragraph("<i>Verificado por:</i><br/><br/>", right_align_title)
    signatures_table_data = [
        [signed_by_title, verified_paragraph_title],
        [signed_by_paragraph, verified_paragraph]
    ]
    signature_table = Table(signatures_table_data, colWidths=[9 * cm, 7 * cm])
    signature_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0, colors.transparent),
    ]))
    content_elements.append(signature_table)
    content_elements.append(Spacer(1, 52))

    # Section footer
    content_elements.append(Paragraph(
        "Certificado generado a través de la plataforma digital WeKAb.com,<br/>"
        "especializada en la gestión de la experiencia docente.",
        footer_style
    ))

    # Document general builder
    document.build(content_elements, onFirstPage=build_document_callback_manager(output_pdf_uuid))
