import os
import qrcode
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Base directory of your Django project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Directory for storing snipsheets PDFs
snipsheets_dir = os.path.join(base_dir, 'snips', 'snipsheets')

def format_snip_id(snip_id:str):
    # Remove any existing hyphens from the input string
    cleaned_snip_id = snip_id.replace("-", "")
    # Separate the string by inserting a hyphen every third character
    return "-".join(cleaned_snip_id[i:i+3] for i in range(0, len(cleaned_snip_id), 3))

def create_snipsheet_pdf(snip_ids:list, snipsheet_id:str, base_link:str="www.studysnips.com"):
    # Combine each hash code with the base link
    base_link = "www.studysnips.com"
    full_links = [f"{base_link}?snip_id={code}" for code in snip_ids]
    # Initialize matplotlib figure and PdfPages object
    pdf_pages = PdfPages(os.path.join(snipsheets_dir, f"{snipsheet_id}.pdf"))
    fig, axs = plt.subplots(nrows=7, ncols=5, figsize=(8, 12), facecolor='white')
    # Flatten the array of axes for easy iteration
    axs_flat = axs.flatten()
    # Generate and plot QR codes and their corresponding hash codes
    for ax, (link, hash_code) in zip(axs_flat, zip(full_links, snip_ids)):
        # Generate QR code
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="transparent")
        # Convert QR code to an image that matplotlib can plot
        ax.imshow(img, interpolation='nearest', aspect='auto')
        ax.set_facecolor('white')
        ax.axis('off')
        # Display the hash code text just below the QR code
        ax.text(0.5, -0.0, format_snip_id(hash_code), ha='center', va='top', transform=ax.transAxes)
    # Adjust layout to prevent overlap
    plt.tight_layout()
    # Save the figure to a PDF file
    pdf_pages.savefig(fig)
    pdf_pages.close()
    plt.close(fig)  # Close the figure to free memory

def delete_snipsheet_pdf(snipsheet_id:str):
    if os.path.exists(os.path.join(snipsheets_dir, f"{snipsheet_id}.pdf")):
        os.remove(os.path.join(snipsheets_dir, f"{snipsheet_id}.pdf"))
        print(f"Snipsheet {snipsheet_id} has been deleted.")
    else:
        print(f"Snipsheet {snipsheet_id} does not exist.")
