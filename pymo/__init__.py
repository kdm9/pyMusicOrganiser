from __future__ import print_function
import os
import sys
import id3reader
import re


TAGS = ['album', 'comment', 'performer', 'title', 'track', 'year', 'genre']


TAG_FORMATS = {
    'album': "%a",
    'performer': "%p",
    'title': "%n",
    'track': "%t",
    'year': "%y",
    'genre': "%g",
    'comment': "%c",
}


def _get_new_filename_from_tags_and_format(tags, format_str):
    filename = format_str
    for tag, fmt in TAG_FORMATS.items():
        if tags[tag]:
            tag_value = tags[tag]
            filename = filename.replace(fmt, tag_value)
    return filename


def _get_file_tags(filename):
    id3tags = id3reader.Reader(filename)
    tags = {}
    for tag in TAGS:
        try:
            tag_value = id3tags.getValue(tag)
            tags[tag] = tag_value
        except:
            tags[tag] = None
    return tags


def _walk(rootdir, excludedirs=[]):
    soundfiles = []
    for root, dirs, files in os.walk(rootdir):
        if root in excludedirs:
            sys.stderr.write("%s excluded from walk\n" % root)
            continue
        for fle in files:
            soundfiles.append(os.path.join(root, fle))
    return soundfiles


def main(opts):
    indir = opts["<inputdir>"]
    outdir = opts["<outputdir>"]
    fmt = opts["<format>"]
    if opts["-m"]:
        method = "move"
        cmd = "mv"
    elif opts["-l"]:
        method = "link"
        cmd = "ln -s"
    else:
        method = "copy"
        cmd = "cp"

    soundfiles = _walk(indir, [outdir,])
    for soundfile in soundfiles:
        soundfile_tags = _get_file_tags(soundfile)
        newfile = _get_new_filename_from_tags_and_format(soundfile_tags, fmt)
        if "%" in newfile:
            sys.stderr.write("Couldn't get tags required to move '%s'\n" % \
                    soundfile)
            continue
        newfile = os.path.join(outdir, newfile)
        if opts["-v"] or opts["-n"]:
            print("%s '%s' '%s'" % (cmd, soundfile, newfile))
        if not opts["-n"]:
            # make dir
            newdirname = os.path.dirname(newfile)
            if not os.path.exists(newdirname):
                try:
                    os.makedirs(newdirname)
                except:
                    sys.stderr.write("Couldn't make directory '%s'" % \
                            newdirname)
                    continue

            try:
                if method == "move":
                    os.rename(soundfile, newfile)
                elif method == "link":
                    os.symlink(soundfile, newfile)
                else:
                    shutil.copyfile(soundfile, newfile)
            except:
                sys.stderr.write("Couldn't %s '%s' to '%s'\n" % \
                        (method, soundfile, newfile))
