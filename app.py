import pandas as pd
import requests
import os
import streamlit as st

# Streamlit UI
st.title("Download Images from CSV Links")

# Upload CSV file
csv_file = st.file_uploader("Upload CSV with Image Links", type=["csv"])

if csv_file:
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Ensure the 'image_link' column exists
    if 'image_link' not in df.columns:
        st.error("The CSV file must contain a column named 'image_link'.")
    else:
        # Create a directory to save the images
        output_dir = "downloaded_images"
        os.makedirs(output_dir, exist_ok=True)

        # Display the number of images to download
        st.write(f"Found {len(df)} image links. Starting the download process...")

        # Loop to download images
        for _, row in df.iterrows():
            image_url = row['image_link']
            try:
                # Send request to get the image
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    output_path = os.path.join(output_dir, f"{row['Product ID']}.jpg")
                    with open(output_path, "wb") as file:
                        file.write(response.content)
                else:
                    st.warning(f"Failed to download image from {image_url}")
            except Exception as e:
                st.error(f"Error downloading image from {image_url}: {e}")

        st.success(f"Images have been downloaded to '{output_dir}'")

        # Provide a download link for the zip of the downloaded images
        import zipfile
        zip_filename = "downloaded_images.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))
        
        st.write("Download your images as a zip file:")
        st.download_button(
            label="Download ZIP",
            data=open(zip_filename, "rb").read(),
            file_name=zip_filename,
            mime="application/zip"
        )
