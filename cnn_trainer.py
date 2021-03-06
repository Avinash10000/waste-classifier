import preprocess_images
from constants import *

#tf and tf keras
import tensorflow as tf
import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import json


#imports needed to build model
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from keras.regularizers import l2


#preprocess the data and load it up
(train_X, train_Y, train_Y_one_hot, class_names) = preprocess_images.load_dataset(
    'processed_datasets/clumped_kitchen_train_data_v3'+str(IMG_WIDTH)
    +'x' + str(IMG_HEIGHT)+ 'x'+str(CHANNELS) +'.h5')
(test_X, test_Y, test_Y_one_hot, class_names_test) = preprocess_images.load_dataset(
    'processed_datasets/clumped_kitchen_test_data_v3'+str(IMG_WIDTH)
    +'x' + str(IMG_HEIGHT)+ 'x'+str(CHANNELS) + '.h5')

#used to determine number of output classes:
num_classes = len(class_names)

#Split train data set into train, cross validation
train_X,valid_X,train_label,valid_label = \
    train_test_split(train_X, train_Y_one_hot, test_size=0.2, random_state=13)
print("train,valid shape", train_X.shape, valid_X.shape, train_label.shape,valid_label.shape)
print(test_X.shape, test_Y_one_hot.shape, test_Y.shape)

#some parameters used to test different models
reg_lambda = 0.001
dropout = True

# # build models:

'''custom model'''
#build a sequential model i.e. a model with layers arranged in a linear manner
waste_model=Sequential()
#Add the first convolutional layer, which helps smooth over the image
waste_model.add(Conv2D(32, kernel_size=(3,3), activation='linear', 
    input_shape=(IMG_WIDTH,IMG_HEIGHT,CHANNELS),padding='same'))
#add a leaky relu layer which essentially turns the negative numbers to 0, and leaves the positive pixel 
#values the same
waste_model.add(LeakyReLU(alpha=0.1))
#a max pooling layer which halves the size of th image
waste_model.add(MaxPooling2D((2,2),padding='same'))
# a dropout layer to reduce over fitting - here dropping out 50% 
waste_model.add(Dropout(0.5))
waste_model.add(Conv2D(128,(3,3),activation='linear',padding='same'))
waste_model.add(LeakyReLU(alpha=0.1))
waste_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
waste_model.add(Dropout(0.25))
waste_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
waste_model.add(LeakyReLU(alpha=0.1))                  
waste_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
waste_model.add(Dropout(0.4))
#flatten the 2d layers to 1d layers
waste_model.add(Flatten())
#add a  multilayer perceptron layer
waste_model.add(Dense(128, activation='linear', activity_regularizer=l2(reg_lambda)))
waste_model.add(LeakyReLU(alpha=0.1))  
waste_model.add(Dropout(0.5))         
#output layer
waste_model.add(Dense(num_classes, activation='softmax'))

'''custom model with no dropout or regularization'''
# waste_model=Sequential()
# waste_model.add(Conv2D(32, kernel_size=(3,3), activation='linear', 
#     input_shape=(IMG_WIDTH,IMG_HEIGHT, CHANNELS),padding='same'))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(MaxPooling2D((2,2),padding='same'))
# waste_model.add(Conv2D(128,(3,3),activation='linear',padding='same'))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
# waste_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
# waste_model.add(LeakyReLU(alpha=0.1))                  
# waste_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
# waste_model.add(Flatten())
# waste_model.add(Dense(128, activation='linear'))
# waste_model.add(LeakyReLU(alpha=0.1))            
# waste_model.add(Dense(num_classes, activation='softmax'))

'''hindawi model'''
# waste_model=Sequential()
# waste_model.add(Conv2D(96, kernel_size=(11,11), activation='linear', 
#     input_shape=(IMG_WIDTH,IMG_HEIGHT, CHANNELS),padding='same', strides=4))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(MaxPooling2D((3,3), padding="same"))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(Conv2D(256,(5,5),activation='linear',padding='same'))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(MaxPooling2D((3,3), padding="same", strides=2))
# waste_model.add(Conv2D(384,(3,3),activation='linear',padding='same'))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(Conv2D(384,(3,3),activation='linear',padding='same'))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(Conv2D(256,(3,3),activation='linear',padding='same'))
# waste_model.add(LeakyReLU(alpha=0.1))
# waste_model.add(MaxPooling2D((3,3), padding="same", strides=2))
# waste_model.add(Dropout(0.5))
# waste_model.add(Flatten())
# waste_model.add(Dense(512, activation='linear'))
# waste_model.add(Dropout(0.5))
# waste_model.add(Dense(512, activation='linear'))
# waste_model.add(Dense(num_classes, activation='softmax'))


'''transfer learning model inception'''
# from keras.applications import InceptionV3
# from keras.models import Model
# original_model = InceptionV3()
# neck_input = original_model.get_layer(index=0).input
# neck_output = original_model.get_layer(index=-2).output
# neck_model = Model(inputs = neck_input, outputs = neck_output)

# for layer in neck_model.layers:
#     layer.trainable = False

# waste_model = Sequential()
# waste_model.add(neck_model)
# waste_model.add(Dense(128,activation='linear'))
# # waste_model.add(Dense(1024, activation='relu'))
# waste_model.add(Dense(num_classes,activation='softmax'))

'''various transfer loarning models:'''
# from keras.applications import MobileNetV2, InceptionResNetV2, DenseNet121, ResNet50, InceptionV3
# from keras.models import Model

# models = [MobileNetV2, InceptionResNetV2, DenseNet121, ResNet50, InceptionV3]
# model_names = ['mobileNetV2', 'inceptionResNetV2', 'denseNet121', 'resNet50', 'inceptionV3']
# for i, m in enumerate(models):
#     input_tensor = Input(shape=(IMG_WIDTH,IMG_HEIGHT, CHANNELS))
#     original_model = MobileNetV2(input_tensor=input_tensor, weights='imagenet')

#     neck_input = original_model.get_layer(index=0).input
#     neck_output = original_model.get_layer(index=-2).output
#     neck_model = Model(inputs = neck_input, outputs = neck_output)

#     for layer in neck_model.layers:
#         layer.trainable = False

#     waste_model = Sequential()
#     waste_model.add(neck_model)
#     # waste_model.add(Dense(1024,activation='relu'))
#     # waste_model.add(Dropout(0.25))
#     # waste_model.add(Dense(1024, activation='relu'))
#     waste_model.add(Dense(num_classes,activation='softmax'))

#     #compile model
#     waste_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),
#         metrics=['accuracy'])
#     waste_model.summary()
#     waste_train = waste_model.fit(train_X, train_label, batch_size=BATCH_SIZE,
#     epochs=EPOCHS,verbose=1,validation_data=(valid_X, valid_label))
#     model_name = "transfer_learning_" + model_names[i] + "_"+str(IMG_HEIGHT)+ "x" + str(IMG_WIDTH)
#     waste_model.save("trained_models/" + model_name + ".h5py")
#     history = waste_train.history
#     with open('model_history/'+model_name+".json", 'w') as f:
#         json.dump(history,f)
#     test_eval = waste_model.evaluate(test_X, test_Y_one_hot, verbose=0)
#     print('Test loss:', test_eval[0])
#     print('Test accuracy:', test_eval[1])


# input_tensor = Input(shape=(IMG_WIDTH,IMG_HEIGHT, CHANNELS))
# original_model = MobileNetV2(input_tensor=input_tensor, weights='imagenet')

# neck_input = original_model.get_layer(index=0).input
# neck_output = original_model.get_layer(index=-2).output
# neck_model = Model(inputs = neck_input, outputs = neck_output)

# for layer in neck_model.layers:
#     layer.trainable = False

# waste_model = Sequential()
# waste_model.add(neck_model)
# waste_model.add(Dense(1024,activation='relu'))
# waste_model.add(Dense(1024, activation='relu'))
# waste_model.add(Dense(num_classes,activation='softmax'))

#compile model
waste_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),
    metrics=['accuracy'])
waste_model.summary()


#train model
waste_train = waste_model.fit(train_X, train_label, batch_size=BATCH_SIZE,
    epochs=EPOCHS,verbose=1,validation_data=(valid_X, valid_label))

#save trained model for later
model_name = "waste_model_clumped_v3"+("_3d" if CHANNELS==3 else "_bw") + ("_dropout" if dropout else "") + \
    ("_reg"+str(reg_lambda) if reg_lambda!=0 else "") +"_in" + str(IMG_WIDTH)+"x"+str(IMG_HEIGHT)
print("saved to:",model_name)
waste_model.save("trained_models/" + model_name + ".h5py")

#save history
history = waste_train.history
with open('model_history/'+model_name+".json", 'w') as f:
    json.dump(history,f)

#evaluate model accuracy and loss
test_eval = waste_model.evaluate(test_X, test_Y_one_hot, verbose=0)
print('Test loss:', test_eval[0])
print('Test accuracy:', test_eval[1])

#show graphs for training history
accuracy = waste_train.history['acc']
val_accuracy = waste_train.history['val_acc']
loss = waste_train.history['loss']
val_loss = waste_train.history['val_loss']
epochs_list = range(len(accuracy))
plt.plot(epochs_list, accuracy, 'bo', label='Training accuracy')
plt.plot(epochs_list, val_accuracy, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs_list, loss, 'bo', label='Training loss')
plt.plot(epochs_list, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()

#make predictions
predicted_classes = waste_model.predict(test_X)
predicted_classes = np.argmax(np.round(predicted_classes),axis=1)

#find the number correct and incorrect
correct = np.where(predicted_classes==test_Y)[0]
incorrect = np.where(predicted_classes!=test_Y)[0]


#do a classification report
from sklearn.metrics import classification_report
print(classification_report(test_Y, predicted_classes, target_names=class_names))
print("num_correct: {}, num_incorrect: {}".format(len(correct), len(incorrect)))
