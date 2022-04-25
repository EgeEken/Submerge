# Submerge
Submerges a given section of the world by raising the sea level to the given height level, by increments of given increment level.

Usage:

- Go on topographic-map.com
- Find the area you want to submerge
- Inspect element
- Find and save the overlay image file from the source code of the website (ctrl + f "Overlay" helps a lot)
- Save the height values given to the right of the image
- Put the height values you saved in the y section of the regression calculator (https://stats.blue/Stats_Suite/polynomial_regression_calculator.html)
- Put 0 to 24 on the x section, from lowest to highest height value
- Save the resulting regression formula
- Plug the coefficients of the formula into the scale2height function

If you want to use a satelite image instead of just the topographic map:

- Go on google maps, get a satellite image of the same area
- Crop, center and maybe resize if you have to the satellite image correctly so that it lines up as accurately as possible with the topographic map overlay and has the same resolution

If you want to create a video from the calculated images, use the Image to MP4 file, input the names of the files except for the number at the end (ex: JakartaHQ.jpg_ if the created images are named as JakartaHQ.jpg_0, JakartaHQ.jpg_1, ...)

# Jakarta

https://user-images.githubusercontent.com/96302110/165179413-d00621f2-f9c8-45e8-a18f-3119ed977873.mp4

# Turkey

https://user-images.githubusercontent.com/96302110/165179431-fbcc2169-23e5-49f7-b248-52f653ddb8e2.mp4

# Progress of the school project i made this for

https://user-images.githubusercontent.com/96302110/165179599-4f936552-ac27-4e6c-892e-88c51036c2b5.mp4

