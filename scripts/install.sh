# @Author: AnthonyKenny98
# @Date:   2020-01-14 15:18:30
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2020-01-14 17:05:57

clear

export ROOT=`pwd`
export LOGS_FOLDER="$ROOT/logs"
export INSTALL_LOG="$LOGS_FOLDER/install.out"
export VENV_FOLDER="venv"

# Function to log string and print to stdout
log_print () {
    printf "$1" 2>&1 | tee -a $INSTALL_LOG
}

# Make folder for logs
if [ ! -d "$LOGS_FOLDER" ]; then
    mkdir "$LOGS_FOLDER"
fi

# Remove existing logs
if [ -f "$INSTALL_LOG" ]; then
    rm $INSTALL_LOG
    touch $INSTALL_LOG
fi

# Install virtualenv
log_print "Installing virtualenv package...\n"
pip3 install virtualenv >> $INSTALL_LOG
log_print "Done\n\n"

# Remove existing Venv folder
if [ -d "$VENV_FOLDER" ]; then
    log_print "Removing existing virtual environment...\n"
    rm -rf "$VENV_FOLDER"
    log_print "Done\n\n"
fi

# Create New Virtual Environment
log_print "Creating New Virtual Environment...\n"
virtualenv venv >> $INSTALL_LOG
log_print "Done\n\n"

# Source Virtual Env
log_print "Entering Virtual Environment...\n"
source $ROOT/venv/bin/activate
log_print "Done\n\n"

# Installing Dependencies
log_print "Installing Dependencies...\n\n"
    # Check if pip3 is installed
if ! hash pip3 2>/dev/null; then
    log_print "\nERROR: pip3 is not installed and is required.\n"
    exit 1;
fi
pip3 install -r requirements.txt >> $INSTALL_LOG
# Need to do some installation check here
log_print "Done\n\n"

# Deactivate Virtual Environment
log_print "Exiting Virtual Environment\n"
deactivate >> $INSTALL_LOG
log_print "Done.\n\n\nInstallation Complete!!!\n\n"
