import os
import webbrowser
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from models import ReceiptDTO


def generate_reregistration_pdf(
    receipt: ReceiptDTO, output_dir: str = "receipts", auto_open: bool = True
) -> str:
    """Génère un reçu de réinscription propre, moderne et parfaitement aligné au format PDF
    et l'ouvre automatiquement dans le navigateur/lecteur PDF.
    """

    # --- 1. PRÉPARATION DU DOSSIER ET DU FICHIER ---
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    safe_student_name = receipt.student_full_name.replace(" ", "_")
    pdf_filename = (
        f"Recu_Reinscription_{receipt.receipt_number:05d}_{safe_student_name}.pdf"
    )
    pdf_path = os.path.join(output_dir, pdf_filename)

    # Dimensions A4 : 595.27 x 841.89 pt
    # Marges de 36 pt (0.5 pouce) -> Largeur imprimable utile = 523 pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    story = []

    # --- PALETTE DE COULEURS PROFESSIONNELLE ---
    PRIMARY_COLOR = colors.HexColor("#1E3A8A")  # Bleu Marine
    ACCENT_COLOR = colors.HexColor("#2563EB")  # Bleu Dynamique
    TEXT_DARK = colors.HexColor("#0F172A")  # Slate 900
    TEXT_MUTED = colors.HexColor("#64748B")  # Slate 500
    BG_LIGHT = colors.HexColor("#F8FAFC")  # Slate 50
    BG_HEADER = colors.HexColor("#F1F5F9")  # Slate 100
    BORDER_COLOR = colors.HexColor("#E2E8F0")  # Slate 200

    styles = getSampleStyleSheet()

    # --- STYLES DE PARAGRAPHE ---
    title_style = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=PRIMARY_COLOR,
    )
    motto_style = ParagraphStyle(
        "HeaderMotto",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=TEXT_MUTED,
    )
    sub_title_style = ParagraphStyle(
        "HeaderSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK,
    )
    receipt_title_style = ParagraphStyle(
        "ReceiptTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        alignment=2,  # Alignement Droite
        textColor=ACCENT_COLOR,
    )
    receipt_num_style = ParagraphStyle(
        "ReceiptNum",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        alignment=2,  # Alignement Droite
        textColor=PRIMARY_COLOR,
    )

    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=TEXT_MUTED,
    )
    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        textColor=TEXT_DARK,
    )
    value_bold_style = ParagraphStyle(
        "ValueBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=TEXT_DARK,
    )
    value_right_style = ParagraphStyle(
        "ValueRight",
        parent=value_bold_style,
        alignment=2,  # Alignement Droite
    )

    tbl_header_style = ParagraphStyle(
        "TblHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK,
    )
    tbl_header_right = ParagraphStyle(
        "TblHeaderRight",
        parent=tbl_header_style,
        alignment=2,
    )
    tbl_header_center = ParagraphStyle(
        "TblHeaderCenter",
        parent=tbl_header_style,
        alignment=1,
    )

    # --- 2. EN-TÊTE DU DOCUMENT ---
    # Largeur : 330 + 193 = 523 pt
    header_data = [
        [
            [
                Paragraph("INSTITUT SUPÉRIEUR", title_style),
                Paragraph("POLYTECHNIQUE SAINTE LUCIE D'OYO", title_style),
                Spacer(1, 3),
                Paragraph("Rigueur — Réussite — Innovation", motto_style),
                Spacer(1, 4),
                Paragraph(
                    f"Année Académique : <b>{receipt.academic_year}</b>",
                    sub_title_style,
                ),
            ],
            [
                Paragraph("REÇU DE RÉINSCRIPTION", receipt_title_style),
                Spacer(1, 4),
                Paragraph(
                    f"N° REÇU : REC-{receipt.receipt_number:05d}", receipt_num_style
                ),
                Spacer(1, 4),
                Paragraph(
                    f"Date : <b>{receipt.receipt_date.strftime('%d/%m/%Y')}</b>",
                    value_right_style,
                ),
            ],
        ]
    ]
    header_table = Table(header_data, colWidths=[330, 193])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -1), 1.5, PRIMARY_COLOR),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 15))

    # --- 3. INFORMATIONS ÉTUDIANT & PAIEMENT ---
    # Largeur : 110 + 151.5 + 110 + 151.5 = 523 pt
    formatted_date = receipt.receipt_date.strftime("%d/%m/%Y")
    program_label = (
        f"{receipt.major_name} — {receipt.level_name} ({receipt.class_group_name})"
    )

    info_data = [
        [
            Paragraph("MATRICULE", label_style),
            Paragraph(receipt.student_id_number, value_bold_style),
            Paragraph("MODE DE RÈGLEMENT", label_style),
            Paragraph(receipt.payment_method, value_bold_style),
        ],
        [
            Paragraph("NOM & PRÉNOM", label_style),
            Paragraph(receipt.student_full_name, value_bold_style),
            Paragraph("DATE RÈGLEMENT", label_style),
            Paragraph(formatted_date, value_style),
        ],
        [
            Paragraph("FILIÈRE & CLASSE", label_style),
            Paragraph(program_label, value_style),
            Paragraph("EMAIL", label_style),
            Paragraph(
                receipt.student_email if receipt.student_email else "-", value_style
            ),
        ],
    ]
    info_table = Table(info_data, colWidths=[110, 151.5, 110, 151.5])
    info_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#F1F5F9")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 15))

    # --- 4. DÉTAIL DE LA RÉINSCRIPTION ---
    # Largeur : 270 + 113 + 140 = 523 pt
    details_data = [
        [
            Paragraph("Désignation", tbl_header_style),
            Paragraph("Statut", tbl_header_center),
            Paragraph("Montant Payé", tbl_header_right),
        ],
        [
            Paragraph(
                f"Frais de réinscription — {receipt.major_name} ({receipt.level_name})",
                value_style,
            ),
            Paragraph(
                "<font color='#166534'><b>PAYÉ</b></font>",
                ParagraphStyle("CenterVal", parent=value_style, alignment=1),
            ),
            Paragraph(f"<b>{receipt.amount_paid:,.0f} FCFA</b>", value_right_style),
        ],
    ]
    details_table = Table(details_data, colWidths=[270, 113, 140])
    details_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BG_HEADER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                ("LINEBELOW", (0, 0), (-1, 0), 1, ACCENT_COLOR),
            ]
        )
    )
    story.append(details_table)
    story.append(Spacer(1, 15))

    # --- 5. RÉSUMÉ DU MONTANT ---
    # Largeur : 343 + 180 = 523 pt
    summary_data = [
        [
            Paragraph(
                "Total Frais de Réinscription Acquittés :",
                ParagraphStyle(
                    "SoldeLabel", parent=label_style, textColor=PRIMARY_COLOR
                ),
            ),
            Paragraph(
                f"<font color='#2563EB'><b>{receipt.amount_paid:,.0f} FCFA</b></font>",
                value_right_style,
            ),
        ],
    ]
    summary_table = Table(summary_data, colWidths=[343, 180])
    summary_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 35))

    # --- 6. BLOC SIGNATURES ---
    # Largeur : 261.5 + 261.5 = 523 pt
    sig_data = [
        [
            Paragraph("<b>Signature de l'Élève / Étudiant</b>", label_style),
            Paragraph(
                "<b>LA GESTIONNAIRE / LA CAISSE</b>",
                ParagraphStyle("RightLabel", parent=label_style, alignment=2),
            ),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[261.5, 261.5])
    sig_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(sig_table)

    # --- 7. GÉNÉRATION ET OUVERTURE DU PDF ---
    doc.build(story)

    if auto_open:
        absolute_path = Path(pdf_path).resolve()
        webbrowser.open(absolute_path.as_uri())

    return pdf_path
