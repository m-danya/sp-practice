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

Type ```./get_statistics.py -h``` to see help message.

You can also run unit tests by `pytest`

### Sample output

```
$ ./get_statistics.py -i "/media/greedisgood/HDD/ML/Rico traces/"
100%|███████████████████████████████████████| 9385/9385 [21:58<00:00,  7.12it/s]


##############################

GUI STATISTICS

Mean number of elements in the GUI screen tree = 96.135
Mean number of clickable elements in the GUI screen tree = 7.793

Top-10 elements:

android.widget.LinearLayout: 1059174 times
android.support.v7.widget.AppCompatTextView: 598281 times
android.widget.RelativeLayout: 513712 times
android.widget.TextView: 491851 times
android.widget.ImageView: 440930 times
android.widget.FrameLayout: 395973 times
android.support.v7.widget.AppCompatImageView: 369789 times
android.view.View: 326067 times
android.view.ViewStub: 85707 times
com.android.internal.policy.PhoneWindow$DecorView: 66805 times

##############################

TRACES STATISTICS

Mean number of taps per trace = 5.138
Mean number of swipes per trace = 1.300
Mean trace length = 6.438

```

### Additional info
```clean_cache``` script [cleans the linux cache](https://unix.stackexchange.com/questions/87908/how-do-you-empty-the-buffers-and-cache-on-a-linux-system) to make script's performance testing fair when running multiple times consecutively

### Several histograms
![1](research/1.jpg?raw=true)

![2](research/2.jpg?raw=true)

![3](research/3.jpg?raw=true)

![4](research/4.jpg?raw=true)
