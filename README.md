# An In-Active-Development Framework for Evaluating DALLE-3 (via ChatGPT) Image Output Quality

This project aims to show that DALLE-3's image output can be vastly improved. The end goal is to do so using mathematical, AI-based, and human-feedback metrics.

It requires some setup to get VMAF working with FFmpeg so that quality metrics can be used to gauge image output variation based on optimizations supplied via this repository.

Through unit testing, the goal is to prove that DALLE-3 is not fully optimized, and can indeed be super-charged, backed by 11 different statistical metrics and, also, AI-determined quality increases as well.

## Features
- Detailed metrics with standardization to help assess relative image quality
- Detailed instructions on how to run your own evals.
- Premade prompt enhancers that can be used with ChatGPT if you lack an API key or API gpt-4 access.
- Premade prompt enhancers that utilize gpt-3.5-turbo-16k if cost is a limiting factor.
- To run your own prompt enhancer, follow the guide below, then simply execute `[pythondistro] src/easy_prompt_enhancer/prompt_enhancer.py "Make a pretty cat"`` or with whatever base prompt you desire.

# Minimal Requirements
- Python 3.9.x (invoke using `pyenv` if you have multiple versions of Python. Even more details on how to set that up later).
- Download using `[system-package-manager] install pyenv`
- Run `pyenv local 3.9.x` or just `pyenv local 3.9`. It may take some time to install new Python versions.
- Setup a `venv` (install using, Python 3.9.x, `python -m install venv`)
- Check your python version by running `python --version`
- If it reads `3.9.x`, you're good to go.
- Install the requirements using `python -m pip install -r requirements.txt`
- You should now be able to run main.py, as well as generate your own prompts as mentioned above.

## It Starts with a Base prompt

This program aims to take a base prompt, extract the output, and save it. Then, the prompt is optimized via various possibilities (mostly through gpt-4-0314 model optimizations via the API) and the resultant, new, "improved" images are saved as well.

# Documentation for Setup for Building Dependencies
This project requires only a few dependencies, but setting up FFmpeg with VMAF support can be tricky. It requires a few steps.

First and foremost, create a `venv` using your preferered Python version from the root directory, source it, and then install dependencies using `[python-distro] -m pip install -r requirements.txt`

## Setup the Dependencies and First Build for libvmaf 
0. **Deactivate your current venv** by running `deactivate` if it is still active (as indicated in your terminal with `(venv)` displayed. If the command is not recognized; your venv is deactivated or you have not installed venv properly.)

1. Run `git clone https://github.com/Netflix/vmaf.git` to a directory of your choosing - preferableay within your project directory, perhaps within a venv. Wherever it is accessible - rememember the path you installed it to.
2. Navigate to your vmaf directory, and `cd` into it.
3. cd into `libvmaf` and then build `libvmaf`, which will be explained below.
4. Install pyenv via [system-package-manager] install pyenv
5. run `pyenv install 3.7.17` (minimum to get libvmaf working)
6. run `pyenv local 3.7.17`
7. Since you're in the libvmaf directory, create a venv (`python --version` first to check that you're using 3.7.17)
8. Once confirming the version, run `python -m venv venv`
9. Run `source venv/bin/activate`
10. Run `python -m pip install meson`
11. Run [package-manager] install nasm ninja doxygen
12. Run `meson build --buildtype release`
13. Run `ninja -vC build`
14. Run `ninja -vC build test` to see if all 13 tests are passed (as of 2023-10-26)
15. Once tests are passed (there may be build issues that arise), proceed to the next step.

## Setup FFmpeg with VMAF Support for Proper Metrics and Analysis

1. You will have to build FFmpeg yourself. Run the following command at your desired directory:
   ```
   git clone https://github.com/FFmpeg/FFmpeg.git
   ```

2. Navigate to the directory where you cloned FFmpeg and run the following commands sequentially:
   ```
   ./configure --enable-libvmaf
   make -j4
   make install
   ```

3. If everything goes well, after a build time of approximately 5-10 minutes on a decent computer, you should have VMAF support enabled.

4. To test this, run the following command, replacing `[path-to-ffmpeg-binary]` with the actual path to your FFmpeg binary:
   ```
   [path-to-ffmpeg-binary] -filters | grep vmaf
   ```
   You should see something like `libvmaf` in the output, likely near the bottom.

5. For macOS users, especially if using Homebrew, the typical path might be:
   ```
   /usr/local/bin/FFmpeg/ffmpeg -filters | grep vmaf
   ```

6. If you encounter permissions errors, navigate to the location of your FFmpeg binary (regardless of its location) and run:
   ```
   chmod -R +x $(pwd)
   ```

7. Once VMAF support is verified, use the following parameters in your program:
   ```
   --ffmpeg-location="/usr/local/bin/FFmpeg/ffmpeg"
   ```

8. Remember to adjust the paths based on your system!


## You Should Now Be Ready to Run This Program

Now, please enjoy running the evaluations and observing any quality increases, and feel free to provide compelling datasets and share them with the community. To contribute, if you want to be a collaborator, contact me directly at ahugi@uw.edu with "DALLE 3 EVALUATION REPO" as the title for a faster response.

## Generating Your Own Prompts
TBA:
- Better chat framework
- More customizability
- Incorporation of EasyGPT-3.5?

# TO DO
- Easier system for automatically generating images, grabbing them, and arranging them so they may be tested.
- Streamlined unit testing support.
- Add more metrics.
- Fine-tune the standardized formula.
- Incorporate human-sampled feedback.
- Use iterative prompting techniques.
- Explore cheaper models and compare results.
- Modularize better!