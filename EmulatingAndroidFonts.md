To mitigate detection of the OpenWPM-Mobile by font-based fingerprinting,
you may uninstall all fonts present on your crawler machine and install fonts
extracted from a real Android device.

## 1 Extracting Android fonts:

Connect the Android device you want to emulate in USB debugging mode.
Copy the Android fonts from the phone using `adb`:

```
mkdir android_fonts  # create a directory for the font files
cd android_fonts
adb pull /system/fonts  # copy the font files from the device
```

## 2 Adding Android fonts to the crawler machine:

```
mv ~/.fonts ~/.fonts_BKP  # back-up existing user-specific fonts - may or may not exist
mkdir -p ~/.fonts  # create the user-specific font directory
cp android_fonts/* ~/.fonts # copy font files extracted from the Android device
fc-cache -f -v # update the font cache

```


## 3 Comment out the aliases for `MS Gothic` and `MS PGothic` fonts in `/etc/fonts/conf.avail/30-cjk-aliases.conf`

```
<!-- Aliases for Japanese Windows fonts -->
<!--    <alias>
        <family>MS Gothic</family>
        <accept>
            <family>Noto Sans Mono CJK JP</family>
            <family>TakaoGothic</family>
            <family>IPAGothic</family>
            <family>IPAMonaGothic</family>
            <family>VL Gothic</family>
            <family>Sazanami Gothic</family>
            <family>Kochi Gothic</family>
        </accept>
    </alias>
-->
...
<!--    <alias>
        <family>MS PGothic</family>
        <accept>
            <family>Noto Sans CJK JP</family>
            <family>IPAMonaPGothic</family>
            <family>TakaoPGothic</family>
            <family>IPAPGothic</family>
            <family>VL PGothic</family>
            <family>Sazanami Gothic</family>
            <family>Kochi Gothic</family>
        </accept>
    </alias>
-->
```

## 4 Remove existing system-wide fonts:
We need to empty	`/usr/share/fonts` and `/usr/local/share/fonts`

```
mkdir ~/usr_share_bkp
mkdir ~/usr_local_share_bkp
mv /usr/share/fonts/* ~/usr_share_bkp
mv /usr/local/share/fonts* ~/usr_local_share_bkp
fc-cache -f -v
```

If you are using a non-Debian based distro, check `/etc/fonts/fonts.conf`
for `<!-- Font directory list -->` and move the font files in those dirs to a backup dir.

### Restoring old fonts after the crawl:
mv ~/usr_share_bkp/* /usr/share/fonts/ 
mv ~/usr_local_share_bkp/*  /usr/local/share/fonts/ 
mv ~/.fonts_BKP ~/.fonts 
