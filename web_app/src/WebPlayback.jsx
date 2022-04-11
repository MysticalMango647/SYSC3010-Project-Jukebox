import React, { useState, useEffect } from 'react';

// create a track data type
const track = {
    name: "",
    album: {
        images: [
            { url: "" }
        ]
    },
    artists: [
        { name: "" }
    ]
}

function WebPlayback(props) {

    const [is_paused, setPaused] = useState(false);
    const [is_active, setActive] = useState(false);
    const [player, setPlayer] = useState(undefined);
    const [current_track, setTrack] = useState(track);

    useEffect(() => {
        
        //opens up an embedded spotify player script from spotify
        const script = document.createElement("script");
        script.src = "https://sdk.scdn.co/spotify-player.js";
        script.async = true;

        document.body.appendChild(script);

        //When the player is ready, pass it our token and start it
        window.onSpotifyWebPlaybackSDKReady = () => {
            
            const player = new window.Spotify.Player({
                name: 'Pi Jukebox',
                getOAuthToken: cb => { cb(props.token); },
                volume: 0.5
            });

            setPlayer(player);

            //Logs our device_id
            player.addListener('ready', ({ device_id }) => {
                console.log('Ready with Device ID', device_id);

            }); 

            player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID has gone offline', device_id);
            });

            //If playback state changes, update the webplayer with the latest states
            player.addListener('player_state_changed', ( state => {

                if (!state) {
                    return;
                }

                setTrack(state.track_window.current_track);
                setPaused(state.paused);

                player.getCurrentState().then( state => { 
                    (!state)? setActive(false) : setActive(true) 
                });

            }));

            //connects the player
            player.connect();

        };
    }, []);

   //if the player instance isn't active, return html to prompt user to swap playback
   if (!is_active) { 
       return (
            <>
               <div className="container">
                   <div className="main-wrapper">
                       <b> Instance not active. Transfer your playback using your Spotify app </b>
                    </div>
                </div>
            </>)
    }
    //If the player is active, display the album art and a couple of playback buttons
    else {
        return (
            <>
                <div className="container">
                    <div className="main-wrapper">

                        <img src={current_track.album.images[0].url} className="now-playing__cover" alt="" />

                        <div className="now-playing__side">
                            <div className="now-playing__name">{current_track.name}</div>
                            <div className="now-playing__artist">{current_track.artists[0].name}</div>

                            <button className="btn-spotify" onClick={() => { player.previousTrack() }} >
                                &lt;&lt;
                            </button>

                            <button className="btn-spotify" onClick={() => { player.togglePlay() }} >
                                { is_paused ? "PLAY" : "PAUSE" }
                            </button>

                            <button className="btn-spotify" onClick={() => { player.nextTrack() }} >
                                &gt;&gt;
                            </button>
                        </div>
                    </div>
                </div>
            </>
        );
    }
}

export default WebPlayback
