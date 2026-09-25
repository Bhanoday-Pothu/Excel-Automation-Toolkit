from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime


def create_pdf_report(output_path,stats):
    doc=SimpleDocTemplate(str(output_path))
    styles=getSampleStyleSheet()
    elements=[]
    title=Paragraph("<b>Excel Automaton Toolkit Report</b>",styles["Title"])
    elements.append(title)
    elements.append(Paragraph("<br/><br/>",styles["Normal"]))
    
    data=[["Metric","Value"]]
    
    for key,value in stats.items():
        data.append([key,str(value)])
    
    table=Table(data,colWidths=[3*inch,2*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("BOTTOMPADING",(0,0),(-1,-0),10),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))
    elements.append(table)
    elements.append(Paragraph("<br/><br/>",styles["Normal"]))
    generated=datetime.now().strftime("%d-%m-%y %I:%M %p")
    
    elements.append(
        Paragraph(f"Generated on:{generated}",styles["Normal"])
    )
    
    doc.build(elements)
