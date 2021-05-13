from flask import Flask, render_template, request, session
from pytube import YouTube


app = Flask(__name__)
app.secret_key = 'abcd'


@app.route('/')
def index():
    return render_template('index.html')


# This block will return Video with Available Quality and other information with download button
@app.route('/download', methods=['GET', 'POST'])
def download():
    try:
        if request.method == 'POST':
            link = request.form['vid_url']
            session['link'] = link
            yt = YouTube(str(link))

            title = yt.title
            length = yt.length
            views = yt.views
            desc = yt.description
            img = yt.thumbnail_url

            vid720 = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution('720p')
            vid480 = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution('480p')
            vid360 = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution('360p')
            vid240 = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution('240p')
            vid144 = yt.streams.filter(progressive=True, file_extension='mp4').get_by_resolution('144p')
            vid720webm = yt.streams.filter(progressive=True, file_extension='webm').get_by_resolution('720p')
            vid480webm = yt.streams.filter(progressive=True, file_extension='webm').get_by_resolution('480p')
            vid360webm = yt.streams.filter(progressive=True, file_extension='webm').get_by_resolution('360p')
            vid240webm = yt.streams.filter(progressive=True, file_extension='webm').get_by_resolution('240p')
            vid144webm = yt.streams.filter(progressive=True, file_extension='webm').get_by_resolution('144p')

            return render_template('index.html', title=title, length=length, views=views, desc=desc,
                            img=img, fname=link, avail=True, vid720=vid720, vid480=vid480, vid360=vid360,
                            vid240=vid240, vid144=vid144, vid720webm=vid720webm, vid480webm=vid480webm,
                            vid360webm=vid360webm, vid240webm=vid240webm, vid144webm=vid144webm)

        else:
            return render_template('index.html')

    # If any error occurs in above field it will be redrecct to message
    except:
        return render_template('message.html', msg="Enter valid URL")


# After Clicking Download button this block will start exwcuting
@app.route('/downloadhandle', methods=['GET', 'POST'])
def downoadhandle():
    if request.method == 'POST':
        # it takes quality attribute from select button provided in html
        link = request.form['quality']

        # creating object of YouTube Class and providing link
        # this link is stored in sessin when user entered link to search

        yt = YouTube(str(session['link']))

        # takes all the available streams
        streams = yt.streams.filter(progressive=True)

        # matches/checks the user seleted quality stream in streams variable
        for stream in streams:

            # if it is available then download will start automatically
            if str(stream) == str(link):

                # files will only saved to d drive
                stream.download("d:/")

            # else it will redirect to message
            else:
                return render_template("message.html", msg="DownLoad Failed")

        # after successfull download it redirects to message
        return render_template("message.html", msg="Download successfull")


if __name__ == '__main__':
    app.run(debug=True)