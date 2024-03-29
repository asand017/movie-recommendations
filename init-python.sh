python3 -m venv venv
source venv/bin/activate
python3 -m pip install tensorflow
python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"