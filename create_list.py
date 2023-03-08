from components.library_parser import LibraryParser
from components.playlist_manager import PlaylistManager
from connector.auth import Auth
import sys, tidalapi, argparse


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Tidal Full Collection Playlist",
        description="If you've ever wanted to shuffle your whole TIDAL library, you're in the right place!",
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Specify this to set the playlist's name.",
        default="Full Collection",
    )  # positional argument
    parser.add_argument(
        "-d",
        "--description",
        help="Specify this to set the playlist's description.",
        default="The entire collection!",
    )  # option that takes a value
    return parser.parse_args()


def setup():
    auth = Auth("session_data.json")
    session = auth.session
    favorites = tidalapi.Favorites(session, session.user.id)
    return LibraryParser(favorites), PlaylistManager(session=auth.session)


def main():
    lib_parser, manager = setup()
    manager.create_full_collection()
    args: argparse.Namespace = handle_args()
    playlist = manager.create_list(args.title, args.description)
    manager.update_from_parser(playlist, lib_parser)


if __name__ == "__main__":
    main(sys.argv)
