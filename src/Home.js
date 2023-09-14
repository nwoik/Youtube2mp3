import axios from "axios";
import React, { useRef, useState } from "react";
import {Link} from "react-router-dom";

function Home() {
    const urlRef = useRef();
    const [urlResult, setUrlResult] = useState(null);

    function getUrlId(url){
        var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
        var match = url.match(regExp);
        return (match&&match[7].length==11)? match[7] : false;
    }

    function search(e) {
        e.preventDefault()
        const url = urlRef.current.value
        const youtubeID = getUrlId(url)
        console.log(youtubeID);

        const options = {
            method: 'get',
            url: 'https://youtube-mp3-download1.p.rapidapi.com/dl',
            
            headers: {
                'X-RapidAPI-Key': '2540ac3983msh66a4bc53b267c2cp10cfcbjsnde2485a06219',
                'X-RapidAPI-Host': 'youtube-mp3-download1.p.rapidapi.com'
            },
            params: {
                id: youtubeID
            }
          }

        axios(options)
            .then(res => setUrlResult(res.data.link))
            .catch(err => console.log(err))
    }

    function downloadMp3(e) {
        e.preventDefault()
        console.log(urlResult)
    }

    return (
        <div>
            <nav>
                <Link to="/" className="home"><h1>Youtube Media Converter</h1></Link>
            </nav>
            <form className="url" onSubmit={search}>
                <label>Download or transform YouTube videos into any audio format with a click</label>
                <input type="text" className="input-link" placeholder="Paste a Youtube link" ref={urlRef}></input>
                <button className="search" type="submit">Search</button>
            </form>

            
            <ol className="instructions">
                <li>Open <a href="https://www.youtube.com">YouTube</a> and search for the video you would like to download</li>
                <li>Click share and copy the URL</li>
                <li>Paste the URL above and click Search</li>
                <li>Pick a file format you want to download</li>
            </ol>
            
            <div className="formats">
                <form>
                    <label>Video</label>
                    {/* <select className="video-formats">
                        <option value="mp4">mp4</option>
                        <option value="mov">mov</option>
                        <option value="webm">webm</option>
                        <option value="mpeg">mpeg</option>
                        <option value="mpa">mpa</option>
                    </select> */}
                    <button>Download Video</button>
                </form>
                <form onSubmit={downloadMp3}>
                    <label>Audio</label>
                    {/* <select className="audio-formats">
                        <option value="mp3">mp3</option>
                        <option value="wav">wav</option>
                        <option value="aac">aac</option>
                        <option value="aiff">aiff</option>
                        <option value="flac">flac</option>
                    </select> */}
                    <button type="submit">Download Audio</button>
                </form>
            </div>
        </div>
    )
}

export default Home;