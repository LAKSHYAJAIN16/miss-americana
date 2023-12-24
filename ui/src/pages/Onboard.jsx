import React from "react";
import Logo from "../assets/crown.png"; // Tell webpack this JS file uses this image
import { SpotifyAuth, Scopes } from "react-spotify-auth";
import "react-spotify-auth/dist/index.css"; // if using the included styles
import Cookies from "js-cookie";
import keys from "../missamericana.config";

export default function Onboard() {
  async function setToken(token) {
    Cookies.set("spotifyAuthToken", token);
    console.log(token);

    // Send request to retrieve profile information
    const result = await fetch("https://api.spotify.com/v1/me", {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });
    const body = await result.json();

    // Filter out body a little bit
    const user = {
      name: body.display_name,
      email: body.email,
      id: body.id,
    };
    Cookies.set("spotifyProfile", JSON.stringify(user));
    console.log(user);

    // Get Playlists
    await getPlaylists(token);

    // Get Liked Songs
    await getLikedSongs(token);

    // Redirect to the homepage
    window.location.replace("/home");
  }

  async function getLikedSongs(token) {
    // Initial result
    const result3 = await fetch(
      "https://api.spotify.com/v1/me/tracks?limit=50",
      {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    const body3 = await result3.json();

    // Declare likedSongs array
    const likedSongs = [];
    for (let kk = 0; kk < body3.items.length; kk++) {
      const song = body3.items[kk];
      const artists = [];
      let art_string = "";
      for (let mmm = 0; mmm < song.track.artists.length; mmm++) {
        const artist = song.track.artists[mmm];
        artists.push({
          id: artist.id,
          name: artist.name,
        });
        art_string += artist.name;
        art_string += ", ";
      }

      const song_formatted = {
        name: song.track.name,
        e: song.track.explicit,
        id: song.track.id,
        art_string: art_string.trimEnd().substring(0, art_string.length - 2),
        artists: artists,
        image: song.track.album.images[0].url,
        album: {
          name: song.track.album.name,
          id: song.track.album.id,
        },
      };
      likedSongs.push(song_formatted);
    }

    // Check if the total is greater than 50
    const total = body3.total;
    if (total > 50) {
      const result4 = await fetch(
        "https://api.spotify.com/v1/me/tracks?offset=50&limit=50",
        {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const body4 = await result4.json();
      for (let kk = 0; kk < body4.items.length; kk++) {
        const song = body4.items[kk];
        const artists = [];
        let art_string = "";
        for (let mmm = 0; mmm < song.track.artists.length; mmm++) {
          const artist = song.track.artists[mmm];
          artists.push({
            id: artist.id,
            name: artist.name,
          });
          art_string += artist.name;
          art_string += ", ";
        }

        const song_formatted = {
          name: song.track.name,
          e: song.track.explicit,
          id: song.track.id,
          art_string: art_string.trimEnd().substring(0, art_string.length - 2),
          artists: artists,
          image: song.track.album.images[0].url,
          album: {
            name: song.track.album.name,
            id: song.track.album.id,
          },
        };
        likedSongs.push(song_formatted);
      }
    }

    // Now, format array
    console.log(likedSongs);

    // Send Request for our song buffer to Backend
    const backendRequest = await fetch(keys.backend + "/check", {
      method: "POST",
      body: JSON.stringify(likedSongs),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    const backendBody = await backendRequest.json();
    console.log(backendBody);
    localStorage.setItem("BUF_LIKED_SONGS", JSON.stringify(likedSongs));
  }

  async function getPlaylists(token) {
    const result2 = await fetch(
      "https://api.spotify.com/v1/me/playlists?limit=50",
      {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    const body2 = await result2.json();

    // Filter out the data we don't need
    const playlists = [];
    for (let kk = 0; kk < body2.items.length; kk++) {
      const play = body2.items[kk];
      playlists.push({
        name: play.name,
        cover: play.images[0].url || "",
        owner: play.owner.display_name,
        id: play.id,
        description: play.description,
      });
    }

    // Check if the total is greater than 50
    const total = body2.total;
    if (total > 50) {
      const result3 = await fetch(
        "https://api.spotify.com/v1/me/playlists?offset=50&limit=50",
        {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const body3 = await result3.json();

      // Filter out the data we don't need
      for (let kk = 0; kk < body3.items.length; kk++) {
        const play = body3.items[kk];
        playlists.push({
          name: play.name,
          cover: play.images[0].url || "",
          owner: play.owner.display_name,
          id: play.id,
          description: play.description,
        });
      }
    }
    console.log(playlists);
    localStorage.setItem("spotifyPlaylists", JSON.stringify(playlists));
  }

  return (
    <div className="center flex flex-col justify-center items-center">
      <img src={Logo} className="h-20 w-20" />
      <h1 className="-mt-10 text-8xl font-bold text-pink-500 text-center font-dancing ">
        miss americana
      </h1>

      <SpotifyAuth
        redirectUri="http://localhost:1420/onboard"
        clientID="7f9b0d52c40944878346f258892e14d3"
        onAccessToken={(token) => setToken(token)}
        scopes={[
          Scopes.userReadPrivate,
          Scopes.userReadEmail,
          Scopes.playlistReadPrivate,
          Scopes.userLibraryRead,
          Scopes.streaming,
          Scopes.userReadPrivate,
        ]}
      />
    </div>
  );
}
