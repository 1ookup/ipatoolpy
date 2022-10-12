import os.path
import plistlib
import zipfile


class SignatureClient:
    def __init__(self, path):
        self.filepath = path

    def append_metadata(self, item, email):
        self.zip = zipfile.ZipFile(self.filepath, mode='a')
        metadata = item['metadata']
        metadata["apple-id"] = email
        metadata["userName"] = email
        zinfo = zipfile.ZipInfo("iTunesMetadata.plist")
        self.zip.writestr(zinfo, plistlib.dumps(metadata))
        self.zip.close()

    def append_signature(self, item):
        self.zip = zipfile.ZipFile(self.filepath, mode='a')
        manifest = None
        app_bundle_name = None
        for file in self.zip.filelist:
            if file.filename.endswith(".app/SC_Info/Manifest.plist") and not manifest:
                manifest = plistlib.loads(self.zip.read(file))
            if file.filename.endswith(".app/Info.plist") and not app_bundle_name:
                app_bundle_name = os.path.basename(os.path.dirname(file.filename)).strip(".app")

        sinf = item['sinfs'][0]['sinf']
        signature_target_path = manifest['SinfPaths'][0]

        signature_url = f"Payload/{app_bundle_name}.app/{signature_target_path}"
        zinfo = zipfile.ZipInfo(signature_url)
        self.zip.writestr(zinfo, sinf)
        self.zip.close()
