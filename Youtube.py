from pytube import YouTube
import tqdm

class YouTube_downloader :

    def __init__(self,url) :
        self.url = url 
        self.video = None
        self.strams = None
        self.progress_bar = None

    def fetch_video(self) :
        try:
            self.video = YouTube(self.url, on_progress_callback=self.progress_callback)
            print(f"Video title: {self.video.title}")
            self.streams = self.video.streams.filter(progressive=True, file_extension='mp4')
        except Exception as e:
            print(f"An error occurred: {e}")
            

    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        if not self.progress_bar:
            self.progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True)
        self.progress_bar.update(len(chunk))

    def choose_qualities(self) :
        if self.streams :
            print("Avaible qualities : ")
            for i, stream in enumerate(self.streams) :
                print(f"{i+1}. Resolution: {stream.resolution}, Format: {stream.mime_type}")

        else :
            print("No streams available. Please fetch the video first.")


    def video_downloader(self, choice):
        if self.streams :
            try :
                selected_stream = self.streams[choice - 1]
                print(f"Downloading {selected_stream.resolution} video...")
                selected_stream.download()
                if self.progress_bar:
                    self.progress_bar.close()
                print(f"Downloaded: {self.video.title}")
            except IndexError:
                print("Invalid choice. Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred during download: {e}")
            
        else:
            print("No video to download. Please fetch the video first.")


if __name__ == "__main__" :
    link = input("Please enter URl of video : ")
    downloader = YouTube_downloader(link)
    downloader.fetch_video()
    downloader.choose_qualities()

    if downloader.streams:
        choice = int(input("Enter the number of the quality you want to download: "))
        downloader.video_downloader(choice)