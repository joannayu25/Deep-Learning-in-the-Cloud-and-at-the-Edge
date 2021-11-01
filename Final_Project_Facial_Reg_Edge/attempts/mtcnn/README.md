# W251 Final Project - Jetson Inference

## Dockerfile.opencv-mtcnn
This dockerfile tries to build an image for mtcnn without using pip, but the build is unsuccessful and would stop in the `RUN ./create_engines line`. The error is CUDA initialization failure with error 38 and could not be resolved using other base images. However, installing mtcnn on the TX2 using the same instruction is successful. But this was resolved close to the project deadline and we decided not to modify the pipeline and focus on other bottleneck in the pipeline.

## Dockerfile.mtcnn
This dockerfile tries to build an image for mtcnn without using `pip`, but the build is unsuccessful and would stop in the `RUN ./create_engines` line. The error is `CUDA initialization failure with error 38` and could not be resolved using other base images. However, installing mtcnn on the TX2 using the same instruction is successful. But given time constraints, we decided not to modify the pipeline and focus on other bottleneck in the pipeline.

## Dockerfile.jetson-inference
This dockerfile tries to install Jetson Inference using Dusty's repo instruction. However, the build cannot complete due to an error with `gl-display-test`. As reported in the class Slack channel, Dusty seems to have made a recent change to his repo that caused this error. The build will only finish if we add flag `-i` to the `make` and `make install` lines. But even though the build could finish, we could not run the demo. The same error is encountered when installing directly on the TX2.
