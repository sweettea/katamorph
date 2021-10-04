import os.path, tempfile
from subprocess import Popen

SECTOR_SIZE = 512

class Device:
    """
    A class representing a single block device.
    """
    def __init__(self, **kwargs):
        assert len(kwargs) == 1, \
               "either name or path but not both should be set"
        if 'name' in kwargs:
            self.name = kwargs['name']
            self.path = _path_from_name(self.name)
        if 'path' in kwargs:
            self.path = kwargs['path']
            self.name = _name_from_path(self.path)
        
        if not os.path.exists(self.path):
            raise FileNotFoundError(
                f"""{self.path} does not exist or is invisible to the current
                user""")
        self._determine_canon_name()

    def _path_from_name(name):
        """ Determine the path, based on the name."""
        raise NotImplementedError()

    def _name_from_path(path):
        """ Determine the name, based on the path"""
        return os.path.basename(path)

    def _determine_canon_name(self):
        """
        Determine and store the canonical name of the device.

        If the provided path is a symlink, follow the symlinks to get down to
        the canonical /dev/foo name, then extract that foo bit."""
        self.canon_path = os.path.realpath(self.path)
        self.canon_name = os.path.basename(self.canon_path)

    def get_size(self):
        """Returns the size of this device, in bytes"""
        with open(f"/sys/block/{self.canon_name}/size", 'r') as f:
            sectors = int(f.read())
        return sectors * SECTOR_SIZE

class DmDevice(Device):
    """ A class representing a dm device.

    If created with create=True, will create the device via additional args
    target_type and table_args.
    """
    def __init__(self, **kwargs):
        if not kwargs.get('create'):
            # XXX check that it is a dm device in init
            super(DmDevice, self).__init__(**kwargs)
            # XXX get table
        else:
            assert(kwargs.get('name'))
            assert(kwargs.get('target_type'))
            assert(kwargs.get('table_args'))
            dmsetup_create = Popen(["dmsetup", "create", kwargs.name,
                                    "--table", " ".join(kwargs.table_args)], text=True)
            dmsetup_create.wait()
            self.table_args = kwargs.table_args
            super(DmDevice, self).__init__(**kwargs)

    def _path_from_name(name):
        return f"/dev/mapper/{self.name}"

    def __del__(self):
        dmsetup_remove = Popen(["dmsetup", "remove", self.name], text=True)
        dmsetup_remove.wait()
        super(DmDevice, self).__del__()
    def disableIO(self):
        dmsetup_reload = Popen(["dmsetup", "reload", self.name,
                                "--table", " ".join(kwargs.table_args[2], "error")], text=True)
        dmsetup_reload.wait()
        dmsetup_resume = Popen(["dmsetup", "resume", self.name]).wait()

    def enableIO(self):
        dmsetup_reload = Popen(["dmsetup", "reload", self.name,
                                "--table", " ".join(kwargs.table_args)], text=True)
        dmsetup_reload.wait()
        dmsetup_resume = Popen(["dmsetup", "resume", self.name]).wait()



class LoopDevice(Device):
    """
    A class representing a loop device and the file backed by it

    Unlike a Device, the name must not be specified and a dir and size in
    bytes must be specified.
    """
    def __init__(self, **kwargs):
        assert(kwargs['dir'] and kwargs['size'])
        self.backing_file = tempfile.NamedTemporaryFile(dir=kwargs['dir'])
        self.backing_file.seek(int(kwargs['size']) - 1)
        self.backing_file.write('\0')
        self.backing_file.flush()
        loop_dev_path = self._create_loop_dev(filename = self.backing_file.name)
        super(LoopDevice, self).__init__(path = loop_dev_path)

    def _create_loop_dev(filename):
        """ Create a loop device atop the given filename, returning its path"""
        losetup = Popen(["losetup", "-f", filename, "--show"], text=True)
        loop_path = losetup.communicate()
        return loop_path
    
    def __del__(self):
        losetup = Popen(["losetup", "-d", self.path]);
        losetup.wait()
        self.backing_file.close()
        super(LoopDevice, self).__del__()



        

