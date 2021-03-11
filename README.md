# sp-practice

This script calculates some statistics about the interaction traces from the [Rico dataset](http://interactionmining.org/rico)

### How to run
Clone repo and install dependencies:
```bash
git clone https://github.com/m-danya/sp-practice
cd sp-practice
pip3 install -r requirements.txt
```
Then run by ```./get_statistics.py``` or ```python3 get_statistics.py```

### Usage

Type ```./get_statistics.py -h``` to see help message 

### Sample output

```
$ ./get_statistics.py -i "/media/greedisgood/HDD/ML/Rico traces/" -n 250

100%|██████████████████████████████████████| 250/250 [00:22<00:00, 11.35it/s]


##############################

GUI STATISTICS

Mean number of elements in the GUI screen tree = 79.652
Mean number of clickable elements in the GUI screen tree = 14.413

Top-10 elements:

android.widget.LinearLayout: 18058 times
android.support.v7.widget.AppCompatTextView: 8659 times
android.widget.RelativeLayout: 8635 times
android.widget.TextView: 8150 times
android.widget.ImageView: 6612 times
android.widget.FrameLayout: 6000 times
android.view.View: 5338 times
android.support.v7.widget.AppCompatImageView: 4293 times
android.widget.Button: 1939 times
android.view.ViewStub: 1575 times

##############################

TRACES STATISTICS

Mean number of taps per trace = 3.844
Mean number of swipes per trace = 0.866
```

### Additional info
```clean_cache``` script [cleans the linux cache](https://unix.stackexchange.com/questions/87908/how-do-you-empty-the-buffers-and-cache-on-a-linux-system) to make script's performance testing fair when running multiple times consecutively
