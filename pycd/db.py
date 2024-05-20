from pathlib import Path
import json
import fnmatch

def get_pattern(pattern):
    dir = "*" + "*".join(pattern) + "*"
    return dir

class LookUpFile:

    def __init__(self,fname):
        self.fname = Path(fname).resolve()
        self.init()

    def init(self):
        if not self.fname.exists():
            with open(self.fname, "w") as fh:
                json.dump({},fh)

    def load(self):
        with open(self.fname) as fh:
            data = json.load(fh)
        return data

    def add(self,dirname):
        dirname = Path(dirname).resolve()
        if not dirname.is_file():
            if dirname.exists():
                _dir = str(dirname)
                data = self.load()
                if not _dir in data:
                    data[_dir] = 0
                data[_dir] += 1
                self.save(data)

    def save(self,data):
        with open(self.fname,"w") as fh:
            json.dump(data,fh)

    def get_all_matches_by_rank(self,pattern):
        pattern = get_pattern(pattern)
        data = self.load()
        output = list()
        for k,v in data.items():
            if fnmatch.fnmatch(k,pattern):
                output.append([k,v])
        if not output:
            return None
        else:
            return output

    def get_dir(self,pattern):

        output = self.get_all_matches_by_rank(pattern)
        if not output:
            return None
        # change with sort
        max_value = 0
        odir = None
        for k in output:
            if max_value < k[1]:
                max_value = k[1]
                odir = k[0]
        return odir

    def script(self,pattern):
        dir = self.get_dir(pattern)
        if dir:
            return f"cd {dir}"
        else:
            return ""


class DB:

    def __init__(self,path):
        self.path = Path(path).resolve()
        self.path.mkdir(exist_ok=True,parents=True)
        self.lf = LookUpFile(self.path / "lookup")

    def add(self,path):
        self.lf.add(path)

    def get_dir(self,pattern):
        return self.lf.get_dir(pattern)

    def script(self,pattern):
        return self.lf.script(pattern)
