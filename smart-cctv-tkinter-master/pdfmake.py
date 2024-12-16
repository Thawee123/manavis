from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io

# Initialize PDF document
def create_pdf(file_path):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Traffic Analysis", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Visitor per hour chart
    visitor_counts = [50, 75, 30, 90, 120, 110, 85, 95]
    hours = [f"{i+8}:00" for i in range(len(visitor_counts))]
    plot_visitor_counts(hours, visitor_counts)

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    img_buf.seek(0)
    elements.append(Spacer(1, 12))

    # Add Table - Zone Analysis
    data = [["Zone", "Avg. Time-spent"],
            ["Pawn Zone", "10m"],
            ["VIP Zone", "15m"],
            ["Display Zone", "5m"],
            ["Cashier Zone", "8m"]]
    table = Table(data, colWidths=[150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Building the document
    doc.build(elements)

# Function to generate visitor per hour chart
def plot_visitor_counts(hours, visitor_counts):
    plt.figure(figsize=(8, 4))
    plt.bar(hours, visitor_counts, color='skyblue')
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Visitors")
    plt.title("Visitor per Hour")

# Generate PDF
create_pdf("output_report.pdf")
