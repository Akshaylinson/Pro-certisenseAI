# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read markdown file
with open('SYNOPSIS.README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Clean content
content = content.replace('\u2705', '').replace('\u2714', '').replace('\u2716', '')

# Create PDF
pdf_path = 'SYNOPSIS_CertiSense_AI_v3.0.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
story = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1a5490'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#2c5aa0'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#3d6bb3'),
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

heading3_style = ParagraphStyle(
    'CustomHeading3',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#4a7bc4'),
    spaceAfter=6,
    spaceBefore=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=6
)

# Parse markdown and add to story
lines = content.split('\n')
i = 0
page_count = 0
while i < len(lines):
    line = lines[i]
    
    # Title
    if line.startswith('# '):
        title = line.replace('# ', '').strip()
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.2*inch))
        i += 1
    
    # Heading 1
    elif line.startswith('## '):
        heading = line.replace('## ', '').strip()
        story.append(Paragraph(heading, heading1_style))
        i += 1
    
    # Heading 2
    elif line.startswith('### '):
        heading = line.replace('### ', '').strip()
        story.append(Paragraph(heading, heading2_style))
        i += 1
    
    # Heading 3
    elif line.startswith('#### '):
        heading = line.replace('#### ', '').strip()
        story.append(Paragraph(heading, heading3_style))
        i += 1
    
    # Code block
    elif line.startswith('```'):
        code_lines = []
        i += 1
        while i < len(lines) and not lines[i].startswith('```'):
            code_lines.append(lines[i])
            i += 1
        code_text = '\n'.join(code_lines).strip()
        if code_text:
            story.append(Paragraph(f'<font face="Courier" size="9"><b>{code_text}</b></font>', body_style))
            story.append(Spacer(1, 0.1*inch))
        i += 1
    
    # Table
    elif line.startswith('|'):
        table_rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = [cell.strip() for cell in lines[i].split('|')[1:-1]]
            if cells and not all('-' in c for c in cells):
                table_rows.append(cells)
            i += 1
        
        if table_rows and len(table_rows) > 1:
            table = Table(table_rows, colWidths=[1.5*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
            ]))
            story.append(table)
            story.append(Spacer(1, 0.15*inch))
    
    # Empty line
    elif line.strip() == '':
        story.append(Spacer(1, 0.05*inch))
        i += 1
    
    # Regular text
    else:
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
        i += 1

# Build PDF
try:
    doc.build(story)
    print(f"PDF generated successfully: {pdf_path}")
except Exception as e:
    print(f"Error generating PDF: {str(e)}")
