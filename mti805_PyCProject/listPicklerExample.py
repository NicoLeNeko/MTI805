# From https://stackoverflow.com/a/17796482/7243716 or https://stackoverflow.com/questions/17796446/convert-a-list-to-a-string-and-back#17796482
import sys

example_list = [[1, 1], [2, 2], [3, 3], [4, 4]]
# Print keypoints positions to stdout
sys.stdout.write(repr(example_list))
sys.stdout.write("\n")
sys.stdout.flush()

sys.stdout.write(repr(example_list))
sys.stdout.write("\n")
sys.stdout.flush()