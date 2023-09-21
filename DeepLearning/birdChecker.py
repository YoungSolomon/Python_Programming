#Function that downloads images to train a model to discern between pictures of birds and non birds

#Import library to search images
from duckduckgo_search import ddg_images
from fastcore.all import *

#Write a function to search images
def image_search(term, max_images = 30):
    print(f"Searching for '{term}'")
    return L(ddg_images(term, max_results = max_images)).itemgot('image')

#calls our image_search function to grab the first bird photo returned by duck duck go
urls = image_search('bird photos', max_images = 1)
urls[0]

#Import library to download the url and open it
from fastdownload import download_url
dest = 'bird.jpg'

#Calls the function to download the first bird image returned
download_url(urls[0], dest, show_progress = False)

#Import library and open the first image downloaded by our helper function
from fastai.vision.all import *
image = Image.open(dest)
image.to_thumb(256, 256)

#call helper function to download and open non bird pics to verify functionality
download_url(image_search("forest photos", max_images = 1)[0], "forest_photos.jpg", show_progress = False )
Image.open("forest_photos.jpg").to_thumb(256,256)

#Creates a directory to divvy up birds and non birds so our model has data to be trained on
searches = "forest", "bird"
path = Path('bird_no_bird')
from time import sleep

#Runs a loop to search for photos and birds and forests in different lightings to give the model more data to work with
for o in searches:
    directory = (path/o)
    directory.mkdir(exist_ok = True, parents = True)
    download_images(directory, urls = image_search(f'{o} photo'))
    sleep(10)
    download_images(directory, urls = image_search(f'{o} sun photo'))
    sleep(10)
    download_images(directory, urls = image_search(f'{o} shade photo'))
    sleep(10)
    resize_images(path/o, max_size = 400, directory = path/o)

#Checks if the download image is corrupted and if so, unlinks it from the directory to avoid skewing model 
corrupt = verify_images(get_image_files(path))
corrupt.map(Path.unlink)
len(corrupt)

#Creates a data block, has a training set of data and a validation set to ensure accuracy of the models results
dataBlock = DataBlock(
    #Input is images and output is categories (bird/no bird)
    blocks = (ImageBlock, CategoryBlock),
    #returns all the images in the directory (our models input)
    get_items = get_image_files,
    #Splits the data into training and validation, 20% split to validation set)
    splitter = RandomSplitter(valid_pct = 0.2, seed = 42),
    #y values are the labels, in this case the names of the image folders containing bird and non bird pictures
    get_y = parent_label,
    #resizes the images by squishing rather than cropping and risking chopping the image into something unrecognizable
    item_tfms = [Resize(192, method = "squish")]
).dataloaders(path, bs = 32)

dataBlock.show_batch(max_n = 6)

#Implements model with a computer vision model and library for fine tuning pretrained ai
learn = vision_learner(dataBlock, resnet18, metrics = error_rate)
learn.fine_tune(3)

is_bird,_,probs = learn.predict(PILImage.create("bird.jpg"))
print(f'This is a: {is_bird}.')
print(f'Probability this is a bird: {probs[0]:.4f}')



