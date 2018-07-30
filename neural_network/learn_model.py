from __future__ import print_function
import numpy as np
from chainer import datasets, iterators, optimizers, serializers
from chainer.dataset import concat_examples
import chainer.functions as F
import chainer.links as L
from utils import loadData
from muji_model import MujiNN

train, test = loadData(7000)

batchsize = 50

train_iter = iterators.SerialIterator(train, batchsize)
test_iter = iterators.SerialIterator(test, batchsize, repeat=False, shuffle=False)

model = MujiNN()

optimizer = optimizers.MomentumSGD(lr=0.01, momentum=0.9)
optimizer.setup(model)

max_epoch = 100

pLoss = 10.0
# while train_iter.epoch < max_epoch:
while pLoss > 0.0001:

    # ---------- One iteration of the training loop ----------
    train_batch = train_iter.next()
    data_train, target_train = concat_examples(train_batch)

    # Calculate the prediction of the network
    prediction_train = model(data_train)

    # Calculate the loss with softmax_cross_entropy
    loss = F.softmax_cross_entropy(prediction_train, target_train)
    pLoss = float(loss.data)

    # Calculate the gradients in the network
    model.cleargrads()
    loss.backward()

    # Update all the trainable paremters
    optimizer.update()
    # --------------------- until here ---------------------

    # Check the validation accuracy of prediction after every epoch
    if train_iter.is_new_epoch:  # If this iteration is the final iteration of the current epoch

        # Display the training loss
        print('epoch:{:02d} train_loss:{:.04f} '.format(
            train_iter.epoch, float(loss.data)), end='')

        test_losses = []
        test_accuracies = []
        while True:
            test_batch = test_iter.next()
            text_test, target_test = concat_examples(test_batch)

            # Forward the test data
            prediction_test = model(text_test)

            # Calculate the loss
            loss_test = F.softmax_cross_entropy(prediction_test, target_test)
            test_losses.append(loss_test.data)

            # Calculate the accuracy
            accuracy = F.accuracy(prediction_test, target_test)
            test_accuracies.append(accuracy.data)

            if test_iter.is_new_epoch:
                test_iter.epoch = 0
                test_iter.current_position = 0
                test_iter.is_new_epoch = False
                test_iter._pushed_position = None
                break

        print('val_loss:{:.04f} val_accuracy:{:.04f}'.format(
            np.mean(test_losses), np.mean(test_accuracies)))

serializers.save_npz('./neural_network/my_mnist.model', model)