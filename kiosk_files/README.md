# Kiosk Setup
This is a work in progress.  The bits and pieces needed to configure everything are here, but still just a dumping ground for things that will be automated and documented,  Please don't expect this to work yet or to be clearly documented.  In time, it will come.

The instructions here are designd to automate the entire process of turning a raspbery pi into a kiosk.  It will setup files specifically for busstop, but could be used for other applications if you would like to fork it and use it in your own projects.

It will attempt to make backups of any file that is modified, should you want to revert to the original, but please use at your own risk.  Read the script before you run it, espeically as it will run with root privelages.

    ./setup_kiosk.sh
