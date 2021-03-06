const express = require('express')
const request = require('request');
const dotenv = require('dotenv');

const port = 5000

global.access_token = ''

dotenv.config()

//Acquiring environment variables, to use yourself, edit the .env file with your corresponding ID, Secret and IP

var spotify_client_id = process.env.SPOTIFY_CLIENT_ID
var spotify_client_secret = process.env.SPOTIFY_CLIENT_SECRET
var ip = process.env.PI_IP

//

var spotify_redirect_uri = 'https://' + ip + ':3000/auth/callback'

var generateRandomString = function (length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

var app = express();

//Below are all the requests that the server handles


//This redirects the user to the spotify login page
app.get('/auth/login', (req, res) => {

  var scope = "streaming user-read-email user-read-private"
  var state = generateRandomString(16);

  //Pass on our credentials to the authorization portal, as well as give a redirect URI for once we login
  var auth_query_parameters = new URLSearchParams({
    response_type: "code",
    client_id: spotify_client_id,
    scope: scope,
    redirect_uri: spotify_redirect_uri,
    state: state
  })

  res.redirect('https://accounts.spotify.com/authorize/?' + auth_query_parameters.toString());
})

//If login is succesful, we will get redirected here, here we will acquire our access token
app.get('/auth/callback', (req, res) => {

  var code = req.query.code;

  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    form: {
      code: code,
      redirect_uri: spotify_redirect_uri,
      grant_type: 'authorization_code'
    },
    headers: {
      'Authorization': 'Basic ' + (Buffer.from(spotify_client_id + ':' + spotify_client_secret).toString('base64')),
      'Content-Type' : 'application/x-www-form-urlencoded'
    },
    json: true
  };

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      access_token = body.access_token;
      console.log(access_token)
      res.redirect('/')
    }
  });

})

//Here is where the SpeakerPi sends its change song request to
app.post('/play/:songID', (req, res) => {

  var token = access_token;

  var url = 'https://api.spotify.com/v1/me/player/play';

  var payload = { 
    body: {
      context_uri: req.params.songID,
      offset: {
        position: 0
      },
      position_ms: 0
    },
    headers: {
      'Content-Type' : 'application/json',
      'Authorization' : 'Bearer ' + token
   },
   json: true
  };
  request.put(url, payload);
  res.json({'Playing' : req.params.songID})
})

//This returns our access token
app.get('/auth/token', (req, res) => {
  res.json({ access_token: access_token})
})

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`)
})
