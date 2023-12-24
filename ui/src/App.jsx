import { useState, useEffect } from "react";
import "./App.css";
import Cookies from "js-cookie";

function App() {
  const [token, setToken] = useState();
  const [user, setUser] = useState();
  const [playlists, setPlaylists] = useState();
  const [songs, setSongs] = useState();

  useEffect(() => {
    setToken(Cookies.get("spotifyAuthToken"));
    setUser(JSON.parse(Cookies.get("spotifyProfile")));
    setPlaylists(JSON.parse(localStorage.getItem("spotifyPlaylists")));
    setSongs(JSON.parse(localStorage.getItem("BUF_LIKED_SONGS")));
  }, [playlists, user, token, songs]);

  return <p className="text-white font-josepfin ml-5 mt-5 text-3xl">Welcome, {user.name}</p>;
}

export default App;
