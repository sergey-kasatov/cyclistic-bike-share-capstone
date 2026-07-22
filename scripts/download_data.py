import os
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

# Resolve BASE_DIR relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

BUCKET_URL = "https://divvy-tripdata.s3.amazonaws.com/"

def get_recent_12_months():
    print("Checking available files on Divvy S3 bucket...")
    try:
        req = urllib.request.Request(BUCKET_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        ns = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
        
        zip_files = []
        for contents in root.findall('s3:Contents', ns):
            key = contents.find('s3:Key', ns).text
            if key.endswith('.zip') and 'divvy-tripdata' in key:
                zip_files.append(key)
        
        recent_files = sorted(zip_files, reverse=True)[:12]
        return recent_files
    except Exception as e:
        print(f"Error fetching file list: {e}")
        return []

def download_and_extract():
    files_to_download = get_recent_12_months()
    if not files_to_download:
        print("No files found to download. Exiting.")
        return
        
    print(f"Found 12 most recent files to process:")
    for f in files_to_download:
        print(f" - {f}")
        
    for zip_name in sorted(files_to_download):
        zip_path = os.path.join(DATA_DIR, zip_name)
        download_url = BUCKET_URL + zip_name
        
        if os.path.exists(zip_path):
            print(f"\n[Skip Download] {zip_name} already exists.")
        else:
            print(f"\nDownloading {zip_name}...")
            try:
                def progress_hook(count, block_size, total_size):
                    percent = int(count * block_size * 100 / total_size)
                    percent = min(percent, 100)
                    print(f"\rProgress: {percent}% ({count * block_size // 1024 // 1024}MB / {total_size // 1024 // 1024}MB)", end="")
                
                urllib.request.urlretrieve(download_url, zip_path, reporthook=progress_hook)
                print("\nDownload complete.")
            except Exception as e:
                print(f"\nError downloading {zip_name}: {e}")
                continue
        
        print(f"Extracting {zip_name}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                csv_files = [name for name in zip_ref.namelist() if name.endswith('.csv') and not name.startswith('__MACOSX')]
                for csv_file in csv_files:
                    extracted_path = os.path.join(DATA_DIR, csv_file)
                    if os.path.exists(extracted_path):
                        print(f" - [Skip Extract] {csv_file} already extracted.")
                    else:
                        print(f" - Extracting {csv_file}...")
                        zip_ref.extract(csv_file, DATA_DIR)
            
            try:
                os.remove(zip_path)
                print(f" - Deleted zip file {zip_name} to save space.")
            except Exception as e:
                print(f" - Could not delete zip: {e}")
                
        except Exception as e:
            print(f"Error extracting {zip_name}: {e}")

if __name__ == '__main__':
    download_and_extract()
    print("\nAll data files have been processed successfully!")
