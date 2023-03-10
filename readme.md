# Setup
- run `bin/bootstrap.sh`
- execute `source ~/.bashrc`

# Usage
`python create_list.py -h"` shows usage instruction. Both arguments are optional.

# Algorithm
This tool generates a playlist of your full collection, with some limits applied from `config.yml`.
`playlist_maximums.tracks_per_artist` applies to all steps.

1. Favorited Tracks
2. Favorited Albums
3. Favorited Artists
    - Takes Artist's top tracks, limited by `favorite_artists.top_tracks`
    - Can be disabled by setting `favorite_artists.top_tracks` to 0

# Future Plans
Album caching or multithreading - Unless there's a better way I haven't found, you have to hit `album/id/tracks` for each album. This can take quite some time in large libraries.

Make this run out of github so we don't need users to clone the repo.