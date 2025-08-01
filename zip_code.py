import zipfile
import os

def zip_folder(folder_path, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Relative path
                zipf.write(file_path, arcname)

# Usage: zip the entire home folder (except system files if any)
zip_folder('/home/kifreality', '/home/kifreality/home_backup.zip')
