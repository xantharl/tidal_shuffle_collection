if [[ $PYTHONPATH != *$(pwd)* ]]; then
  echo "export PYTHONPATH=$PYTHONPATH:~/repos/tidal_shuffle_collection" >> ~/.bashrc
  echo "Adding repo to PYTHONPATH, run 'source ~/.bashrc'"
fi

pip install -r requirements.txt