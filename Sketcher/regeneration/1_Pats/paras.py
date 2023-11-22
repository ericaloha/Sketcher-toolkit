'''
1. local paras
'''
data_dir = 'C:\\Users\\shang\\Desktop\\Generative\\LSTM_RNN_Single_Pat\\input\\mapping'  # data directory containing input.txt
save_dir = 'C:\\Users\\shang\\Desktop\\Generative\\LSTM_RNN_Single_Pat\\input\\save\\Random'  # directory to store models
seq_length = 30  # sequence length
sequences_step = 1  # step to create sequences

file_list = ["3"]

'''
2. model paras
'''


'''
    default
    rnn_size = 256  # size of RNN
    batch_size = 32  # minibatch size
    num_epochs = 50  # number of epochs
    learning_rate = 0.001  # learning rate
'''
rnn_size = 256  # size of RNN
batch_size = 32  # minibatch size
num_epochs = 50  # number of epochs
learning_rate = 0.001  # learning rate
