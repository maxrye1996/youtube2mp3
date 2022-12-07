from flask import Flask, render_template, request, redirect
from pytube import YouTube
from json import loads
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def run():
    return render_template('main.html')

@app.route('/process_urls', methods=['POST'])
def process_urls():
    urls: str = request.form['urls']
    urls: list = urls.split(",")
    print(urls)

    with open("config.json") as f:
        f = loads(f.read())
        print(f)
        output_dir: str = f["download_dir"]
    successful: list = []
    for url in urls:
        url = url.rstrip()
        try:
            # url input from user
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            # download the file
            out_file = video.download(output_path=output_dir)
            # save the file
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            successful.append(new_file)
            
            # result of success
            print(yt.title + " has been successfully downloaded.")
            
        except Exception as e:
            print("FAILED TO DOWNLOAD VIDEO:")
            print(e)

    return render_template('success.html', successful=successful)

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')
    

if __name__ == '__main__':
    app.run()