# Image Annotation and Augmentation
**Joanna Yu**

**Wednesday 4pm, Summer 2020**

## Introduction

### Part 1: Image Annotation
The task for this part is to annotate the Millennium Falcon and TIE Fighters in 384 images from Star Wars: The Force Awakens. `RectLabel` (available in the App Store) is used for the annotations, which are exported in the PASCAL VOC format. As this requires the use of a user interface, it is recommended that the normal workstation be used instead of the cloud or Jetson.

**Questions**
1. In the time allowed, how many images did you annotate?
> I finished annotating the entire set of 384 images.

2. Home many instances of the Millennium Falcon did you annotate? How many TIE Fighters?
> I annotated 308 instances of the Millennium Falcon and 295 instances of the TIE Fighters.

3. Based on this experience, how would you handle the annotation of large image data set?
> Annotating by hand is definitely infeasible for large image dataset. The quality of the annotation is also questionable.

4. Think about image augmentation? How would augmentations such as flip, rotation, scale, cropping, and translation effect the annotations?
> Some of these augmentations would change the bounding box coordinates and some would change the size. 

### Part 2: Image Augmentation
**Questions:**

Describe the following augmentations in your own words:

**Flip** - flips the image either horizontally (creating a mirror image) or vertically (creating an up-side down version).

**Rotation** - rotates the image by a certain degree of angle. 

**Scale** - zooms in or out of the picture. 

**Crop** - cuts out parts of the picture. 

**Translation** - shifts the pixels of the image by user specified amounts in the x and y directions. It works almost like rotation except rotation only spins the image based on the specified angle. For translation, depending on the argument, part of the image may be lost.  

**Noise** - adds noise to the image, which tends to alter the pixel colors and makes the image look blurry.

### Part 3: Audio Annotation
**Questions:**

Image annotations require the coordinates of the objects and their classes; in your option, what is needed for an audio annotation?
> Audio annotation require the start and end time of the audio clip and the class. 
