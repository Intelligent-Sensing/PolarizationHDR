#!/bin/bash
. /usr/share/Modules/init/bash
module add matlab/2019b
matlab -nodisplay -r "cd('hdrvdp3');addpath('utils');cd('examples');compare('$1','$2', '$3');exit"
# matlab -nodisplay -r "addpath('utils');cd('./examples');display_quality;exit"
