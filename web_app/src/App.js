import React, { useState, useEffect } from 'react';
import WebPlayback from './WebPlayback'
import Login from './Login'
import './App.css';

function App() {

  const [token, setToken] = useState('');

  //This use effect hook asynchronously awaits a token
  useEffect(() => {

    async function getToken() {
      const response = await fetch('/auth/token');
      const json = await response.json();
      setToken(json.access_token);
    }

    getToken();

  }, []);

  //If we dont have a token return the login page, if we do have a token return the webplayback page
  return (
    <>
        { (token === '') ? <Login/> : <WebPlayback token={token} /> }
    </>
  );
}


export default App;
