import sys
from keras.models import load_model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
import os
import keras.backend as K
from scipy.ndimage.interpolation import zoom
import tensorflow as tf
from vis.utils import utils
tf.compat.v1.disable_eager_execution()


#utility to get index of neural network layer 
def getLayerIndexByName(model, layername):
    for idx, layer in enumerate(model.layers):
        if layer.name == layername:
            return idx


#utility to plot map and other data
def plot_map(grads , classlabel , class_idx ,pred,img):
    fig, axes = plt.subplots(1,2,figsize=(14,5))
    axes[0].imshow(img)
    axes[1].imshow(img)
    i = axes[1].imshow(grads,cmap="jet",alpha=0.8)
    fig.colorbar(i)
    
    if(classlabel[class_idx] == 'covid' or classlabel[class_idx] == 'normal'):
        print("Predicted Class= ",classlabel[class_idx])
        print("Probability = ",2*(50-pred[0][0]*100))
    
    elif(classlabel[class_idx] == 'pneumonia'):
        print("Predicted Class= ",classlabel[class_idx])
        print("Probability = ",2*(pred[0][0]*100-50))
    

#data generator to load data
datagen = image.ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
)

#utility to predict and generate heat map of last layer  for covid v/s pneumonia
def predict_covid_and_plot(  X_test_batch , path, name_featureMap, name_gradcam, class_of_interest=1):
    new_image = X_test_batch[0]
    img=new_image
    # check prediction
    model_loaded = load_model(BASE_DIR+'\model_2.h5')
    model=model_loaded
    
    pred = model.predict(X_test_batch)
    # print(pred)
    seed_input =new_image
    classlabel = ['covid','pneumonia']
    penultimate_layer_idx = utils.find_layer_idx(model, "conv2d_8")
    if pred[0][0]<0.5:
        class_idx=0
    else:
        class_idx=1
    layer_idx = utils.find_layer_idx(model, "dense_4")
    ## feature map from the final convolusional layer
    final_fmap_index    = utils.find_layer_idx(model, 'conv2d_8')
    penultimate_output  = model.layers[final_fmap_index].output
    ## define derivative d loss^c / d A^k,k =1,...,512
    layer_input          = model.input
    loss                 = model.layers[layer_idx].output[:class_of_interest]
    grad_wrt_fmap        = K.gradients(loss,penultimate_output)[0]

    grad_wrt_fmap_fn     = K.function([layer_input,K.learning_phase()],
                                        [penultimate_output,grad_wrt_fmap])

    ## evaluate the derivative_fn
    fmap_eval, grad_wrt_fmap_eval = grad_wrt_fmap_fn([img[np.newaxis,...],0])

    # For numerical stability. Very small grad values along with small penultimate_output_value can cause
    # w * penultimate_output_value to zero out, even for reasonable fp precision of float32.
    grad_wrt_fmap_eval /= (np.max(grad_wrt_fmap_eval) + K.epsilon())

    # print(grad_wrt_fmap_eval.shape)
    alpha_k_c           = grad_wrt_fmap_eval.mean(axis=(0,1,2)).reshape((1,1,1,-1))
    Lc_Grad_CAM         = np.maximum(np.sum(fmap_eval*alpha_k_c,axis=-1),0).squeeze()

    ## upsampling the class activation map to th esize of ht input image
    scale_factor        = np.array(img.shape[:-1])/np.array(Lc_Grad_CAM.shape)
    _grad_CAM           = zoom(Lc_Grad_CAM,scale_factor)
    ## normalize to range between 0 and 1
    arr_min, arr_max    = np.min(_grad_CAM), np.max(_grad_CAM)
    grad_CAM            = (_grad_CAM - arr_min) / (arr_max - arr_min + K.epsilon())


    plt.figure(figsize=(20,5))
    plt.plot(alpha_k_c.flatten())
    plt.xlabel("Feature Map at Final Convolusional Layer")
    plt.ylabel("alpha_k^c")
    plt.title("The {}th feature map has the largest weight alpha^k_c".format(
        np.argmax(alpha_k_c.flatten())))
    plt.savefig(path+name_featureMap,dpi=100)    ############################## name of first image
    
    plot_map(grad_CAM,classlabel,class_idx,pred,img)
    plt.savefig(path+name_gradcam)                         ###########################name of second image
    return pred[0][0]

#utility to predict and generate heat map of last layer  for normal v/s pneumonia
def predict_normal_and_pneumonia(  X_test_batch , path, name_featureMap, name_gradcam, class_of_interest=1):
    new_image = X_test_batch[0]
    img=new_image
    # check prediction
    model_loaded = load_model(BASE_DIR+'\model.h5')
    model=model_loaded
    
    pred = model.predict(X_test_batch)
    
    seed_input =new_image
    classlabel = ['normal','pneumonia']
    penultimate_layer_idx = utils.find_layer_idx(model, "conv2d_28") 
    if pred[0][0]<0.5:
        class_idx=0
    else:
        class_idx=1
    layer_idx = utils.find_layer_idx(model, "dense_14")
    ## feature map from the final convolusional layer
    final_fmap_index    = utils.find_layer_idx(model, 'conv2d_28')
    penultimate_output  = model.layers[final_fmap_index].output
    ## define derivative d loss^c / d A^k,k =1,...,512
    layer_input          = model.input
    loss                 = model.layers[layer_idx].output[:class_of_interest]
    grad_wrt_fmap        = K.gradients(loss,penultimate_output)[0]

    grad_wrt_fmap_fn     = K.function([layer_input,K.learning_phase()],
                                        [penultimate_output,grad_wrt_fmap])

    ## evaluate the derivative_fn
    fmap_eval, grad_wrt_fmap_eval = grad_wrt_fmap_fn([img[np.newaxis,...],0])

    # For numerical stability. Very small grad values along with small penultimate_output_value can cause
    # w * penultimate_output_value to zero out, even for reasonable fp precision of float32.
    grad_wrt_fmap_eval /= (np.max(grad_wrt_fmap_eval) + K.epsilon())

    # print(grad_wrt_fmap_eval.shape)
    alpha_k_c           = grad_wrt_fmap_eval.mean(axis=(0,1,2)).reshape((1,1,1,-1))
    Lc_Grad_CAM         = np.maximum(np.sum(fmap_eval*alpha_k_c,axis=-1),0).squeeze()

    ## upsampling the class activation map to th esize of ht input image
    scale_factor        = np.array(img.shape[:-1])/np.array(Lc_Grad_CAM.shape)
    _grad_CAM           = zoom(Lc_Grad_CAM,scale_factor)
    
    ## normalize to range between 0 and 1
    arr_min, arr_max    = np.min(_grad_CAM), np.max(_grad_CAM)
    grad_CAM            = (_grad_CAM - arr_min) / (arr_max - arr_min + K.epsilon())
    plt.figure(figsize=(20,5))
    plt.plot(alpha_k_c.flatten())
    plt.xlabel("Feature Map at Final Convolusional Layer")
    plt.ylabel("alpha_k^c")
    plt.title("The {}th feature map has the largest weight alpha^k_c".format(
        np.argmax(alpha_k_c.flatten())))
    plt.savefig(path+name_featureMap,dpi=100)    ############################## name of first image
    
    plot_map(grad_CAM,classlabel,class_idx,pred,img)
    plt.savefig(path+name_gradcam)                         ###########################name of second image
    return pred[0][0]

if __name__ == "__main__":

    BASE_DIR = sys.argv[1]
    output_image_path = sys.argv[2]
    output_image_name_featureMap = sys.argv[3]
    output_image_name_gradcam = sys.argv[4]
    output_image_name_featureMap2 = sys.argv[5]
    output_image_name_gradcam2 = sys.argv[6]

    datagen = image.ImageDataGenerator(
        rescale = 1./255,
        shear_range = 0.2,
        zoom_range = 0.2,
        horizontal_flip = True,
    )

    TEST_PATH  = BASE_DIR + "/input/"  ###folder path of input image build two folder covid and pneumonia inside this and put file in any of these

    test_generator_single = datagen.flow_from_directory(
        TEST_PATH,
        target_size = (224,224),
        batch_size = 1,
        class_mode = 'binary')

    X_test_batch,Y_test_batch = next(test_generator_single)

    isCovid = (predict_covid_and_plot(X_test_batch, output_image_path, output_image_name_featureMap, output_image_name_gradcam))   #it will return an integer and generate two images
    isPneumonia = (predict_normal_and_pneumonia(X_test_batch, output_image_path, output_image_name_featureMap2, output_image_name_gradcam2)) #it will return an integer and generate two images

