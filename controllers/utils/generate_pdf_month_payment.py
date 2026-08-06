import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from models import PaymentReceiptDTO


def generate_pdf_month_payment(
    receipt: PaymentReceiptDTO, output_dir: str = "receipts"
) -> str:
    """Génère un reçu de paiement propre, moderne et parfaitement aligné au format PDF."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    pdf_filename = f"Recu_{receipt.receipt_number:05d}_{receipt.student_last_name}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    # Dimensions A4 : 595.27 x 841.89 pt
    # Marges de 36 pt (0.5 pouce) -> Largeur imprimable utile = 523.27 pt (~523 pt)
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
        alignment=2,  # Droite
        textColor=ACCENT_COLOR,
    )
    receipt_num_style = ParagraphStyle(
        "ReceiptNum",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        alignment=2,  # Droite
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
        alignment=2,  # Droite
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

    # --- 1. EN-TÊTE DU DOCUMENT ---
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
                    f"Année Académique : <b>{receipt.academic_year_label}</b>",
                    sub_title_style,
                ),
            ],
            [
                Paragraph("REÇU DE PAIEMENT", receipt_title_style),
                Spacer(1, 4),
                Paragraph(f"N° : REC-{receipt.receipt_number:05d}", receipt_num_style),
                Spacer(1, 4),
                Paragraph(
                    f"Date : <b>{receipt.payment_date.strftime('%d/%m/%Y')}</b>",
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

    # --- 2. INFORMATIONS ÉTUDIANT & PAIEMENT ---
    # Largeur : 110 + 151.5 + 110 + 151.5 = 523 pt
    info_data = [
        [
            Paragraph("MATRICULE", label_style),
            Paragraph(receipt.student_id_number, value_bold_style),
            Paragraph("MODE DE RÈGLEMENT", label_style),
            Paragraph(receipt.payment_method, value_bold_style),
        ],
        [
            Paragraph("NOM & PRÉNOM", label_style),
            Paragraph(
                f"{receipt.student_last_name.upper()} {receipt.student_first_name.title()}",
                value_bold_style,
            ),
            Paragraph("DATE RÈGLEMENT", label_style),
            Paragraph(receipt.payment_date.strftime("%d/%m/%Y"), value_style),
        ],
        [
            Paragraph("CLASSE / PARCOURS", label_style),
            Paragraph(receipt.class_name, value_style),
            "",
            "",
        ],
    ]
    info_table = Table(info_data, colWidths=[110, 151.5, 110, 151.5])
    info_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("SPAN", (1, 2), (3, 2)),
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

    # --- 3. DÉTAILS DU VERSEMENT ---
    # Largeur : 270 + 113 + 140 = 523 pt
    details_data = [
        [
            Paragraph("Désignation", tbl_header_style),
            Paragraph("Mois Réglé", tbl_header_center),
            Paragraph("Montant Versé", tbl_header_right),
        ],
        [
            Paragraph("Règlement Mensualité de Scolarité", value_style),
            Paragraph(
                receipt.month_name,
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

    # --- 4. RÉSUMÉ DES MONTANTS ---
    # Largeur : 343 + 180 = 523 pt
    summary_data = [
        [
            Paragraph("Montant Global des Frais d'Étude :", label_style),
            Paragraph(f"{receipt.total_program_fees:,.0f} FCFA", value_right_style),
        ],
        [
            Paragraph("Total Réglé à ce jour :", label_style),
            Paragraph(f"{receipt.total_paid_so_far:,.0f} FCFA", value_right_style),
        ],
        [
            Paragraph(
                "Reste à Payer :",
                ParagraphStyle(
                    "SoldeLabel", parent=label_style, textColor=PRIMARY_COLOR
                ),
            ),
            Paragraph(
                f"<font color='#2563EB'><b>{receipt.remaining_balance:,.0f} FCFA</b></font>",
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
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#F1F5F9")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 35))

    # --- 5. BLOC SIGNATURES ---
    # Largeur : 261.5 + 261.5 = 523 pt
    sig_data = [
        [
            Paragraph("<b>Signature de l'Élève / Étudiant</b>", label_style),
            Paragraph(
                "<b>LA GESTIONNAIRE</b>",
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

    # Build PDF
    doc.build(story)
    return pdf_path
