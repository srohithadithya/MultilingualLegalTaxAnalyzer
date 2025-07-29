# backend/app/services/pdf_generation_service.py

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib import colors
import io
import json # Used for pretty-printing JSON if needed
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def generate_pdf_report(analyzed_data, language='en'):
    """
    Generates a structured PDF report from analyzed data.
    Takes analyzed_data (which might already be translated) and the target language for labels.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    h1_style = styles['h1']
    h1_style.alignment = TA_CENTER
    h3_style = styles['h3']
    normal_style = styles['Normal']
    code_style = styles['Code']
    bold_style = ParagraphStyle(
        'bold_style',
        parent=normal_style,
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12
    )
    data_style = ParagraphStyle(
        'data_style',
        parent=normal_style,
        fontSize=10,
        leading=12
    )

    # --- Labels for PDF (can be translated based on 'language' param) ---
    # For a real multi-lingual PDF, you would load these labels from a translations file
    # or use Flask-Babel/another i18n library on the server side to get translated strings.
    # For simplicity, these are hardcoded placeholders.
    labels = {
        'en': {
            'report_title': "Tax Document Analysis Report",
            'basic_info': "Basic Information:",
            'document_type': "Document Type:",
            'invoice_number': "Invoice Number:",
            'date': "Date:",
            'due_date': "Due Date:",
            'parties_involved': "Parties Involved:",
            'vendor_name': "Vendor Name:",
            'vendor_address': "Vendor Address:",
            'vendor_tax_id': "Vendor Tax ID:",
            'customer_name': "Customer Name:",
            'customer_address': "Customer Address:",
            'customer_tax_id': "Customer Tax ID:",
            'line_items': "Line Items:",
            'description': "Description",
            'quantity': "Quantity",
            'unit_price': "Unit Price",
            'total_price': "Total Price",
            'summary': "Summary:",
            'subtotal_amount': "Subtotal Amount:",
            'tax_amount': "Tax Amount:",
            'total_amount': "Total Amount:",
            'currency': "Currency:",
            'gst_number': "GST/VAT/Tax ID:", # Generic label
            'payment_terms': "Payment Terms:",
            'notes': "Notes:",
            'raw_document_snippet': "Raw Document Snippet:",
            'validation_errors': "Validation Errors:",
            'warnings': "Warnings:"
        },
        'hi': { # Hindi placeholders - you'd replace with actual Hindi text
            'report_title': "कर दस्तावेज़ विश्लेषण रिपोर्ट",
            'basic_info': "मूलभूत जानकारी:",
            'document_type': "दस्तावेज़ का प्रकार:",
            'invoice_number': "चालान संख्या:",
            'date': "दिनांक:",
            'due_date': "देय तिथि:",
            'parties_involved': "शामिल पक्ष:",
            'vendor_name': "विक्रेता का नाम:",
            'vendor_address': "विक्रेता का पता:",
            'vendor_tax_id': "विक्रेता कर पहचान:",
            'customer_name': "ग्राहक का नाम:",
            'customer_address': "ग्राहक का पता:",
            'customer_tax_id': "ग्राहक कर पहचान:",
            'line_items': "लाइन आइटम:",
            'description': "विवरण",
            'quantity': "मात्रा",
            'unit_price': "इकाई मूल्य",
            'total_price': "कुल मूल्य",
            'summary': "सारांश:",
            'subtotal_amount': "उपयोग राशि:",
            'tax_amount': "कर राशि:",
            'total_amount': "कुल राशि:",
            'currency': "मुद्रा:",
            'gst_number': "जीएसटी/वैट/कर आईडी:",
            'payment_terms': "भुगतान शर्तें:",
            'notes': "टिप्पणियाँ:",
            'raw_document_snippet': "मूल दस्तावेज़ का स्निपेट:",
            'validation_errors': "मान्यकरण त्रुटियाँ:",
            'warnings': "चेतावनी:"
        }
        # Add more languages as needed
    }.get(language, labels['en']) # Default to English if language not found


    # --- Report Content ---

    # Title
    story.append(Paragraph(f"{labels['report_title']} ({language.upper()})", h1_style))
    story.append(Spacer(1, 0.2 * 10))

    # Basic Info
    story.append(Paragraph(labels['basic_info'], h3_style))
    story.append(Paragraph(f"<b>{labels['document_type']}</b> {analyzed_data.get('document_type', 'N/A')}", data_style))
    story.append(Paragraph(f"<b>{labels['invoice_number']}</b> {analyzed_data.get('invoice_number', 'N/A')}", data_style))
    story.append(Paragraph(f"<b>{labels['date']}</b> {analyzed_data.get('date', 'N/A')}", data_style))
    story.append(Paragraph(f"<b>{labels['due_date']}</b> {analyzed_data.get('due_date', 'N/A')}", data_style))
    story.append(Spacer(1, 0.1 * 10))

    # Vendor and Customer Details
    story.append(Paragraph(labels['parties_involved'], h3_style))
    data_parties = [
        [Paragraph(f"<b>{labels['vendor_name']}</b>", bold_style), Paragraph(analyzed_data.get('vendor_name', 'N/A'), data_style),
         Paragraph(f"<b>{labels['customer_name']}</b>", bold_style), Paragraph(analyzed_data.get('customer_name', 'N/A'), data_style)],
        [Paragraph(f"<b>{labels['vendor_address']}</b>", bold_style), Paragraph(analyzed_data.get('vendor_address', 'N/A'), data_style),
         Paragraph(f"<b>{labels['customer_address']}</b>", bold_style), Paragraph(analyzed_data.get('customer_address', 'N/A'), data_style)],
        [Paragraph(f"<b>{labels['vendor_tax_id']}</b>", bold_style), Paragraph(analyzed_data.get('vendor_tax_id', 'N/A'), data_style),
         Paragraph(f"<b>{labels['customer_tax_id']}</b>", bold_style), Paragraph(analyzed_data.get('customer_tax_id', 'N/A'), data_style)]
    ]
    table_parties = Table(data_parties, colWidths=[100, 200, 100, 200])
    table_parties.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(table_parties)
    story.append(Spacer(1, 0.2 * 10))

    # Line Items
    line_items = analyzed_data.get('line_items', [])
    if line_items:
        story.append(Paragraph(labels['line_items'], h3_style))
        table_data = [
            [
                Paragraph(labels['description'], bold_style),
                Paragraph(labels['quantity'], bold_style),
                Paragraph(labels['unit_price'], bold_style),
                Paragraph(labels['total_price'], bold_style)
            ]
        ]
        for item in line_items:
            table_data.append([
                Paragraph(item.get('description', 'N/A'), data_style),
                Paragraph(str(item.get('quantity', 'N/A')), data_style),
                Paragraph(str(item.get('unit_price', 'N/A')), data_style),
                Paragraph(str(item.get('total_price', 'N/A')), data_style)
            ])
        
        table_items = Table(table_data, colWidths=[250, 80, 80, 80])
        table_items.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0F2F7')), # Light blue header
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (0,-1), 'LEFT'),
            ('ALIGN', (1,0), (-1,-1), 'RIGHT'), # Align numbers to the right
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(table_items)
        story.append(Spacer(1, 0.2 * 10))

    # Summary Totals
    story.append(Paragraph(labels['summary'], h3_style))
    summary_data = [
        [Paragraph(f"<b>{labels['subtotal_amount']}</b>", bold_style), Paragraph(f"{analyzed_data.get('currency', 'N/A')} {analyzed_data.get('subtotal_amount', '0.00')}", data_style)],
        [Paragraph(f"<b>{labels['tax_amount']}</b>", bold_style), Paragraph(f"{analyzed_data.get('currency', 'N/A')} {analyzed_data.get('tax_amount', '0.00')}", data_style)],
        [Paragraph(f"<b>{labels['total_amount']}</b>", bold_style), Paragraph(f"{analyzed_data.get('currency', 'N/A')} {analyzed_data.get('total_amount', '0.00')}", data_style)],
        [Paragraph(f"<b>{labels['gst_number']}</b>", bold_style), Paragraph(analyzed_data.get('vendor_tax_id', 'N/A'), data_style)],
        [Paragraph(f"<b>{labels['payment_terms']}</b>", bold_style), Paragraph(analyzed_data.get('payment_terms', 'N/A'), data_style)],
        [Paragraph(f"<b>{labels['notes']}</b>", bold_style), Paragraph(analyzed_data.get('notes', 'N/A'), data_style)]
    ]
    table_summary = Table(summary_data, colWidths=[150, 300])
    table_summary.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(table_summary)
    story.append(Spacer(1, 0.4 * 10))

    # Validation Errors
    validation_errors = analyzed_data.get('validation_errors', {})
    if validation_errors:
        story.append(Paragraph(labels['validation_errors'], h3_style))
        for key, error_msg in validation_errors.items():
            story.append(Paragraph(f"<b>{key}:</b> <font color='red'>{error_msg}</font>", data_style))
        story.append(Spacer(1, 0.2 * 10))

    # Warnings
    warnings = analyzed_data.get('warnings', {})
    if warnings:
        story.append(Paragraph(labels['warnings'], h3_style))
        for key, warning_msg in warnings.items():
            story.append(Paragraph(f"<b>{key}:</b> <font color='orange'>{warning_msg}</font>", data_style))
        story.append(Spacer(1, 0.2 * 10))

    # Raw Text Snippet
    if analyzed_data.get('raw_ocr_text_reference'):
        story.append(Paragraph(labels['raw_document_snippet'], h3_style))
        story.append(Paragraph(analyzed_data['raw_ocr_text_reference'], code_style))

    try:
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Error building PDF report: {e}", exc_info=True)
        raise Exception(f"Failed to build PDF report: {e}")