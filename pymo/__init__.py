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


def _get_new_filename(tags, format_str, pad):
    filename = format_str
    for tag, fmt in TAG_FORMATS.items():
        if tags[tag]:
            tag_value = tags[tag]
            if tag == "track":
                tag_value.zfill(pad)
            filename = filename.replace(fmt, tag_value)
    return filename


def _transform_filename(filename, transforms):
    new_filename = filename
    if "lc" in transforms:
        new_filename = new_filename.lower()
    elif "uc" in transforms:
        new_filename = new_filename.upper()
    elif "jc" in transforms:
        segments = []  # to be joined with os.path.join
        for segment in os.path.split(new_filename):
            words = segment.split()
            segment = words.pop(0).lower()  # first one is lowercase
            for word in words:
                word = word.lower()
                segment += word[0].upper()
                segment += word[1:].lower()
            segments.append(segment)
        new_filename = os.path.join(*segments)
    elif "cc" in transforms:
        segments = []  # to be joined with os.path.join
        for segment in os.path.split(new_filename):
            words = segment.split()
            segment = ""
            for word in words:
                word = word.lower()
                segment += word[0].upper()
                segment += word[1:].lower()
            segments.append(segment)
        new_filename = os.path.join(*segments)

    if "us" in transforms:
        new_filename = new_filename.replace(" ", "_")

    if "rs" in transforms:
        new_filename = new_filename.replace(" ", "")

    if "rp" in transforms:
        new_filename = re.sub("[!@#$%^&*():;?=+~`<>,]", "", new_filename)

    if "pu" in transforms:
        new_filename = re.sub("[!@#$%^&*():;?=+~`<>,]", "_", new_filename)

    return new_filename


def _get_file_tags(filename):
    """
    Given a filename, this retreives all tags it can, and returns a dict.
    If a tag is unavailable, ``None`` is given as it's value.
    """
    #TODO: use mutagen, for cross-format tag retreival
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

    if opts["-f"]:
        fmt = opts["-p"]
    else:
        fmt = "%p/%a/%t-%n"

    if opts["-m"]:
        method = "move"
        cmd = "mv"
    elif opts["-l"]:
        method = "link"
        cmd = "ln -s"
    else:
        method = "copy"
        cmd = "cp"

    if opts["-p"]:
        pad = int(opts["-p"])
    else:
        pad = 2

    if opts["-t"]:
        transforms = opts["TRANSFORMS"].split(",")
    else:
        transforms = []

    soundfiles = _walk(indir, [outdir,])
    for soundfile in soundfiles:
        soundfile_tags = _get_file_tags(soundfile)
        newfile = _get_new_filename(soundfile_tags, fmt, pad)
        newfile = _transform_filename(newfile, transforms)
        if "%" in newfile:  # a tag has not been replaced
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

            # do the move/cp/link
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
