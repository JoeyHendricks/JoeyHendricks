<p align="center">
  <img src="https://github.com/JoeyHendricks/JoeyHendricks/blob/main/rest-by-fire-image.png?raw=true"/>
</p>


## Updating log4j files within Neoload

As many of you have possible also noticed there is a 
[massive security vulnerability](https://www.cert.govt.nz/it-specialists/advisories/log4j-rce-0-day-actively-exploited/) 
currently, in the Java logging library, Apache Log4j between versions 2.0 and 2.14.1 this problem has been repaired in 
a newer version of log4j(2.15), but it could be possible that you might still be using an older version.

When I heard about this vulnerability I started to review my Java tooling to verify which Log4j version 
they are using and try to update them. One of the tools I use is Neoload, and I noticed it has an 
older log4j version, so I decided to write quick last minute guide with a possible workaround to the problem.

So if you are using a Neoload version between 7.4 and 7.10 it will be likely that you are using a version of 
log4j that has the vulnerability. (I have not checked all versions, but you are likely using an older version.)

The purpose of this quick and dirty guide is to help out people with updating their instance of Neoloads 
Log4j libraries. **I have tested this quickly on my machine and everything seems to work fine so fingers 
crossed until Neotys comes with an official patch for this vulnerability.** ( So no guarantees that it works :D )

If you encounter any problems with this workaround please let me know, so I can either remove, update or put a 
warning on this guide.

> The following I have tried on my Windows 10 machine using Neoload version 7.9.

## Delete the old Apache log4j files from the installation folder.

Find the following files in the installation directory of Neoload, in my case this is 
"C:\Program Files\NeoLoad 7.9\lib", select the files that I have highlighted in the image and delete them. 
(Just to be sure I would recommend backing them up in a separate folder, just in case you encounter problems.)

<p align="center">
  <img src="https://github.com/JoeyHendricks/JoeyHendricks/blob/main/images/log4j-neoload-post/frame_1.png?raw=true"/>
</p>

## Download the new Apache log4j files from the vendor's website.

Download the most recent log4j files from the [Apache website](https://logging.apache.org/log4j/2.x/download.html) 
and unzip them.

<p align="center">
  <img src="https://github.com/JoeyHendricks/JoeyHendricks/blob/main/images/log4j-neoload-post/frame_2.png?raw=true"/>
</p>

Make sure you have extracted the following files:

<p align="center">
  <img src="https://github.com/JoeyHendricks/JoeyHendricks/blob/main/images/log4j-neoload-post/frame_3.png?raw=true"/>
</p>

## Copy the files into the Neoload installation directory.

Make sure that all the files are put back into the "lib" folder, and you should be okay to start up Neoload again 
with an update log4j version.

<p align="center">
  <img src="https://github.com/JoeyHendricks/JoeyHendricks/blob/main/images/log4j-neoload-post/frame_4.png?raw=true"/>
</p>

## Conclusion

Hopefully, this workaround is useful for you and it might save you some time and effort in dealing 
with this security issue if you have any additions to this guide then please let me know, so I can update it 
accordingly.

Let me know if this works for you!