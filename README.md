# sd15-recommended-res-calc
A simple script (also a Custom Node in ComfyUI), to calculate and automatically set the recommended initial latent size for Stable Diffusion 1.5 image generation and its Upscale Factor based on the desired Final Resolution output.

**Usage showcase in ComfyUI**
![image](https://github.com/marhensa/sd15-recommended-res-calc/assets/816600/f8bca01a-7f6a-4a5b-9ee7-c85c7ceac9c5)

Example Workflow of usage in ComfyUI : [JSON](https://github.com/marhensa/sd15-recommended-res-calc/blob/main/_use-case-example-comfyui-nodes/sd15-recommended-res-calc_upscale-case.json) / [PNG](https://github.com/marhensa/sd15-recommended-res-calc/blob/main/_use-case-example-comfyui-nodes/sd15-recommended-res-calc_upscale-case.png)

**To install it as ComfyUI custom node using manual Git Clone Operation** :
1. Go to this folder /ComfyUI/custom_nodes/
2. Open command prompt to that folder, type this line below:
3. git clone https://github.com/marhensa/sd15-recommended-res-calc.git
4. Restart ComfyUI, now this custom node "Recommended Resolution Calculator SD15" is located in "utils" node section
5. Usage: DesiredXSIZE and DesiredYSIZE is your TARGET FINAL RESOLUTION, Upscale Factor OR Reverse Upscale Factor is used as example above

As standalone (Not Using ComfyUI):
1. Download (Click green button Code > Download ZIP) from repo. Or this [direct link](https://github.com/marhensa/sd15-recommended-res-calc/archive/refs/heads/main.zip).
2. Make sure .Py and .Bat file on same folder
3. Double click .Bat file! (.Sh for Linux)
4. Input your desired Final Resolution
5. You'll get recommended SD 1.5 Initial Image Size, and its upscale factor to reach the Final Resolution.
