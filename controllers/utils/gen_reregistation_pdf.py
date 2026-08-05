import os
import webbrowser
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from models import ReceiptDTO


def gen_registration_pdf(
    receipt: ReceiptDTO, output_dir: str = "receipts", auto_open: bool = True
) -> str:
    """Génère un reçu de réinscription au format PDF à partir d'un ReceiptDTO
    et l'ouvre automatiquement dans le navigateur/lecteur PDF.
    """

    # --- 1. PRÉPARATION DES DOSSIERS ET DU FICHIER ---
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Nettoyage du nom d'étudiant pour le nom de fichier
    safe_student_name = receipt.student_full_name.replace(" ", "_")
    pdf_filename = (
        f"Recu_Reinscription_{receipt.receipt_number:05d}_{safe_student_name}.pdf"
    )
    pdf_path = os.path.join(output_dir, pdf_filename)

    # Document A4 (largeur utile = 595.27 - 60 = 535.27 pt)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )
    story = []

    # --- 2. CONFIGURATION DES STYLES ---
    base_styles = getSampleStyleSheet()

    style_header_title = ParagraphStyle(
        "HeaderTitle",
        parent=base_styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
    )
    style_header_sub = ParagraphStyle(
        "HeaderSub",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748B"),
    )
    style_receipt_title = ParagraphStyle(
        "ReceiptTitle",
        parent=base_styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        alignment=2,  # Alignement Droite
        textColor=colors.HexColor("#2563EB"),
    )
    style_receipt_num = ParagraphStyle(
        "ReceiptNum",
        parent=base_styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        alignment=2,
        textColor=colors.HexColor("#475569"),
    )
    style_label = ParagraphStyle(
        "Label",
        parent=base_styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748B"),
    )
    style_value = ParagraphStyle(
        "Value",
        parent=base_styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
    )
    style_value_right = ParagraphStyle(
        "ValueRight",
        parent=style_value,
        alignment=2,
    )

    # --- 3. BLOC EN-TÊTE ---
    header_data = [
        [
            [
                Paragraph("ÉTABLISSEMENT SCOLAIRE", style_header_title),
                Spacer(1, 4),
                Paragraph(
                    f"Année Académique : {receipt.academic_year}",
                    style_header_sub,
                ),
            ],
            [
                Paragraph("REÇU DE RÉINSCRIPTION", style_receipt_title),
                Spacer(1, 4),
                Paragraph(
                    f"N° REÇU : REC-{receipt.receipt_number:05d}",
                    style_receipt_num,
                ),
            ],
        ]
    ]
    header_table = Table(header_data, colWidths=[310, 225])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -1), 1.5, colors.HexColor("#2563EB")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 15))

    # --- 4. BLOC INFORMATIONS ÉTUDIANT & PAIEMENT ---
    formatted_date = receipt.receipt_date.strftime("%d/%m/%Y")
    program_label = (
        f"{receipt.major_name} — {receipt.level_name} ({receipt.class_group_name})"
    )

    info_data = [
        [
            Paragraph("MATRICULE :", style_label),
            Paragraph(receipt.student_id_number, style_value),
            Paragraph("DATE :", style_label),
            Paragraph(formatted_date, style_value),
        ],
        [
            Paragraph("NOM & PRÉNOM :", style_label),
            Paragraph(receipt.student_full_name, style_value),
            Paragraph("MODE DE RÈGLEMENT :", style_label),
            Paragraph(receipt.payment_method, style_value),
        ],
        [
            Paragraph("FILIÈRE & CLASSE :", style_label),
            Paragraph(program_label, style_value),
            Paragraph("EMAIL :", style_label),
            Paragraph(receipt.student_email, style_value),
        ],
    ]
    info_table = Table(info_data, colWidths=[110, 160, 130, 135])
    info_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 15))

    # --- 5. TABLEAU DÉTAIL DE LA RÉINSCRIPTION ---
    details_data = [
        ["Désignation", "Statut", "Montant Payé"],
        [
            f"Frais de réinscription — {receipt.major_name} ({receipt.level_name})",
            "PAYÉ",
            f"{receipt.amount_paid:,.0f} FCFA",
        ],
    ]
    details_table = Table(details_data, colWidths=[310, 90, 135])
    details_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#334155")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ]
        )
    )
    story.append(details_table)
    story.append(Spacer(1, 15))

    # --- 6. RÉSUMÉ DU MONTANT ---
    summary_data = [
        [
            Paragraph("Total Frais de Réinscription Acquittés :", style_label),
            Paragraph(f"{receipt.amount_paid:,.0f} FCFA", style_value_right),
        ],
    ]
    summary_table = Table(summary_data, colWidths=[330, 205])
    summary_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 35))

    # --- 7. SIGNATURES ---
    sig_data = [
        [
            Paragraph("Signature de l'Élève / Étudiant", style_label),
            Paragraph("LA GESTION / LA CAISSE", style_label),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[267, 268])
    sig_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )
    story.append(sig_table)

    # --- 8. GÉNÉRATION ET OUVERTURE DU PDF ---
    doc.build(story)

    if auto_open:
        absolute_path = Path(pdf_path).resolve()
        webbrowser.open(absolute_path.as_uri())

    return pdf_path
