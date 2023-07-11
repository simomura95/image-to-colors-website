# Image to colors website
*(the website is deployed on-demand, so it could take some minutes to load the page)*

Flask application to extract the top 10 most used colors from an image with their hexadecimal codes.

The image is uploaded by the user, opened with the Pillow package and converted to a JPEG file (needed if the original image is a .png file, with 4 channels).<br>
It is then converted to a Numpy array and subsequently to a Pandas dataframe. Each pixel of the image is one row of the dataframe.<br>
Through operations on the dataframe, pixel colors are counted and sorted, finding the most popular 10.<br>
The hexadecimal codes are easily obtained from the RGB values.

In the end, the website shows the image uploaded, 10 strips with the most popular colors with their hexadecimal codes, and a button to upload a new image.
![image-to-colors](https://github.com/simomura95/image-to-colors-website/assets/134875169/ee1070a8-2f2a-4bda-b956-68895e83daa6)

Occasionally, with some pictures the process fails to complete and a timeout occurs.
I think it's because of the limited memory of the hosting service that I use for my web application, as the problem never happens with the same image running the app on my pc.
