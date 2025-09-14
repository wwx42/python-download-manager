# modules
import requests
from tqdm import tqdm
import os
import sys

# download links 
links = list() 
download_folder = "C:/Users/Mahdi/Downloads" # enter download path

# simple function for clearing the terminal
def clear():
    return os.system("cls" if sys.platform == "win32" else "clear")

# add links to list of download
while True:
    files = input("give me download link(etc type start for start download): " )
    if files == "start":
        clear()# for use this in linux and other os
        break
    else:
        links.append(files)

# whole operation is here
for link in links:
    filename = link.split("/")[-1].split("?")[0]
    filepath = os.path.join(download_folder, filename)
    print(f"{filename} is downloading...")

    try:
        # downloading the video
        response = requests.get(link,stream=True)
        # for error of downloding
        response.raise_for_status()
        # size of your file
        total_size = int(response.headers.get('content-length', 0))
        print(f"download size is {total_size / 10**6:.2f}MB")
        # chunk for loading the file on your ram
        chunk_size = 1024 * 8 # 8KB
        # progress of downloading
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=filename)
        # read the downloaded file
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()
        print(f"{filename} download has been completed.")
        clear()
        
        

    # error handling if file not download it shows the error or status code
    except requests.exceptions.RequestException as e:
        print(f"Error in download because of {e} .")
    

print("Sincerly,\nMade by Mahdi Mohammadkhani:)")
    


