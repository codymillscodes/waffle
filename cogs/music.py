import spotipy
from config import (
    MUSIC_CHANNEL,
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    PLAYLIST_URI,
)
import discord
from discord.ext import commands
from discord import app_commands
from loguru import logger
from typing import Literal
from helpers.db import DB


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify = spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET,
                redirect_uri=SPOTIPY_REDIRECT_URI,
                scope="playlist-modify-public",
                open_browser=False,
                show_dialog=True,
            )
        )
        self.PLAYLIST_URI = PLAYLIST_URI

    async def check_existing_tracks(self, tracks: list):
        logger.info(f"Checking {len(tracks)} tracks.")
        logger.info(f"Tracks: {tracks}")
        db_tracks = {}
        for t in tracks:
            if await DB().find_track(t):
                track_query = self.spotify.track(t)
                db_tracks[
                    f"{track_query['artists'][0]['name']} - {track_query['name']}"
                ] = track_query["uri"]
            else:
                tracks.remove(t)
                logger.info(f"Removing {t} from tracks.")

        # logger.info(f"Playlist tracks: {playlist_tracks}")
        if len(db_tracks) > 0:
            await DB().add_to_playlist(db_tracks)
        logger.info(f"Found {len(tracks)} new tracks.")
        return tracks

    @app_commands.command(name="playlist_url", description="Get the playlist URL.")
    async def playlist_url(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "https://open.spotify.com/playlist/6xHdV7jlRcuon1AaUDVvNb?si=e1ae8290dd4247a8",
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        music_channel = await self.bot.fetch_channel(MUSIC_CHANNEL)
        if (
            message.channel.id == music_channel.id
            and "https://open.spotify.com/" in message.content
        ):
            try:
                logger.info(f"Got spotify link: {message.content}")
                if message.content.startswith("https://open.spotify.com/album/"):
                    album = self.spotify.album(message.content)
                    track_uris = []
                    logger.info(f"Got album: {album['name']}")
                    for track in album["tracks"]["items"]:
                        track_uris.append(track["uri"])

                    add_tracks = await self.check_existing_tracks(track_uris)

                elif message.content.startswith("https://open.spotify.com/track/"):
                    track = self.spotify.track(message.content)
                    logger.info(f"Got track: {track['name']}")
                    add_tracks = await self.check_existing_tracks([track["uri"]])

                if len(add_tracks) > 0:
                    logger.info(f"Adding {len(add_tracks)} tracks to playlist.")
                    await message.add_reaction("🧇")
                    self.spotify.playlist_add_items(PLAYLIST_URI, add_tracks)

            except spotipy.exceptions.SpotifyException:
                logger.error("SpotifyException")


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
