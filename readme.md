# Setup
- run `bin/bootstrap.sh`
- execute `source ~/.bashrc`

# Usage
`create_list.py (optional)"Name of List"`
If a name is not specified, the default in `config.yml` will be used.

# Algorithm
This tool generates a playlist of your full collection, with some limits applied from `config.yml`.
`playlist_maximums.tracks_per_artist` applies to all steps.

1. Favorited Tracks
2. Favorited Albums
3. Favorited Artists
    - Takes Artist's top tracks, limited by `favorite_artists.top_tracks`
    - Can be disabled by setting `favorite_artists.top_tracks` to 0