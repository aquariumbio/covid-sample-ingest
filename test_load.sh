for var in "$@"
do
    python make_random_samples.py -n "$var"
done
python load_samples.py -s laptop