import os
import zipfile


class ZipWriter:

    def create_zip(self, folder):

        zip_path = folder + ".zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

            for root, dirs, files in os.walk(folder):

                for file in files:

                    file_path = os.path.join(root, file)

                    arcname = os.path.relpath(file_path, folder)

                    zipf.write(file_path, arcname)

        return zip_path