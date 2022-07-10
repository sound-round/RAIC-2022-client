#!/bin/bash
ps aux | grep -ie aicup22 | awk '{print $2}' | xargs kill -9 || (true);
killall 0_cur;
killall 29_native;
true
