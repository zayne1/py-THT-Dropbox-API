# Dropbox API Demo

A Python script that connects to and uses the Dropbox V2 API

Info:

The app connects to Dropbox via an access token, which lasts for 4 hours. 
We built in a caching mechanism that stores this access token to disk for three hours, as we would then otherwise be creating a new 4 hour access token on each run of the script.

If the script is run again any time after 3 hours, a new token will be retrieved, and cached.

The program itself has access to the account holder's personal info (we greet the user by name).

It also pulls the remote file list, as well as metadata (only modified date for now)

Storage info is retrieved as well (total space allocation as well as space used.)

A somewhat randomly named file is then generated, populated with the current date stamp, and then uploaded to Dropbox.

Once this is done, the update remote file list is then retrieved.


# Setup - Installing Python (Linux):
To see which version of Python 3 you have installed, open a command prompt and run

```
$ python3 --version
```

If you are using Ubuntu 16.10 or newer, then you can easily install Python 3.6 with the following commands:

```
$ sudo apt-get update
$ sudo apt-get install python3.6
```

If you’re using another version of Ubuntu (e.g. the latest LTS release) or you want to use a more current Python, we recommend using the deadsnakes PPA to install Python 3.8:

```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.8
```

At this point, you may have system Python 2.7 available as well.
```
$ python
```
This might launch the Python 2 interpreter.
```
$ python3
```
This will always launch the Python 3 interpreter.


# Setup - Installing Python (Windows):

1. Open your web browser and navigate to the Downloads for Windows section of the official Python website.
2. Search for Python3
3. Select a link to download either the Windows x86-64 executable installer or Windows x86 executable installer
4. For all recent versions of Python, the recommended installation options include *Pip* and *IDLE*. Older versions might not include such additional features.

# Setup - Installing Pip:

To see if pip is installed, open a command prompt and run
```
$ command -v pip
```
Note that on some Linux distributions including Ubuntu and Fedora the pip command is meant for Python 2, while the pip3 command is meant for Python 3.
```
$ command -v pip3
```
*Installation*
Try
```
python -m ensurepip --upgrade
```
and if the above fails, try the alternate method using get-pip.py: 

Download the script, from [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py). 

Open a terminal/command prompt, cd to the folder containing the get-pip.py file and run:
```
python get-pip.py
```

# Setup - Installing curl:
The program makes use of the curl program, which is usually installed on most servers. 

To test if you have curl installed, simply do the following from the terminal, on all OS's
```
curl
```

To install it on Linux, run the following from the terminal
```
sudo apt-get install curl
```
To install curl on Windows
1. In Windows, create a folder called curl in your C: drive.

2. Go to http://curl.haxx.se/download.html and download one of the following zip files:

  - If you have a Windows 64 system, scroll to the Win64 - Generic section and look for the latest Win64 ia64 zip version with SSL support. It's normally second in the list. Click the version number to start the download.
  - If you have a Windows 32 system, scroll to the Win32 - Generic section and look for the latest Win32 zip version with SSL support. It's normally second in the list. Click the version number to start the download.

3. Unzip the downloaded file and move the curl.exe file to your C:\curl folder.

4. Go to http://curl.haxx.se/docs/caextract.html and download the digital certificate file named cacert.pem.

The PEM file contains a bundle of valid digital certificates. The certificates are used to verify the authenticity of secure websites. They're distributed by certificate authority (CA) companies such as GlobalSign and VeriSign. The PEM file allows cURL to connect securely to the Zendesk API using the Secure Sockets Layer (SSL) protocol.

5. Move the cacert.pem file to your C:\curl folder and rename it curl-ca-bundle.crt.

6. Add the curl folder path to your Windows PATH environment variable so that the curl command is available from any location at the command prompt. Update the variable as follows:

    1. In the Start menu, right-click This PC and select More > Properties. 
  Note: In Windows 7, right-click Computer and select Properties.

    2. Click Advanced System Settings.

    3. In the Advanced tab, click the Environment Variables button on the lower right side.

    4. Select the "Path" variable in System Variables, and click Edit.

    5. In the Edit environment variable dialog box, click New and add the path to the curl.exe file. Example: C:\curl.

# Executing script

To start, we need to install the Dropbox Python SDK from the terminal:

```
pip install dropbox
```
or alternatively,
```
python3 -m pip install dropbox
```

Then to run the script, simply run:
```
python3 zayne-THT-DropBox.py
```
