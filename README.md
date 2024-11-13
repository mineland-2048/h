# Mineland's pack packer for packing packs automatically

These are some tools that aid with the annoying process of multiple file stuff with resource packs and such. 

There are two main things to note:

## pack.py

This is the one that will pack all the files.

#### options:

  -h, --help            show this help message and exit
  
  -f `FILE`, --file `FILE`  Name of the output file (Dont add the extension, it will be zip. Default: pack)
  
  -p `PATH`, --path `PATH`  Path to pack
  
  -d `DIR`, --dir `DIR`     Destination folder (Default: current dir). Can be set to `!copy` to move the dir into the copy destination. Will ignore date if thats the case)

  -c `CONFIG`, --config `CONFIG`
                        Config file to check. Uses ./config.cfg if not set, Will ignore the default if other arguments are present


  
  -cp `COPY`, --copy `COPY` Directory to copy to. For faster testing purposes
  
  -ncp, --no-copy       Forces no copy if set on the config file

  --date                Append date time to the name of the zip file
  
  --no-date             Removes date if set on the config file

  -s, --silent          Silent mode. Less command output


---

Ill append examples and doc for bulkRename.py tomorrow. I need sleep 