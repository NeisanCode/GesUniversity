import os
import webbrowser
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet




def gen_registration_pdf(
    receipt: ReceiptDTO, 
    output_dir: str = "receipts", 
    auto_open: bool = True
) -> str:
    """Génère un reçu d'inscription au format PDF à partir d'un ReceiptDTO
    
    et l'ouvre automatiquement dans le navigateur.
    """
    
    # Formate le nom complet de la classe à partir des données du DTO
    class_name = (
        f"{receipt.major_name} - {receipt.level_name} ({receipt.class_group_name})"
    )

    # --- PRÉPARATION DU DOCUMENT ---
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Nom du fichier nettoyé
    safe_name = receipt.student_full_name.replace(" ", "_")
    pdf_filename = (
        f"Recu_Inscription_{receipt.receipt_number:05d}_{safe_name}.pdf"
    )
    pdf_path = os.path.join(output_dir, pdf_filename)

    # Largeur utile A4 (595.27) minus marges (30x2) = 535.27 pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )
    story = []

    # --- STYLES ---
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
    )
    sub_title_style = ParagraphStyle(
        "HeaderSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748B"),
    )
    receipt_title_style = ParagraphStyle(
        "ReceiptTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        alignment=2,  # Alignement Droite
        textColor=colors.HexColor("#2563EB"),
    )
    receipt_num_style = ParagraphStyle(
        "ReceiptNum",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        alignment=2,  # Alignement Droite
        textColor=colors.HexColor("#475569"),
    )

    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748B"),
    )
    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
    )
    value_right_style = ParagraphStyle(
        "ValueRight",
        parent=value_style,
        alignment=2,  # Alignement Droite
    )

    # --- EN-TÊTE ---
    header_data = [
        [
            [
                Paragraph("ÉTABLISSEMENT SCOLAIRE", title_style),
                Spacer(1, 4),
                Paragraph(f"Année Académique {receipt.academic_year}", sub_title_style),
            ],
            [
                Paragraph("REÇU D'INSCRIPTION", receipt_title_style),
                Spacer(1, 4),
                Paragraph(
                    f"N° INSCRIPTION : REC-{receipt.receipt_number:05d}",
                    receipt_num_style,
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

    # --- INFOS ÉTUDIANT & DATES ---
    info_data = [
        [
            Paragraph("MATRICULE :", label_style),
            Paragraph(receipt.student_id_number, value_style),
            Paragraph("DATE D'INSCRIPTION :", label_style),
            Paragraph(receipt.receipt_date.strftime("%d/%m/%Y"), value_style),
        ],
        [
            Paragraph("NOM & PRÉNOM :", label_style),
            Paragraph(receipt.student_full_name, value_style),
            Paragraph("MODE DE RÈGLEMENT :", label_style),
            Paragraph(receipt.payment_method, value_style),
        ],
        [
            Paragraph("CLASSE / FILIÈRE :", label_style),
            Paragraph(class_name, value_style),
            "",
            "",
        ],
    ]
    info_table = Table(info_data, colWidths=[120, 150, 130, 135])
    info_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("SPAN", (1, 2), (3, 2)),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 15))

    # --- TABLEAU DÉTAILS DE L'INSCRIPTION ---
    details_data = [
        ["Désignation", "Statut", "Montant Payé"],
        [
            f"Frais d'inscription - {receipt.major_name} ({receipt.level_name})",
            "VALIDE",
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
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ]
        )
    )
    story.append(details_table)
    story.append(Spacer(1, 15))

    # --- RÉSUMÉ DE L'INSCRIPTION ---
    summary_data = [
        [
            Paragraph("Total Frais d'Inscription Acquittés :", label_style),
            Paragraph(f"{receipt.amount_paid:,.0f} FCFA", value_right_style),
        ],
    ]
    summary_table = Table(summary_data, colWidths=[350, 185])
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

    # --- SIGNATURES ---
    sig_data = [
        [
            Paragraph("Signature de l'Élève / Étudiant", label_style),
            Paragraph("LA GESTIONNAIRE", label_style),
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

    # Génération du fichier PDF
    doc.build(story)

    # --- OUVERTURE DANS LE NAVIGATEUR ---
    if auto_open:
        absolute_path = Path(pdf_path).resolve()
        webbrowser.open(absolute_path.as_uri())

    return pdf_path