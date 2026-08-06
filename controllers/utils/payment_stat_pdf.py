import datetime
import os
import tempfile

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class NumberedCanvas(canvas.Canvas):
    """Canvas personnalisé pour ajouter la numérotation 'Page X / Y' dynamiquement."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6b7280"))
        page_text = f"Page {self._pageNumber} / {page_count}"
        self.drawRightString(A4[0] - 10 * mm, 10 * mm, page_text)


def payment_stat_pdf(
    month_name: str,
    class_name: str,
    program_name: str,
    academic_year: str,
    students: list[dict],
    only_unpaid: bool = False,
) -> str:
    """Génère le PDF du rapport de paiement avec ReportLab et retourne le chemin du fichier."""

    output_dir = tempfile.gettempdir()
    file_name = f"rapport_paiements_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(output_dir, file_name)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=12 * mm,
        bottomMargin=15 * mm,
    )

    page_width = A4[0] - 20 * mm

    # Styles
    styles = getSampleStyleSheet()

    style_inst_title = ParagraphStyle(
        "InstTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#1e3a8a"),
    )
    style_inst_sub = ParagraphStyle(
        "InstSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4b5563"),
    )
    style_rep_title = ParagraphStyle(
        "RepTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        alignment=2,
        textColor=colors.HexColor("#2563eb"),
    )
    style_rep_meta = ParagraphStyle(
        "RepMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=2,
        textColor=colors.HexColor("#6b7280"),
    )

    style_ctx_lbl = ParagraphStyle(
        "CtxLbl",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=colors.HexColor("#475569"),
    )
    style_ctx_val = ParagraphStyle(
        "CtxVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        textColor=colors.HexColor("#0f172a"),
    )

    style_th = ParagraphStyle(
        "TH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=colors.white,
    )
    style_th_right = ParagraphStyle("THRight", parent=style_th, alignment=2)
    style_th_center = ParagraphStyle("THCenter", parent=style_th, alignment=1)

    style_td = ParagraphStyle(
        "TD",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1f2937"),
    )
    style_td_right = ParagraphStyle("TDRight", parent=style_td, alignment=2)
    style_td_center = ParagraphStyle("TDCenter", parent=style_td, alignment=1)

    style_status_paid = ParagraphStyle(
        "StatusPaid",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        alignment=1,
        textColor=colors.HexColor("#15803d"),
    )
    style_status_unpaid = ParagraphStyle(
        "StatusUnpaid",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        alignment=1,
        textColor=colors.HexColor("#b91c1c"),
    )

    story = []

    # 1. En-tête
    now_str = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
    report_type = "DES IMPAYÉS" if only_unpaid else "RÉCAPITULATIF DES ENCAISSEMENTS"

    header_left = [
        Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_inst_title),
        Paragraph("ISPSLO - Enregistrement comptable de scolarités", style_inst_sub),
    ]
    header_right = [
        Paragraph(f"ÉTAT {report_type}", style_rep_title),
        Paragraph(f"MOIS : <b>{month_name.upper()}</b> | Généré le {now_str}", style_rep_meta),
    ]

    header_table = Table([[header_left, header_right]], colWidths=[page_width * 0.55, page_width * 0.45])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=8))

    # 2. Bloc Contexte
    filter_label = "Seulement Impayés" if only_unpaid else "Tous les étudiants"
    ctx_data = [
        [
            Paragraph("Programme :", style_ctx_lbl),
            Paragraph(program_name, style_ctx_val),
            Paragraph("Classe :", style_ctx_lbl),
            Paragraph(class_name, style_ctx_val),
        ],
        [
            Paragraph("Année Acad. :", style_ctx_lbl),
            Paragraph(academic_year, style_ctx_val),
            Paragraph("Filtre :", style_ctx_lbl),
            Paragraph(filter_label, style_ctx_val),
        ],
    ]
    ctx_table = Table(ctx_data, colWidths=[page_width * 0.15, page_width * 0.35, page_width * 0.15, page_width * 0.35])
    ctx_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(ctx_table)
    story.append(Spacer(1, 10))

    # 3. Tableau des données
    col_widths = [
        page_width * 0.14,  # Niveau
        page_width * 0.18,  # Matricule
        page_width * 0.32,  # Nom & Prénom
        page_width * 0.14,  # Scolarité
        page_width * 0.14,  # Déjà versé
        page_width * 0.08,  # Statut
    ]

    table_data = [[
        Paragraph("Niveau", style_th),
        Paragraph("Matricule", style_th),
        Paragraph("Nom & Prénom(s)", style_th),
        Paragraph("Scolarité", style_th_right),
        Paragraph("Déjà Versé", style_th_right),
        Paragraph("Statut", style_th_center),
    ]]

    tstyle = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]

    total_students = len(students)
    total_paid_count = sum(1 for s in students if s["is_paid"])
    total_unpaid_count = total_students - total_paid_count
    total_amount_collected = sum(s["amount_paid"] for s in students)

    if not students:
        table_data.append([
            Paragraph("Aucune donnée disponible", style_td),
            "", "", "", "", ""
        ])
        tstyle.append(("SPAN", (0, 1), (5, 1)))
        tstyle.append(("ALIGN", (0, 1), (5, 1), "CENTER"))
    else:
        for idx, s in enumerate(students, start=1):
            is_paid = s["is_paid"]
            status_p = Paragraph("En Règle", style_status_paid) if is_paid else Paragraph("En Retard", style_status_unpaid)
            scolarite_str = f"{s.get('monthly_fee', 0):,.0f} F".replace(",", " ")
            verse_str = f"{s['amount_paid']:,.0f} F".replace(",", " ")

            if idx % 2 == 0:
                tstyle.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#f8fafc")))

            table_data.append([
                Paragraph(s.get("level_name", "N/A"), style_td),
                Paragraph(s["student_id_number"], style_td),
                Paragraph(s["full_name"], style_td),
                Paragraph(scolarite_str, style_td_right),
                Paragraph(verse_str, style_td_right),
                status_p,
            ])

    data_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    data_table.setStyle(TableStyle(tstyle))
    story.append(data_table)
    story.append(Spacer(1, 10))

    # 4. Total & Récapitulatif
    summary_left = Paragraph(
        f"<b>Total :</b> {total_students} élève(s) (En règle : {total_paid_count} | En retard : {total_unpaid_count})",
        style_td,
    )
    summary_right = Paragraph(
        f"<b>TOTAL ENCAISSÉ : {total_amount_collected:,.0f} FCFA</b>".replace(",", " "),
        style_td_right,
    )

    summary_table = Table([[summary_left, summary_right]], colWidths=[page_width * 0.5, page_width * 0.5])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # 5. Signatures
    style_sig_left = ParagraphStyle(
        "SigLeft",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=colors.HexColor("#334155"),
    )
    style_sig_right = ParagraphStyle("SigRight", parent=style_sig_left, alignment=2)

    sig_table = Table(
        [
            [Paragraph("LE SERVICE COMPTABILITÉ", style_sig_left), Paragraph("VISA DE DIRECTION GÉNÉRALE", style_sig_right)],
            [Spacer(1, 35), Spacer(1, 35)],
            [
                HRFlowable(width="70%", thickness=0.5, color=colors.HexColor("#94a3b8"), hAlign="LEFT"),
                HRFlowable(width="70%", thickness=0.5, color=colors.HexColor("#94a3b8"), hAlign="RIGHT"),
            ],
        ],
        colWidths=[page_width * 0.5, page_width * 0.5],
    )
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(sig_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path